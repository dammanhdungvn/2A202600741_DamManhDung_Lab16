# Data Model

## Entities

### `JudgeResult`
Represents the outcome from the `evaluator()` LLM call.
- **`is_correct`** (bool): Whether the actor's predicted answer matches the gold answer conceptually.
- **`feedback`** (str): Detailed feedback or explanation of why the answer is correct or incorrect.
- **`score`** (int): Optional score (0-100) indicating confidence or degree of correctness.

### `ReflectionEntry`
Represents the self-reflection output from the `reflector()` LLM call.
- **`attempt_id`** (int): The ID of the attempt that failed.
- **`lesson`** (str): What the agent learned about why its previous attempt failed.
- **`strategy`** (str): An actionable strategy to try in the next attempt to avoid the same mistake.
- **`failure_mode`** (str): Categorization of the failure (e.g., "incomplete_multi_hop", "entity_drift", "wrong_final_answer").

*(Other entities like `QAExample`, `AttemptTrace`, `RunRecord`, and `ReportPayload` are already defined in `schemas.py` and require no structural changes, though `JudgeResult` and `ReflectionEntry` will be integrated into the attempt traces).*
