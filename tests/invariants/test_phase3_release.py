from __future__ import annotations

import json
from pathlib import Path

from data_generator.release_validation import build_validation_report

ROOT = Path(__file__).resolve().parents[2]


def test_all_phase3_scales_have_zero_release_validation_errors() -> None:
    report = build_validation_report(ROOT)
    assert report["summary"]["validation_errors"] == 0
    assert report["summary"]["warnings"] == 0


def test_phase4_contract_covers_packaged_files() -> None:
    contract = json.loads((ROOT / "data" / "phase4_load_contract.json").read_text(encoding="utf-8"))
    assert contract["contract_version"] == "1.0.0"
    assert len(contract["files"]) >= 100
    assert all(
        entry["source_file"] and entry["expected_target_table"] and entry["checksum"]
        for entry in contract["files"]
    )
