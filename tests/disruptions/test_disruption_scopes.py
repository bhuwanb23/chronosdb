from __future__ import annotations

import csv
from pathlib import Path

from data_generator.phase4_validation import validate_disruptions_release

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "releases" / "v1.0.0"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_golden_disruption_scope_is_canonical() -> None:
    disruptions = {
        "events": _rows(RELEASE / "disruptions" / "disruption_events.csv"),
        "scope_components": _rows(
            RELEASE / "disruptions" / "disruption_scope_components.csv"
        ),
        "scope_purchase_orders": _rows(
            RELEASE / "disruptions" / "disruption_scope_purchase_orders.csv"
        ),
        "status_history": _rows(
            RELEASE / "disruptions" / "disruption_status_history.csv"
        ),
    }
    purchase_orders = _rows(RELEASE / "operations" / "purchase_orders.csv")
    validate_disruptions_release(disruptions, purchase_orders)
    golden = next(
        row
        for row in disruptions["events"]
        if row["disruption_event_id"] == "EVT-GOLD-001"
    )
    assert golden["event_type"] == "SUPPLIER_OUTAGE"
    assert golden["recovery_lag_hours"] == "48"
