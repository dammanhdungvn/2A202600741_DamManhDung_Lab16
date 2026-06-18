# Quickstart: Lab 16 Reflexion Agent Validation

## Prerequisites
1. Python 3.11+ environment with `requirements.txt` installed (including `openai`).
2. `.env` file configured with Qwen API credentials:
   ```env
   QWEN_API_KEY=your_key_here
   QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
   QWEN_MODEL_NAME=qwen-plus
   ```
3. A dataset file `data/evaluation_100.json` containing at least 100 QAExample records.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install openai python-dotenv
```

## Validation Scenario 1: Run Benchmark
Execute the benchmark script against the evaluation dataset to trigger the Reflexion Loop using Qwen API.
```bash
python run_benchmark.py --dataset data/evaluation_100.json --out-dir outputs/qwen_run
```
**Expected Outcome**: The script should complete successfully, generating a `report.json` and trace files in `outputs/qwen_run/`. You should see `latency_ms` and `token_estimate` populated realistically.

## Validation Scenario 2: Autograde
Verify the project against the grading script to ensure it meets the success criteria (80/80 for Core Flow).
```bash
python autograde.py --report-path outputs/qwen_run/report.json
```
**Expected Outcome**: The console should display a score breakdown totaling at least 80/100, verifying that `num_records >= 100` and all schema validation checks pass.
