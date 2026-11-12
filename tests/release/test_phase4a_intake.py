from __future__ import annotations

import json
from pathlib import Path

from data_generator.release_profile import load_release_profile

ROOT = Path(__file__).resolve().parents[2]


def test_demo_release_profile_locks_phase4_story() -> None:
    profile = load_release_profile(ROOT, "demo")
    assert profile.seed == 260311
    assert profile.golden_supplier_id == "SUP-0104"
    assert profile.golden_component_id == "CMP-MCU-42"
    assert profile.golden_purchase_order_id == "PO-2208"


def test_phase4a_intake_report_passed() -> None:
    report = json.loads(
        (ROOT / "data" / "releases" / "v1.0.0" / "reports" / "phase-3-intake.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["status"] == "PASS"
