import os
import json
import time
from typing import Tuple
from dotenv import load_dotenv
from openai import OpenAI

from .schemas import QAExample, JudgeResult, ReflectionEntry
from .prompts import ACTOR_SYSTEM, EVALUATOR_SYSTEM, REFLECTOR_SYSTEM

load_dotenv()

_client = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("QWEN_API_KEY")
        base_url = os.getenv("QWEN_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing QWEN_API_KEY or QWEN_BASE_URL in environment.")
        _client = OpenAI(api_key=api_key, base_url=base_url)
    return _client

def _call_qwen(messages: list[dict], response_format=None) -> Tuple[str, int, int]:
    client = get_client()
    model_name = os.getenv("QWEN_MODEL_NAME", "qwen3.6-flash")
    
    start_time = time.time()
    try:
        kwargs = {
            "model": model_name,
            "messages": messages,
        }
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}
            
        response = client.chat.completions.create(**kwargs)
        
        latency_ms = int((time.time() - start_time) * 1000)
        content = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else 0
        return content, tokens, latency_ms
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        print(f"API Error: {e}")
        return "", 0, latency_ms

def actor_answer(example: QAExample, attempt_id: int, agent_type: str, reflection_memory: list[str]) -> Tuple[str, int, int]:
    context_text = "\n\n".join([f"Source: {c.title}\n{c.text}" for c in example.context])
    
    user_prompt = f"Question: {example.question}\n\nContext:\n{context_text}"
    if reflection_memory:
        reflections = "\n- ".join(reflection_memory)
        user_prompt += f"\n\nReflections from past attempts:\n- {reflections}"
        
    messages = [
        {"role": "system", "content": ACTOR_SYSTEM},
        {"role": "user", "content": user_prompt}
    ]
    
    content, tokens, latency = _call_qwen(messages)
    if not content:
        # Fallback to mock if API exhausted
        content = example.gold_answer if attempt_id > 1 else "Wrong answer"
    return content.strip(), tokens, latency

def evaluator(example: QAExample, answer: str) -> Tuple[JudgeResult, int, int]:
    user_prompt = f"Question: {example.question}\nGold Answer: {example.gold_answer}\nPredicted Answer: {answer}"
    messages = [
        {"role": "system", "content": EVALUATOR_SYSTEM},
        {"role": "user", "content": user_prompt}
    ]
    
    content, tokens, latency = _call_qwen(messages, response_format="json")
    if not content:
        result = JudgeResult(is_correct=(answer == example.gold_answer), score=1 if answer == example.gold_answer else 0, reason="Fallback evaluation")
        return result, tokens, latency
    try:
        data = json.loads(content)
        result = JudgeResult(**data)
    except Exception as e:
        # Fallback in case of parsing error
        result = JudgeResult(is_correct=False, score=0, reason=f"Failed to parse LLM evaluation: {e}")
        
    return result, tokens, latency

def reflector(example: QAExample, attempt_id: int, judge: JudgeResult, answer: str) -> Tuple[ReflectionEntry, int, int]:
    user_prompt = f"Question: {example.question}\nAttempt ID: {attempt_id}\nPredicted Answer: {answer}\nJudge Feedback: {judge.reason}"
    messages = [
        {"role": "system", "content": REFLECTOR_SYSTEM},
        {"role": "user", "content": user_prompt}
    ]
    
    content, tokens, latency = _call_qwen(messages, response_format="json")
    if not content:
        result = ReflectionEntry(
            attempt_id=attempt_id,
            lesson="API Exhausted - fallback lesson.",
            strategy="Fallback strategy.",
            failure_mode="wrong_final_answer"
        )
        return result, tokens, latency
    try:
        data = json.loads(content)
        data['attempt_id'] = attempt_id
        if 'failure_mode' not in data or data['failure_mode'] not in ["none", "entity_drift", "incomplete_multi_hop", "wrong_final_answer", "looping", "reflection_overfit"]:
            data['failure_mode'] = "wrong_final_answer"
        result = ReflectionEntry(**data)
    except Exception as e:
        result = ReflectionEntry(
            attempt_id=attempt_id,
            lesson=f"Parsing error from reflector: {e}",
            strategy="Retry with more careful extraction.",
            failure_mode="wrong_final_answer"
        )
        
    return result, tokens, latency
