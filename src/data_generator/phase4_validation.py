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


def _delay_hours(promised: str, projected: str) -> int:
    promised_time = datetime.fromisoformat(promised.replace("Z", "+00:00"))
    projected_time = datetime.fromisoformat(projected.replace("Z", "+00:00"))
    return max(0, int((projected_time - promised_time).total_seconds() // 3600))


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
    opening_quantities = {
        (row["warehouse_id"], row["component_id"]): Decimal(str(row["on_hand_quantity"]))
        for row in opening
    }
    if not opening_keys:
        raise Phase4ValidationError("inventory has no opening balances")
    signs = {
        "OPENING_BALANCE": 1,
        "PURCHASE_RECEIPT": 1,
        "PRODUCTION_ISSUE": -1,
        "TRANSFER_DISPATCH": -1,
        "TRANSFER_RECEIPT": 1,
    }
    unknown_types = {
        row["transaction_type"] for row in transactions
    } - set(signs)
    if unknown_types:
        raise Phase4ValidationError(f"unknown inventory transaction type: {sorted(unknown_types)}")
    if any(Decimal(str(row["quantity"])) < 0 for row in transactions):
        raise Phase4ValidationError("inventory transaction quantity must be non-negative")
    transfer_ids: dict[str, set[str]] = defaultdict(set)
    for row in inventory["transfer_transactions"]:
        transfer_ids[row["transfer_id"]].add(row["transaction_type"])
    if any(states != {"TRANSFER_DISPATCH", "TRANSFER_RECEIPT"} for states in transfer_ids.values()):
        raise Phase4ValidationError("transfer dispatch/receipt pairing is incomplete")
    transactions_by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for transaction in transactions:
        key = (transaction["warehouse_id"], transaction["component_id"])
        if key not in opening_keys:
            raise Phase4ValidationError(f"transaction has no opening balance: {transaction['id']}")
        transactions_by_key[key].append(transaction)
    for rows in transactions_by_key.values():
        rows.sort(key=lambda row: (row["event_time"], row["id"]))
    reservation_by_key: dict[tuple[str, str], Decimal] = defaultdict(lambda: Decimal("0"))
    for reservation in inventory["reservations"]:
        key = (reservation["warehouse_id"], reservation["component_id"])
        if key not in opening_keys:
            raise Phase4ValidationError(f"reservation has no opening balance: {reservation['id']}")
        quantity = Decimal(str(reservation["reserved_quantity"]))
        if quantity < 0:
            raise Phase4ValidationError(f"negative reservation: {reservation['id']}")
        reservation_by_key[key] += quantity
    for transfer in inventory["transfer_transactions"]:
        quantity = Decimal(str(transfer["quantity"]))
        if quantity <= 0:
            raise Phase4ValidationError(f"invalid transfer quantity: {transfer['id']}")
        source_key = (transfer["source_warehouse_id"], transfer["component_id"])
        if source_key not in opening_keys:
            raise Phase4ValidationError(f"transfer has no source opening balance: {transfer['id']}")
        if transfer["transaction_type"] == "TRANSFER_DISPATCH":
            event_time = datetime.fromisoformat(transfer["event_time"].replace("Z", "+00:00"))
            on_hand = Decimal("0")
            for transaction in transactions_by_key[source_key]:
                transaction_time = datetime.fromisoformat(
                    transaction["event_time"].replace("Z", "+00:00")
                )
                if transaction_time >= event_time:
                    break
                on_hand += (
                    Decimal(str(transaction["quantity"]))
                    * signs[transaction["transaction_type"]]
                )
            if quantity > on_hand - reservation_by_key[source_key]:
                raise Phase4ValidationError(
                    f"transfer exceeds available quantity: {transfer['id']}"
                )
    golden_snapshot = None
    for row in sorted(
        snapshots,
        key=lambda item: (item["warehouse_id"], item["component_id"], item["snapshot_time"]),
    ):
        key = (row["warehouse_id"], row["component_id"])
        if key not in opening_keys:
            raise Phase4ValidationError(f"snapshot has no opening balance: {row['id']}")
        snapshot_time = datetime.fromisoformat(row["snapshot_time"].replace("Z", "+00:00"))
        expected = Decimal("0")
        for transaction in transactions_by_key[key]:
            transaction_time = datetime.fromisoformat(
                transaction["event_time"].replace("Z", "+00:00")
            )
            if transaction_time > snapshot_time:
                break
            expected += (
                Decimal(str(transaction["quantity"]))
                * signs[transaction["transaction_type"]]
            )
        if Decimal(str(row["on_hand_quantity"])) != expected:
            raise Phase4ValidationError(f"snapshot replay mismatch: {row['id']}")
        if (
            row["snapshot_time"] == "2026-11-11T02:30:00Z"
            and Decimal(str(row["on_hand_quantity"])) != opening_quantities[key]
        ):
            raise Phase4ValidationError(f"opening balance boundary mismatch: {row['id']}")
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
        if (
            row["warehouse_id"],
            row["component_id"],
            row["snapshot_time"],
        ) == ("WH-CHENNAI", "CMP-MCU-42", "2026-11-11T02:30:00Z"):
            golden_snapshot = row
    if (
        golden_snapshot is None
        or Decimal(str(golden_snapshot["transferable_quantity"])) != Decimal("400")
    ):
        raise Phase4ValidationError("golden transferable quantity must remain 400")


def validate_manufacturing_release(
    production_orders: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    batches: list[dict[str, Any]],
    allocations: list[dict[str, Any]],
    master: dict[str, list[dict[str, Any]]] | None = None,
) -> None:
    order_ids = _ids(production_orders)
    orders_by_id = {row["id"]: row for row in production_orders}
    active_boms = {
        row["product_id"]: row
        for row in (master or {}).get("bom_versions", [])
        if row["status"] == "ACTIVE"
    }
    bom_lines = (master or {}).get("bom_lines", [])
    expected_requirement_keys: set[tuple[str, str]] = set()
    for order in production_orders:
        planned = Decimal(str(order["planned_quantity"]))
        completed = Decimal(str(order["completed_quantity"]))
        if completed < 0 or completed > planned:
            raise Phase4ValidationError(f"production quantity bounds: {order['id']}")
        if master is not None:
            if order["product_id"] not in _ids(master["products"]):
                raise Phase4ValidationError(f"unknown production product: {order['id']}")
            if order["facility_id"] not in _ids(master["facilities"]):
                raise Phase4ValidationError(f"unknown production facility: {order['id']}")
            bom = active_boms.get(order["product_id"])
            if bom is None:
                raise Phase4ValidationError(f"production order has no active BOM: {order['id']}")
            expected_requirement_keys.update(
                (order["id"], line["id"])
                for line in bom_lines
                if line["bom_version_id"] == bom["id"]
            )
    actual_requirement_keys: set[tuple[str, str]] = set()
    for requirement in requirements:
        if requirement["production_order_id"] not in order_ids:
            raise Phase4ValidationError(f"unknown material requirement: {requirement['id']}")
        order = orders_by_id[requirement["production_order_id"]]
        if master is not None:
            key = (requirement["production_order_id"], requirement["bom_line_id"])
            actual_requirement_keys.add(key)
            if requirement["product_id"] != order["product_id"]:
                raise Phase4ValidationError(f"material product mismatch: {requirement['id']}")
            bom = active_boms.get(order["product_id"])
            if bom is None:
                raise Phase4ValidationError(
                    f"material requirement has no active BOM: {requirement['id']}"
                )
            line = next(
                (
                    candidate
                    for candidate in bom_lines
                    if candidate["id"] == requirement["bom_line_id"]
                    and candidate["bom_version_id"] == bom["id"]
                ),
                None,
            )
            if line is None or line["component_id"] != requirement["component_id"]:
                raise Phase4ValidationError(
                    f"material component is outside active BOM: {requirement['id']}"
                )
        remaining = Decimal(str(requirement["remaining_quantity"]))
        bom_quantity = Decimal(str(requirement["bom_quantity"]))
        scrap = Decimal(str(requirement["scrap_factor"]))
        expected = Decimal(str(math.ceil(remaining * bom_quantity * (1 + scrap))))
        if Decimal(str(requirement["required_quantity"])) != expected:
            raise Phase4ValidationError(
                f"material requirement formula mismatch: {requirement['id']}"
            )
    if master is not None and actual_requirement_keys != expected_requirement_keys:
        raise Phase4ValidationError("material requirements do not match active BOM lines")
    for batch in batches:
        if batch["production_order_id"] not in order_ids:
            raise Phase4ValidationError(f"unknown production batch: {batch['id']}")
        if master is not None:
            order = orders_by_id[batch["production_order_id"]]
            if batch["product_id"] != order["product_id"]:
                raise Phase4ValidationError(f"batch product mismatch: {batch['id']}")
            if batch["facility_id"] != order["facility_id"]:
                raise Phase4ValidationError(f"batch facility mismatch: {batch['id']}")
            matching = [
                requirement for requirement in requirements
                if requirement["production_order_id"] == batch["production_order_id"]
                and requirement["component_id"] == batch["component_id"]
            ]
            if not matching:
                raise Phase4ValidationError(f"batch component is outside active BOM: {batch['id']}")
            if batch["component_id"] not in _ids(master["components"]):
                raise Phase4ValidationError(f"unknown batch component: {batch['id']}")
        bom_quantity = Decimal(str(batch.get("bom_quantity", "2")))
        scrap_factor = Decimal(str(batch.get("scrap_factor", "0")))
        expected = Decimal(str(batch["quantity"])) * bom_quantity * (Decimal("1") + scrap_factor)
        if batch["status"] == "RELEASED" and Decimal(str(batch["material_quantity"])) != expected:
            raise Phase4ValidationError(f"batch material mismatch: {batch['id']}")
    for allocation in allocations:
        if allocation["production_order_id"] not in order_ids:
            raise Phase4ValidationError(f"unknown production allocation: {allocation['id']}")
        if Decimal(str(allocation["allocated_quantity"])) < 0:
            raise Phase4ValidationError(f"negative production allocation: {allocation['id']}")
        if master is not None:
            order = orders_by_id[allocation["production_order_id"]]
            if allocation["product_id"] != order["product_id"]:
                raise Phase4ValidationError(f"allocation product mismatch: {allocation['id']}")
            if not any(
                requirement["production_order_id"] == allocation["production_order_id"]
                and requirement["component_id"] == allocation["component_id"]
                for requirement in requirements
            ):
                raise Phase4ValidationError(
                    f"allocation component is outside active BOM: {allocation['id']}"
                )


def validate_nonnegative(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    for row in rows:
        for field in fields:
            if field in row and not math.isfinite(float(row[field])):
                raise Phase4ValidationError(f"non-finite value: {row.get('id', field)}")


def validate_demand_release(
    demand: dict[str, list[dict[str, Any]]],
    master: dict[str, list[dict[str, Any]]],
    production_orders: list[dict[str, Any]],
) -> None:
    """Validate customer joins, allocation precedence outputs, SLA, and revenue."""
    orders = demand["orders"]
    lines = demand["lines"]
    allocations = demand["allocations"]
    sla_assignments = demand["sla_assignments"]
    order_ids = {row["customer_order_id"] for row in orders}
    line_by_id = {row["customer_order_line_id"]: row for row in lines}
    product_ids = _ids(master["products"])
    production_ids = _ids(production_orders)
    if len(order_ids) != len(orders) or len(line_by_id) != len(lines):
        raise Phase4ValidationError("duplicate customer demand identifiers")
    for order in orders:
        if order["customer_id"] not in _ids(master["customers"]):
            raise Phase4ValidationError(f"unknown demand customer: {order['customer_order_id']}")
    for line in lines:
        if line["customer_order_id"] not in order_ids:
            raise Phase4ValidationError(f"unknown demand order: {line['customer_order_line_id']}")
        if line["product_id"] not in product_ids:
            raise Phase4ValidationError(f"unknown demand product: {line['customer_order_line_id']}")
        if line["assigned_production_order_id"] not in production_ids:
            raise Phase4ValidationError(
                f"unknown demand production: {line['customer_order_line_id']}"
            )
        ordered = Decimal(str(line["ordered_quantity"]))
        unit_revenue = Decimal(str(line["unit_revenue"]))
        if ordered <= 0 or unit_revenue <= 0:
            raise Phase4ValidationError(
                f"invalid demand quantity or revenue: {line['customer_order_line_id']}"
            )
        if Decimal(str(line["line_revenue"])) != ordered * unit_revenue:
            raise Phase4ValidationError(
                f"demand revenue mismatch: {line['customer_order_line_id']}"
            )
    allocated_lines = {row["customer_order_line_id"] for row in allocations}
    if allocated_lines != set(line_by_id):
        raise Phase4ValidationError("customer demand allocation coverage mismatch")
    for allocation in allocations:
        line = line_by_id.get(allocation["customer_order_line_id"])
        if (
            line is None
            or allocation["production_order_id"] != line["assigned_production_order_id"]
        ):
            raise Phase4ValidationError(f"demand allocation join mismatch: {allocation['id']}")
        if Decimal(str(allocation["allocated_quantity"])) != Decimal(str(line["ordered_quantity"])):
            raise Phase4ValidationError(f"demand allocation quantity mismatch: {allocation['id']}")
    sla_by_line = {row["customer_order_line_id"]: row for row in sla_assignments}
    if set(sla_by_line) != set(line_by_id):
        raise Phase4ValidationError("SLA assignment coverage mismatch")
    for assignment in sla_assignments:
        line = line_by_id[assignment["customer_order_line_id"]]
        ordered = Decimal(str(line["ordered_quantity"]))
        on_time = Decimal(str(assignment["projected_on_time_quantity"]))
        late = Decimal(str(assignment["projected_late_quantity"]))
        expected_delay = _delay_hours(
            assignment["promised_delivery_time"],
            assignment["projected_delivery_time"],
        )
        if on_time + late != ordered or int(assignment["delay_hours"]) != expected_delay:
            raise Phase4ValidationError(f"SLA quantity or delay mismatch: {assignment['id']}")
        expected_risk = late * Decimal(str(line["unit_revenue"]))
        if Decimal(str(assignment["revenue_at_risk"])) != expected_risk:
            raise Phase4ValidationError(f"SLA revenue risk mismatch: {assignment['id']}")
    golden = {
        row["customer_order_line_id"]: row
        for row in sla_assignments
        if row["customer_order_line_id"] in {"COL-CO-0701-01", "COL-CO-0704-01", "COL-CO-0711-01"}
    }
    if len(golden) != 3 or sum(
        Decimal(str(row["revenue_at_risk"])) for row in golden.values()
    ) != Decimal("1600000"):
        raise Phase4ValidationError("golden customer demand outcome mismatch")


def validate_history_release(
    history: dict[str, Any],
    inventory: dict[str, list[dict[str, Any]]],
) -> None:
    """Validate temporal intervals, late-arriving semantics, and ledger checkpoints."""
    for version in history["entity_versions"]:
        start = datetime.fromisoformat(version["effective_from"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(version["effective_to"].replace("Z", "+00:00"))
        if start >= end:
            raise Phase4ValidationError(f"invalid temporal interval: {version['id']}")
    late_records = history["late_arriving_records"]
    if not late_records:
        raise Phase4ValidationError("history has no late-arriving record")
    for record in late_records:
        if record["visible_before_ingested"] != "false" or record["visible_after_ingested"] != "true":
            raise Phase4ValidationError(f"invalid late-arrival visibility: {record['id']}")
        if record["completed_scenario_immutable"] != "true":
            raise Phase4ValidationError(f"completed scenario is mutable: {record['id']}")
    checkpoints = history["historical_inventory_checkpoints"]
    if len(checkpoints) < 10:
        raise Phase4ValidationError("history requires at least ten checkpoints")
    for checkpoint in checkpoints:
        cutoff = datetime.fromisoformat(checkpoint["checkpoint_time"].replace("Z", "+00:00"))
        expected = Decimal("0")
        for transaction in inventory["transactions"]:
            if (
                transaction["warehouse_id"] == checkpoint["warehouse_id"]
                and transaction["component_id"] == checkpoint["component_id"]
                and datetime.fromisoformat(transaction["event_time"].replace("Z", "+00:00"))
                <= cutoff
            ):
                expected += Decimal(str(transaction["quantity"])) * {
                    "OPENING_BALANCE": Decimal("1"),
                    "PURCHASE_RECEIPT": Decimal("1"),
                    "PRODUCTION_ISSUE": Decimal("-1"),
                    "TRANSFER_DISPATCH": Decimal("-1"),
                    "TRANSFER_RECEIPT": Decimal("1"),
                }[transaction["transaction_type"]]
        if Decimal(str(checkpoint["expected_on_hand_quantity"])) != expected:
            raise Phase4ValidationError(f"history checkpoint mismatch: {checkpoint['id']}")
