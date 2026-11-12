from __future__ import annotations

import json
from pathlib import Path

from data_generator.phase4_validation import validate_golden_release

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "data" / "releases" / "v1.0.0" / "golden"


def _json(name: str) -> object:
    return json.loads((GOLDEN / name).read_text(encoding="utf-8"))


def test_phase4_golden_headlines_and_timeline_are_frozen() -> None:
    golden = {
        "scenario": _json("scenario.json"),
        "state_at_as_of": _json("state_at_as_of.json"),
        "expected_candidate_results": _json("expected_candidate_results.json"),
        "expected_recommendation": _json("expected_recommendation.json"),
        "expected_timeline": _json("expected_timeline.json"),
    }
    validate_golden_release(golden)
    assert golden["expected_recommendation"]["recommended_intervention"] == "INT-GOLD-C"
