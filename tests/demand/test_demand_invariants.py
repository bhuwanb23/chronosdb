from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from data_generator.phase4_validation import validate_demand_release

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "releases" / "v1.0.0"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_golden_customer_orders_have_expected_revenue_risk() -> None:
    assignments = _rows(RELEASE / "demand" / "customer_sla_assignments.csv")
    golden = [
        row
        for row in assignments
        if row["customer_order_line_id"]
        in {"COL-CO-0701-01", "COL-CO-0704-01", "COL-CO-0711-01"}
    ]
    assert sum(Decimal(row["revenue_at_risk"]) for row in golden) == Decimal("1600000")


def test_demand_release_relationships_and_formulas() -> None:
    demand = {
        "orders": _rows(RELEASE / "demand" / "customer_orders.csv"),
        "lines": _rows(RELEASE / "demand" / "customer_order_lines.csv"),
        "statuses": _rows(RELEASE / "demand" / "customer_order_status_history.csv"),
        "allocations": _rows(RELEASE / "demand" / "production_customer_allocations.csv"),
        "sla_assignments": _rows(RELEASE / "demand" / "customer_sla_assignments.csv"),
    }
    master = {
        name: _rows(RELEASE / "master" / f"{name}.csv")
        for name in ("customers", "products")
    }
    production = _rows(RELEASE / "production" / "production_orders.csv")
    validate_demand_release(demand, master, production)
