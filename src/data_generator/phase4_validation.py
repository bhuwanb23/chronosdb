"""Release-specific Phase 4A–4G validation helpers."""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import Any


class Phase4ValidationError(ValueError):
    """Raised when a Phase 4 release invariant fails."""


def _ids(rows: list[dict[str, Any]]) -> set[str]:
    return {str(row["id"]) for row in rows if row.get("id")}


def validate_master_release(
    master: dict[str, list[dict[str, Any]]],
    require_full_network: bool = True,
) -> None:
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
    bom_ids = _ids(master["bom_versions"])
    sla_ids = _ids(master["sla_policies"])
    if require_full_network and not {
        "WH-PUNE",
        "WH-CHENNAI",
        "WH-GURUGRAM",
    }.issubset(warehouse_ids):
        raise Phase4ValidationError("required Phase 4 warehouses are missing")
    if require_full_network and not {"FAC-PUNE", "FAC-CHENNAI"}.issubset(facility_ids):
        raise Phase4ValidationError("required Phase 4 facilities are missing")
    for row in master["facilities"]:
        if row.get("source_warehouse_id") not in warehouse_ids:
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


def validate_inventory_release(inventory: dict[str, list[dict[str, Any]]]) -> None:
    opening = inventory["opening"]
    transactions = inventory["transactions"]
    snapshots = inventory["snapshots"]
    opening_keys = {
        (row["warehouse_id"], row["component_id"]) for row in opening
    }
    if not opening_keys:
        raise Phase4ValidationError("inventory has no opening balances")
    transfer_ids: dict[str, set[str]] = defaultdict(set)
    for row in inventory["transfer_transactions"]:
        transfer_ids[row["transfer_id"]].add(row["transaction_type"])
    if any(states != {"TRANSFER_DISPATCH", "TRANSFER_RECEIPT"} for states in transfer_ids.values()):
        raise Phase4ValidationError("transfer dispatch/receipt pairing is incomplete")
    signs = {
        "OPENING_BALANCE": 1,
        "PURCHASE_RECEIPT": 1,
        "PRODUCTION_ISSUE": -1,
        "TRANSFER_DISPATCH": -1,
        "TRANSFER_RECEIPT": 1,
    }
    for row in snapshots:
        key = (row["warehouse_id"], row["component_id"])
        if key not in opening_keys:
            raise Phase4ValidationError(f"snapshot has no opening balance: {row['id']}")
        snapshot_time = datetime.fromisoformat(row["snapshot_time"].replace("Z", "+00:00"))
        expected = sum(
            Decimal(str(transaction["quantity"])) * signs[transaction["transaction_type"]]
            for transaction in transactions
            if (
                transaction["warehouse_id"],
                transaction["component_id"],
            ) == key
            and datetime.fromisoformat(transaction["event_time"].replace("Z", "+00:00"))
            <= snapshot_time
            and transaction["transaction_type"] in signs
        )
        if Decimal(str(row["on_hand_quantity"])) != expected:
            raise Phase4ValidationError(f"snapshot replay mismatch: {row['id']}")
        available = max(
            Decimal("0"),
            expected
            - Decimal(str(row["reserved_quantity"]))
            - Decimal(str(row["quarantined_quantity"])),
        )
        if Decimal(str(row["available_quantity"])) != available:
            raise Phase4ValidationError(f"available quantity mismatch: {row['id']}")
        transferable = max(
            Decimal("0"),
            available - Decimal(str(row["safety_stock_quantity"])),
        )
        if Decimal(str(row["transferable_quantity"])) != transferable:
            raise Phase4ValidationError(f"transferable quantity mismatch: {row['id']}")


def validate_manufacturing_release(
    production_orders: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    batches: list[dict[str, Any]],
    allocations: list[dict[str, Any]],
) -> None:
    order_ids = _ids(production_orders)
    for order in production_orders:
        planned = Decimal(str(order["planned_quantity"]))
        completed = Decimal(str(order["completed_quantity"]))
        if completed < 0 or completed > planned:
            raise Phase4ValidationError(f"production quantity bounds: {order['id']}")
    for requirement in requirements:
        if requirement["production_order_id"] not in order_ids:
            raise Phase4ValidationError(f"unknown material requirement: {requirement['id']}")
        remaining = Decimal(str(requirement["remaining_quantity"]))
        bom_quantity = Decimal(str(requirement["bom_quantity"]))
        scrap = Decimal(str(requirement["scrap_factor"]))
        expected = Decimal(str(math.ceil(remaining * bom_quantity * (1 + scrap))))
        if Decimal(str(requirement["required_quantity"])) != expected:
            raise Phase4ValidationError(
                f"material requirement formula mismatch: {requirement['id']}"
            )
    for batch in batches:
        expected = Decimal(str(batch["quantity"])) * Decimal("2")
        if batch["status"] == "RELEASED" and Decimal(str(batch["material_quantity"])) != expected:
            raise Phase4ValidationError(f"batch material mismatch: {batch['id']}")
    for allocation in allocations:
        if allocation["production_order_id"] not in order_ids:
            raise Phase4ValidationError(f"unknown production allocation: {allocation['id']}")


def validate_nonnegative(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    for row in rows:
        for field in fields:
            if field in row and not math.isfinite(float(row[field])):
                raise Phase4ValidationError(f"non-finite value: {row.get('id', field)}")
