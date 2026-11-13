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
    purchase_order_ids = [row.get("id", "") for row in records["purchase_orders"] if row.get("id")]
    duplicate_purchase_orders = sorted(
        {
            purchase_order_id
            for purchase_order_id in purchase_order_ids
            if purchase_order_ids.count(purchase_order_id) > 1
        }
    )
    if duplicate_purchase_orders:
        raise StateReconstructionError(f"duplicate purchase order IDs: {duplicate_purchase_orders}")
    warnings: list[str] = []
    for name, rows in records.items():
        if not rows:
            warnings.append(f"empty record set: {name}")
    return warnings


def insufficient_record_sets(records: dict[str, tuple[dict[str, str], ...]]) -> tuple[str, ...]:
    return tuple(sorted(name for name in REQUIRED_RECORD_SETS if not records.get(name)))
