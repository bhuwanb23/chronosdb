from __future__ import annotations

import csv
import json
from pathlib import Path

from data_generator.phase4_validation import validate_history_release

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "releases" / "v1.0.0"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_temporal_history_has_bitemporal_replay_cases() -> None:
    history = {
        "entity_versions": _rows(RELEASE / "history" / "entity_versions.csv"),
        "business_events": _rows(RELEASE / "history" / "business_events.csv"),
        "late_arriving_records": _rows(RELEASE / "history" / "late_arriving_records.csv"),
        "historical_inventory_checkpoints": _rows(
            RELEASE / "history" / "historical_inventory_checkpoints.csv"
        ),
        "replay_expectations": json.loads(
            (RELEASE / "history" / "replay_expectations.json").read_text(
                encoding="utf-8"
            )
        ),
    }
    inventory = {
        "transactions": _rows(RELEASE / "inventory" / "inventory_transactions.csv")
    }
    validate_history_release(history, inventory)
    cases = history["replay_expectations"]["late_arrival_cases"]
    assert [case["uses_correction"] for case in cases] == [False, True, False]
