from __future__ import annotations

from ..contracts.errors import StateReconstructionError

REQUIRED_RECORD_SETS = {
    "suppliers",
    "components",
    "products",
    "purchase_orders",
    "inventory_opening_balances",
    "production_orders",
    "customer_orders",
    "customer_order_lines",
}


def validate_state_records(records: dict[str, list[dict[str, str]]]) -> list[str]:
    missing = sorted(REQUIRED_RECORD_SETS - records.keys())
    if missing:
        raise StateReconstructionError(f"missing record sets: {missing}")
    warnings: list[str] = []
    for name, rows in records.items():
        if not rows:
            warnings.append(f"empty record set: {name}")
    return warnings
