from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPERATIONS = ROOT / "data" / "releases" / "v1.0.0" / "operations"


def _rows(name: str) -> list[dict[str, str]]:
    with (OPERATIONS / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_golden_purchase_order_and_quantity_bounds() -> None:
    orders = _rows("purchase_orders.csv")
    golden = next(row for row in orders if row["id"] == "PO-2208")
    assert golden["supplier_id"] == "SUP-0104"
    assert golden["component_id"] == "CMP-MCU-42"
    assert golden["ordered_quantity"] == "800"
    assert golden["received_quantity"] == "0"
    for row in orders:
        assert 0 <= float(row["received_quantity"]) <= float(row["ordered_quantity"])
        assert float(row["outstanding_quantity"]) == (
            float(row["ordered_quantity"]) - float(row["received_quantity"])
        )
