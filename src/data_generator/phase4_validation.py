"""Release-specific Phase 4A–4G validation helpers."""

from __future__ import annotations

import math
from collections import defaultdict
from decimal import Decimal
from typing import Any


class Phase4ValidationError(ValueError):
    """Raised when a Phase 4 release invariant fails."""


def _ids(rows: list[dict[str, Any]]) -> set[str]:
    return {str(row["id"]) for row in rows if row.get("id")}


def validate_master_release(master: dict[str, list[dict[str, Any]]]) -> None:
    required = {
        "warehouses",
        "facilities",
        "transfer_lanes",
        "suppliers",
        "components",
        "supplier_component_agreements",
        "products",
        "bom_versions",
        "bom_lines",
        "customers",
        "sla_policies",
    }
    missing = required - set(master)
    if missing:
        raise Phase4ValidationError(f"missing master files: {sorted(missing)}")
    for entity, rows in master.items():
        ids = _ids(rows)
        if len(ids) != len(rows):
            raise Phase4ValidationError(f"duplicate IDs in {entity}")
    warehouse_ids = _ids(master["warehouses"])
    facility_ids = _ids(master["facilities"])
    supplier_ids = _ids(master["suppliers"])
    component_ids = _ids(master["components"])
    product_ids = _ids(master["products"])
    bom_ids = _ids(master["bom_versions"])
    sla_ids = _ids(master["sla_policies"])
    if not {"WH-PUNE", "WH-CHENNAI", "WH-GURUGRAM"}.issubset(warehouse_ids):
        raise Phase4ValidationError("required Phase 4 warehouses are missing")
    if not {"FAC-PUNE", "FAC-CHENNAI"}.issubset(facility_ids):
        raise Phase4ValidationError("required Phase 4 facilities are missing")
    for row in master["facilities"]:
        if not row.get("source_warehouse_id") in warehouse_ids:
            raise Phase4ValidationError(f"facility has unknown source warehouse: {row['id']}")
    for row in master["warehouse_facility_links"]:
        if row["warehouse_id"] not in warehouse_ids or row["facility_id"] not in facility_ids:
            raise Phase4ValidationError(f"invalid warehouse facility link: {row['id']}")
    for row in master["supplier_component_agreements"]:
        if row["supplier_id"] not in supplier_ids or row["component_id"] not in component_ids:
            raise Phase4ValidationError(f"invalid supplier agreement: {row['id']}")
    for row in master["products"]:
        product_boms = [
            bom for bom in master["bom_versions"] if bom["product_id"] == row["id"]
        ]
        active = [bom for bom in product_boms if bom["status"] == "ACTIVE"]
        if len(active) != 1:
            raise Phase4ValidationError(f"product active BOM count is not one: {row['id']}")
        lines = [
            line for line in master["bom_lines"] if line["bom_version_id"] == active[0]["id"]
        ]
        if len(lines) < 3:
            raise Phase4ValidationError(f"active BOM has fewer than three lines: {row['id']}")
    for row in master["bom_lines"]:
        if row["bom_version_id"] not in bom_ids or row["component_id"] not in component_ids:
            raise Phase4ValidationError(f"invalid BOM line: {row['id']}")
    for row in master["customers"]:
        if row["default_sla_policy_id"] not in sla_ids:
            raise Phase4ValidationError(f"customer has unknown SLA: {row['id']}")


def validate_procurement(
    purchase_orders: list[dict[str, Any]],
    status_history: list[dict[str, Any]],
    receipts: list[dict[str, Any]],
    capacity: list[dict[str, Any]],
) -> None:
    allowed_states = {
        "DRAFT",
        "CONFIRMED",
        "IN_TRANSIT",
        "PARTIALLY_RECEIVED",
        "RECEIVED",
        "DELAYED",
        "CANCELLED",
    }
    po_ids = _ids(purchase_orders)
    receipt_totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for receipt in receipts:
        if receipt["purchase_order_id"] not in po_ids:
            raise Phase4ValidationError(f"receipt references unknown PO: {receipt['id']}")
        receipt_totals[receipt["purchase_order_id"]] += Decimal(str(receipt["quantity"]))
    for order in purchase_orders:
        ordered = Decimal(str(order["ordered_quantity"]))
        received = Decimal(str(order["received_quantity"]))
        if ordered <= 0 or received < 0 or received > ordered:
            raise Phase4ValidationError(f"invalid PO quantities: {order['id']}")
        if received != receipt_totals[order["id"]]:
            raise Phase4ValidationError(f"receipt total mismatch: {order['id']}")
        if order["status"] not in allowed_states:
            raise Phase4ValidationError(f"invalid PO status: {order['id']}")
        if Decimal(str(order["outstanding_quantity"])) != ordered - received:
            raise Phase4ValidationError(f"outstanding quantity mismatch: {order['id']}")
    known_states = {row["status"] for row in status_history}
    if not known_states.issubset(allowed_states):
        raise Phase4ValidationError("status history contains an invalid state")
    capacity_by_key: dict[tuple[str, str], Decimal] = defaultdict(lambda: Decimal("0"))
    for row in capacity:
        capacity_by_key[(row["supplier_id"], row["component_id"])] += Decimal(
            str(row["available_capacity"])
        )
    for order in purchase_orders:
        key = (order["supplier_id"], order["component_id"])
        if Decimal(str(order["ordered_quantity"])) > capacity_by_key[key]:
            raise Phase4ValidationError(f"supplier capacity exceeded: {order['id']}")


def validate_capacity(
    batches: list[dict[str, Any]],
    capacity_calendar: list[dict[str, Any]],
) -> None:
    allocated: dict[tuple[str, str], Decimal] = defaultdict(lambda: Decimal("0"))
    effective: dict[tuple[str, str], Decimal] = {}
    for row in capacity_calendar:
        key = (row["facility_id"], row["capacity_date"])
        effective[key] = Decimal(str(row["effective_capacity"]))
    for batch in batches:
        key = (batch["facility_id"], batch["batch_date"])
        allocated[key] += Decimal(str(batch["quantity"]))
    for key, quantity in allocated.items():
        if quantity > effective.get(key, Decimal("0")):
            raise Phase4ValidationError(f"facility capacity exceeded: {key}")


def validate_nonnegative(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    for row in rows:
        for field in fields:
            if field in row and not math.isfinite(float(row[field])):
                raise Phase4ValidationError(f"non-finite value: {row.get('id', field)}")
