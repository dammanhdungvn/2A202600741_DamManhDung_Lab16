import json
from dataclasses import dataclass
from typing import List

@dataclass
class FailureDetail:
    question_id: str
    agent_type: str
    gold_answer: str
    predicted_answer: str
    attempts: int
    failure_mode: str
    reflection_count: int

@dataclass
class ReportMetrics:
    react_em: float
    reflexion_em: float
    react_avg_attempts: float
    reflexion_avg_attempts: float
    failure_modes: List[FailureDetail]

def parse_report(report_path: str) -> ReportMetrics:
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    summary = data.get("summary", {})
    react_summary = summary.get("react", {})
    reflexion_summary = summary.get("reflexion", {})
    
    react_em = react_summary.get("em", 0.0)
    reflexion_em = reflexion_summary.get("em", 0.0)
    react_avg_attempts = react_summary.get("avg_attempts", 1.0)
    reflexion_avg_attempts = reflexion_summary.get("avg_attempts", 1.0)
    
    failure_modes = []
    examples = data.get("examples", [])
    for ex in examples:
        if not ex.get("is_correct", True):
            failure_modes.append(FailureDetail(
                question_id=ex.get("qid", ""),
                agent_type=ex.get("agent_type", ""),
                gold_answer=ex.get("gold_answer", ""),
                predicted_answer=ex.get("predicted_answer", ""),
                attempts=ex.get("attempts", 1),
                failure_mode=ex.get("failure_mode", ""),
                reflection_count=ex.get("reflection_count", 0)
            ))
            
    return ReportMetrics(
        react_em=react_em,
        reflexion_em=reflexion_em,
        react_avg_attempts=react_avg_attempts,
        reflexion_avg_attempts=reflexion_avg_attempts,
        failure_modes=failure_modes
    )
