import json
import tempfile
import pytest
from pathlib import Path
from src.ui.utils.report_parser import parse_report, ReportMetrics

def test_parse_report():
    # Create dummy JSON report
    dummy_data = {
        "summary": {
            "react": {
                "em": 0.45,
                "avg_attempts": 1.0
            },
            "reflexion": {
                "em": 0.85,
                "avg_attempts": 2.5
            }
        },
        "examples": [
            {
                "qid": "q1",
                "agent_type": "react",
                "gold_answer": "Paris",
                "predicted_answer": "London",
                "is_correct": False,
                "attempts": 1,
                "failure_mode": "hallucination",
                "reflection_count": 0
            },
            {
                "qid": "q2",
                "agent_type": "reflexion",
                "gold_answer": "7",
                "predicted_answer": "7",
                "is_correct": True,
                "attempts": 2,
                "failure_mode": None,
                "reflection_count": 1
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(dummy_data, f)
        temp_path = f.name
        
    try:
        metrics = parse_report(temp_path)
        
        assert metrics.react_em == 0.45
        assert metrics.reflexion_em == 0.85
        assert metrics.react_avg_attempts == 1.0
        assert metrics.reflexion_avg_attempts == 2.5
        assert len(metrics.failure_modes) == 1
        
        fm = metrics.failure_modes[0]
        assert fm.question_id == "q1"
        assert fm.agent_type == "react"
        assert fm.predicted_answer == "London"
        
    finally:
        Path(temp_path).unlink()
