# Research: Lab 16 Reflexion Agent

## LLM API Integration

**Decision**: Use Qwen API via the official `openai` SDK in Python.
**Rationale**: The user specifically requested to use the Qwen model with API keys from `.env`. The provided documentation (`docs/qwen-api.md`) explicitly indicates that Qwen is OpenAI-compatible and should be invoked using the `OpenAI` client class.
**Alternatives considered**: Using generic `requests` or `langchain`. Rejected because the project provides a clean `docs/qwen-api.md` stating we should use `openai` SDK directly to avoid unnecessary abstraction layers.

## Structured Output (JudgeResult & ReflectionEntry)

**Decision**: Use Pydantic models with OpenAI SDK's `response_format` (JSON schema parsing) or instruct the model to return raw JSON and use `json.loads`.
**Rationale**: The `schemas.py` requires `JudgeResult` and `ReflectionEntry` to be populated. The Qwen API can generate structured output. We can enforce JSON output in the system prompt.
**Alternatives considered**: Regex parsing. Rejected because JSON is much more reliable and standard for LLM output extraction.

## Dataset Generation

**Decision**: Create a Python script (`create_dataset.py`) or manually provide a sample of 100+ questions based on HotpotQA or generated synthetically to satisfy the autograder requirement.
**Rationale**: Autograder requires at least 100 questions.
