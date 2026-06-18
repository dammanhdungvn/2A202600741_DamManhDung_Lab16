# Implementation Plan: Lab 16 Reflexion Agent

**Branch**: `002-lab-reflexion-agent` | **Date**: 2026-06-18 | **Spec**: [spec.md](../spec.md)

**Input**: Feature specification from `/specs/002-lab-reflexion-agent/spec.md`

## Summary

Implement a Reflexion Agent to evaluate Qwen LLM performance on multi-hop questions. Replace the mock runtime with actual API calls to Qwen via the OpenAI SDK, properly parsing responses into `JudgeResult` and `ReflectionEntry` schemas. Autogenerate or provide a 100+ dataset to achieve an autograder score of >= 80.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `pydantic>=2.7`, `openai`, `python-dotenv`

**Storage**: Local JSON/JSONL files for datasets and reports.

**Testing**: Auto-graded via `autograde.py` measuring schema completeness and benchmark completion.

**Target Platform**: Local execution environment.

**Project Type**: CLI Tool / Agent Scaffold.

**Performance Goals**: Support sequential processing of 100+ QA records without hanging.

**Constraints**: Qwen API calls must be dynamic (no hardcoded keys).

**Scale/Scope**: Evaluate 100+ QA records, with max attempts limited to prevent infinite loops (adaptive_max_attempts recommended).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Production Quality**: Code will handle LLM JSON parsing errors safely (e.g., fallback parsing or retry logic).
- **Clean Architecture**: Agent loop is decoupled from LLM invocation. Mock runtime will be replaced by a clean `llm_client` wrapper or direct usage with clear boundaries.
- **RESTful API**: N/A (CLI tool).
- **Test Coverage**: Tested via `autograde.py` output.

## Project Structure

### Documentation (this feature)

```text
specs/002-lab-reflexion-agent/
├── plan.md              # This file
├── research.md          # Tech decisions for LLM API integration
├── data-model.md        # Schemas for JudgeResult and ReflectionEntry
├── quickstart.md        # Guide to run benchmark and autograder
├── contracts/           # Empty (no external API contracts exposed)
└── tasks.md             # Tasks for implementation
```

### Source Code (repository root)

```text
src/reflexion_lab/
├── schemas.py           # Add JudgeResult and ReflectionEntry fields
├── prompts.py           # Implement system prompts
├── mock_runtime.py      # Refactor actor_answer, evaluator, reflector to use Qwen
├── agents.py            # Complete Reflexion loop logic
data/
└── evaluation_100.json  # To be generated (100+ items)
```

**Structure Decision**: The project already provides an existing structure in `src/reflexion_lab`. We will work within this existing structure without creating new directories, merely editing the `.py` files to implement the logic.
