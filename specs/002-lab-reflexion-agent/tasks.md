# Tasks: Lab 16 Reflexion Agent

**Input**: Design documents from `/specs/002-lab-reflexion-agent/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Qwen API configuration in `.env`
- [x] T002 Add `openai` and `python-dotenv` to `requirements.txt` and install them

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Update `src/reflexion_lab/schemas.py` to implement the `JudgeResult` Pydantic model
- [x] T004 Update `src/reflexion_lab/schemas.py` to implement the `ReflectionEntry` Pydantic model
- [x] T005 [P] Update `src/reflexion_lab/prompts.py` to define `ACTOR_SYSTEM`, `EVALUATOR_SYSTEM`, and `REFLECTOR_SYSTEM` prompts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Replace Mock Runtime with Actual LLM (Priority: P1) 🎯 MVP

**Goal**: Replace deterministic mock functions with live Qwen API calls via OpenAI SDK.

**Independent Test**: Running `python run_benchmark.py` against a subset of data should successfully hit the LLM endpoint and return diverse, parsed responses.

### Implementation for User Story 1

- [x] T006 [US1] Configure OpenAI client globally in `src/reflexion_lab/mock_runtime.py` using `python-dotenv`
- [x] T007 [P] [US1] Implement `actor_answer()` in `src/reflexion_lab/mock_runtime.py` to invoke Qwen
- [x] T008 [P] [US1] Implement `evaluator()` in `src/reflexion_lab/mock_runtime.py` to invoke Qwen and return `JudgeResult`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Implement Reflexion Loop (Priority: P1)

**Goal**: Update the agent loop to handle LLM feedback and reflect on failures.

**Independent Test**: Log outputs of the benchmark should show `attempt_count > 1` when the LLM makes an error and correctly feeds `reflection_memory` into the subsequent prompt.

### Implementation for User Story 2

- [x] T009 [P] [US2] Implement `reflector()` in `src/reflexion_lab/mock_runtime.py` to parse `ReflectionEntry`
- [x] T010 [US2] Implement the `run_reflexion_agent` reflexion loop logic in `src/reflexion_lab/agents.py`
- [x] T011 [US2] Update `agents.py` to dynamically record `token_estimate` and `latency_ms` from LLM usage

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Create Evaluation Dataset (Priority: P1)

**Goal**: Generate 100+ evaluation questions formatted as `QAExample` items.

**Independent Test**: Ensure `autograde.py` detects 100+ items inside `report.json`.

### Implementation for User Story 3

- [x] T012 [P] [US3] Create Python script `scripts/generate_dataset.py` to fetch/generate 100 `QAExample` items into `data/evaluation_100.json`
- [x] T013 [US3] Execute `scripts/generate_dataset.py` to populate the dataset file

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and validate the final lab deliverables.

- [x] T014 Run `python run_benchmark.py --dataset data/evaluation_100.json --out-dir outputs/qwen_run`
- [x] T015 Run `python autograde.py --report-path outputs/qwen_run/report.json` to verify score is >80/100
- [x] T016 Code cleanup (remove unused mock logic in `mock_runtime.py`)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed sequentially in priority order (US1 → US2 → US3) or concurrently if team size permits.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### Parallel Opportunities

- Schema modifications (T003, T004) and prompt creation (T005) can be done in parallel.
- `actor_answer` (T007), `evaluator` (T008), and `reflector` (T009) can be implemented in parallel.
- Dataset script generation (T012) can be done in parallel at any time during the project.

---

## Parallel Example: User Story 1 & 2 API Integration

```bash
# Developer A implements the Actor and Evaluator API calls
Task: "Implement actor_answer() in src/reflexion_lab/mock_runtime.py to invoke Qwen"
Task: "Implement evaluator() in src/reflexion_lab/mock_runtime.py to invoke Qwen and return JudgeResult"

# Developer B implements the Reflector API call simultaneously
Task: "Implement reflector() in src/reflexion_lab/mock_runtime.py to parse ReflectionEntry"
```

## Implementation Strategy

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Verify API connectivity → Run single record tests
3. Add User Story 2 → Verify Reflection loop triggers → Inspect traces
4. Add User Story 3 → Verify Autograder volume requirement
5. Validate end-to-end with full benchmark run.
