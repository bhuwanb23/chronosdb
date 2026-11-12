from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from data_generator.phase4_validation import (
    validate_capacity,
    validate_manufacturing_release,
)

ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT / "data" / "releases" / "v1.0.0" / "production"


def _rows(name: str) -> list[dict[str, str]]:
    with (PRODUCTION / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_golden_production_orders_and_batches() -> None:
    orders = _rows("production_orders.csv")
    golden = [row for row in orders if row["id"] in {"MO-0876", "MO-0882", "MO-0889"}]
    assert len(golden) == 3
    assert all(row["planned_quantity"] == "200" for row in golden)
    batches = _rows("production_batches.csv")
    assert sum(Decimal(row["material_quantity"]) for row in batches) == Decimal("800")


def test_manufacturing_formulas_and_capacity() -> None:
    orders = _rows("production_orders.csv")
    requirements = _rows("production_material_requirements.csv")
    batches = _rows("production_batches.csv")
    allocations = _rows("production_material_allocations.csv")
    capacity = _rows("facility_capacity_calendar.csv")
    validate_manufacturing_release(orders, requirements, batches, allocations)
    validate_capacity(batches, capacity)
