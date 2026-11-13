from __future__ import annotations

import json
from pathlib import Path

from scripts.impact_intake import run

ROOT = Path(__file__).resolve().parents[2]


def test_phase5_intake_passes() -> None:
    report = run()
    assert report["status"] == "PASS"
    assert report["issues"] == []


def test_intake_report_is_deterministic() -> None:
    run()
    report = json.loads(
        (ROOT / "artifacts" / "phase-5" / "intake-report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["runtime_expected_output_reads"] is False
