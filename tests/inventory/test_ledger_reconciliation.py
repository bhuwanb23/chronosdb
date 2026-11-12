from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from data_generator.phase4_validation import validate_inventory_release

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "data" / "releases" / "v1.0.0" / "inventory"


def _rows(name: str) -> list[dict[str, str]]:
    with (INVENTORY / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_release_inventory_reconciles_from_ledger() -> None:
    inventory = {
        "opening": _rows("inventory_opening_balances.csv"),
        "transactions": _rows("inventory_transactions.csv"),
        "reservations": _rows("inventory_reservations.csv"),
        "snapshots": _rows("inventory_snapshots_daily.csv"),
        "benchmark_snapshots": _rows("inventory_snapshots_benchmark.csv"),
        "transfer_transactions": _rows("transfer_transactions.csv"),
    }
    validate_inventory_release(inventory)


def test_golden_transferable_quantity_is_400() -> None:
    snapshots = _rows("inventory_snapshots_daily.csv")
    golden = next(
        row
        for row in snapshots
        if row["warehouse_id"] == "WH-CHENNAI"
        and row["component_id"] == "CMP-MCU-42"
    )
    assert Decimal(golden["transferable_quantity"]) == Decimal("400")
