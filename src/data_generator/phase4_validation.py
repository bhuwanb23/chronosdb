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
    capacity_by_window: dict[tuple[str, str, str], Decimal] = defaultdict(
        lambda: Decimal("0")
    )
    for row in capacity:
        available = Decimal(str(row["effective_capacity"])) - Decimal(
            str(row.get("reserved_capacity", "0"))
        )
        if available < 0:
            raise Phase4ValidationError(
                f"supplier capacity reservation exceeds window: {row['id']}"
            )
        capacity_window = row.get("capacity_date") or row.get("effective_from")
        capacity_by_window[
            (row["supplier_id"], row["component_id"], str(capacity_window)[:10])
        ] += available
    allocated_by_window: dict[tuple[str, str, str], Decimal] = defaultdict(
        lambda: Decimal("0")
    )
    for order in sorted(purchase_orders, key=lambda row: row["id"]):
        key = (order["supplier_id"], order["component_id"])
        expected_date = str(order["expected_arrival_time"])[:10]
        windows = sorted(
            window
            for supplier, component, window in capacity_by_window
            if supplier == key[0] and component == key[1] and window <= expected_date
        )
        if not windows:
            all_windows = [
                window
                for supplier, component, window in capacity_by_window
                if supplier == key[0] and component == key[1]
            ]
            if all_windows and expected_date < min(all_windows):
                if (
                    order["status"] != "RECEIVED"
                    or not order.get("actual_arrival_time")
                    or str(order["actual_arrival_time"])[:10] >= min(all_windows)
                ):
                    raise Phase4ValidationError(
                        f"historical supplier capacity exemption is not proven: {order['id']}"
                    )
                continue
            raise Phase4ValidationError(
                f"supplier capacity window missing: {order['id']}"
            )
        remaining = Decimal(str(order["ordered_quantity"]))
        for window in windows:
            window_key = (key[0], key[1], window)
            available = capacity_by_window[window_key] - allocated_by_window[window_key]
            allocation = min(remaining, available)
            allocated_by_window[window_key] += allocation
            remaining -= allocation
            if remaining <= 0:
                break
        if remaining > 0:
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
    production_by_id = {row["id"]: row for row in production_orders}
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
        if (
            production_by_id[line["assigned_production_order_id"]]["product_id"]
            != line["product_id"]
        ):
            raise Phase4ValidationError(
                f"demand product allocation mismatch: {line['customer_order_line_id']}"
            )
        ordered = Decimal(str(line["ordered_quantity"]))
        fulfilled = Decimal(str(line["fulfilled_quantity"]))
        unit_revenue = Decimal(str(line["unit_revenue"]))
        if ordered <= 0 or fulfilled < 0 or fulfilled > ordered or unit_revenue <= 0:
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
        allocation_line = line_by_id.get(allocation["customer_order_line_id"])
        if (
            allocation_line is None
            or allocation["production_order_id"]
            != allocation_line["assigned_production_order_id"]
        ):
            raise Phase4ValidationError(f"demand allocation join mismatch: {allocation['id']}")
        if Decimal(str(allocation["allocated_quantity"])) != Decimal(
            str(allocation_line["ordered_quantity"])
        ):
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
    if not any(row["status"] == "PARTIALLY_FULFILLED" for row in orders):
        raise Phase4ValidationError("demand lacks partial fulfilment coverage")
    if not any(
        row["projection_context"] == "INTERVENTION_PROTECTED"
        for row in sla_assignments
    ) or not any(
        row["projection_context"] == "RESCHEDULING_HARM"
        for row in sla_assignments
    ):
        raise Phase4ValidationError("demand lacks intervention impact examples")


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
        if (
            record["visible_before_ingested"] != "false"
            or record["visible_after_ingested"] != "true"
        ):
            raise Phase4ValidationError(f"invalid late-arrival visibility: {record['id']}")
        if record["completed_scenario_immutable"] != "true":
            raise Phase4ValidationError(f"completed scenario is mutable: {record['id']}")
    checkpoints = history["historical_inventory_checkpoints"]
    if len(checkpoints) < 10:
        raise Phase4ValidationError("history requires at least ten checkpoints")
    replay_inputs = history["replay_input_events"]
    for checkpoint in checkpoints:
        cutoff = datetime.fromisoformat(checkpoint["checkpoint_time"].replace("Z", "+00:00"))
        expected = Decimal("0")
        for transaction in replay_inputs:
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
    if not inventory["transactions"]:
        raise Phase4ValidationError("history validation requires release ledger context")


def validate_disruptions_release(
    disruptions: dict[str, list[dict[str, Any]]],
    purchase_orders: list[dict[str, Any]],
) -> None:
    """Validate event intervals and supplier/component/PO scope joins."""
    events = disruptions["events"]
    event_ids = _ids(
        [{"id": row["disruption_event_id"]} for row in events]
    )
    allowed_types = {
        "SUPPLIER_OUTAGE",
        "PARTIAL_SUPPLY_INTERRUPTION",
        "SHIPMENT_DELAY",
        "QUALITY_HOLD",
    }
    if len(event_ids) != len(events) or not events:
        raise Phase4ValidationError("disruption event identifiers are invalid")
    po_by_id = {row["id"]: row for row in purchase_orders}
    for event in events:
        if event["event_type"] not in allowed_types:
            raise Phase4ValidationError(f"unknown disruption type: {event['disruption_event_id']}")
        start = datetime.fromisoformat(event["start_time"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(event["expected_end_time"].replace("Z", "+00:00"))
        if start >= end or int(event["recovery_lag_hours"]) < 0:
            raise Phase4ValidationError(
                f"invalid disruption interval: {event['disruption_event_id']}"
            )
    for scope in disruptions["scope_purchase_orders"]:
        order = po_by_id.get(scope["purchase_order_id"])
        if order is None:
            raise Phase4ValidationError(f"unknown disrupted PO: {scope['id']}")
        event = next(
            row
            for row in events
            if row["disruption_event_id"] == scope["disruption_event_id"]
        )
        if order["supplier_id"] != event["supplier_id"]:
            raise Phase4ValidationError(f"disruption supplier scope mismatch: {scope['id']}")
    golden = next(
        (row for row in events if row["disruption_event_id"] == "EVT-GOLD-001"),
        None,
    )
    if golden is None or golden["supplier_id"] != "SUP-0104":
        raise Phase4ValidationError("golden disruption is missing")
    if golden["expected_end_time"] != "2026-11-25T02:30:00Z":
        raise Phase4ValidationError("golden disruption end time mismatch")
    if golden["projected_arrival_time"] != "2026-11-27T02:30:00Z":
        raise Phase4ValidationError("golden disruption recovery mismatch")
    if not any(
        row["disruption_event_id"] == "EVT-GOLD-001"
        and row["purchase_order_id"] == "PO-2208"
        for row in disruptions["scope_purchase_orders"]
    ):
        raise Phase4ValidationError("golden disruption PO scope is missing")


def validate_interventions_release(
    interventions: dict[str, list[dict[str, Any]]],
) -> None:
    """Validate feasibility boundaries and golden intervention arithmetic."""
    transfers = {row["id"]: row for row in interventions["transfers"]}
    golden_transfer = transfers.get("INT-GOLD-A")
    if golden_transfer is None or golden_transfer["feasibility_status"] != "FEASIBLE":
        raise Phase4ValidationError("golden transfer capability is missing")
    if (
        golden_transfer["source_warehouse_id"],
        golden_transfer["destination_warehouse_id"],
        golden_transfer["component_id"],
        golden_transfer["requested_quantity"],
    ) != ("WH-CHENNAI", "WH-PUNE", "CMP-MCU-42", "400"):
        raise Phase4ValidationError("golden transfer coordinates mismatch")
    constrained_transfer = transfers.get("INT-GOLD-TRANSFER-500")
    if (
        constrained_transfer is None
        or constrained_transfer["feasibility_status"] != "INFEASIBLE"
        or constrained_transfer["rejection_reason"] != "SOURCE_SAFETY_STOCK_VIOLATION"
    ):
        raise Phase4ValidationError("infeasible transfer guard is missing")
    alternate = next(
        (row for row in interventions["alternates"] if row["id"] == "INT-GOLD-B"),
        None,
    )
    if alternate is None or alternate["incremental_premium_inr"] != "72000":
        raise Phase4ValidationError("golden alternate supply mismatch")
    expedite = next(
        (row for row in interventions["expedites"] if row["id"] == "INT-GOLD-EXPEDITE"),
        None,
    )
    if expedite is None or expedite["eligible"] != "false":
        raise Phase4ValidationError("outage-incompatible expedite was not rejected")
    costs = {row["candidate_id"]: row for row in interventions["costs"]}
    if costs.get("INT-GOLD-C", {}).get("total_cost_inr") != "132000":
        raise Phase4ValidationError("golden hybrid cost mismatch")
    for row in interventions["costs"]:
        expected = (
            Decimal(str(row["fixed_cost_inr"]))
            + Decimal(str(row["variable_cost_inr"]))
        )
        if Decimal(str(row["total_cost_inr"])) != expected:
            raise Phase4ValidationError(f"intervention cost mismatch: {row['id']}")


def validate_evidence_release(evidence: dict[str, Any]) -> None:
    """Validate evidence counts, metadata completeness, and answer isolation."""
    documents = evidence["documents"]
    expected_counts = {
        "supplier_notices": 60,
        "incident_reports": 60,
        "procedures": 15,
        "policies": 10,
        "recovery_summaries": 30,
    }
    counts: dict[str, int] = defaultdict(int)
    ids: set[str] = set()
    forbidden = (
        "expected_recommendation",
        "revenue_at_risk",
        "ground_truth",
        "SCN-GOLD-001",
        "INT-GOLD",
    )
    for document in documents:
        document_id = document["document_id"]
        if document_id in ids:
            raise Phase4ValidationError(f"duplicate evidence document: {document_id}")
        ids.add(document_id)
        counts[document["document_type"]] += 1
        if document["synthetic_origin"] != "true":
            raise Phase4ValidationError(f"evidence is not marked synthetic: {document_id}")
        if any(token.lower() in document["text"].lower() for token in forbidden):
            raise Phase4ValidationError(f"evidence answer leakage: {document_id}")
    if counts != expected_counts:
        raise Phase4ValidationError(f"evidence class counts mismatch: {dict(counts)}")
    metadata_ids = {row["document_id"] for row in evidence["metadata"]}
    if metadata_ids != ids:
        raise Phase4ValidationError("evidence metadata coverage mismatch")
    if sum(row["status"] == "EXPIRED" for row in documents) < 10:
        raise Phase4ValidationError("evidence lacks expired coverage")
    if sum(row["access_class"] == "UNAUTHORIZED" for row in documents) < 10:
        raise Phase4ValidationError("evidence lacks unauthorized coverage")
    if sum(
        "ignore previous instructions" in row["text"].lower() for row in documents
    ) < 5:
        raise Phase4ValidationError("evidence lacks prompt-injection coverage")


def validate_golden_release(
    golden: dict[str, Any],
    evidence: dict[str, Any] | None = None,
) -> None:
    """Validate the independently frozen golden headline and timeline."""
    candidates = {
        row["candidate_id"]: row for row in golden["expected_candidate_results"]
    }
    required = {
        "DO-NOTHING",
        "INT-GOLD-A",
        "INT-GOLD-B",
        "INT-GOLD-C",
        "INT-GOLD-EXPEDITE",
        "INT-GOLD-RESCHEDULE",
        "INT-GOLD-TRANSFER-500",
    }
    if set(candidates) != required:
        raise Phase4ValidationError("golden candidate set mismatch")
    do_nothing = candidates["DO-NOTHING"]
    hybrid = candidates["INT-GOLD-C"]
    if (
        do_nothing["sla_breach_count"] != 2
        or do_nothing["revenue_at_risk"] != "1600000.00"
        or hybrid["intervention_cost"] != "132000"
        or hybrid["sla_breach_count"] != 0
        or hybrid["revenue_at_risk"] != "0.00"
        or hybrid["revenue_protected"] != "1600000.00"
    ):
        raise Phase4ValidationError("golden headline result mismatch")
    if golden["expected_recommendation"]["recommended_intervention"] != "INT-GOLD-C":
        raise Phase4ValidationError("golden recommendation mismatch")
    if len(golden["expected_timeline"]) < 7 or any(
        not row.get("event_time") for row in golden["expected_timeline"]
    ):
        raise Phase4ValidationError("golden timeline is incomplete")
    issued = sum(
        Decimal(str(row["quantity"]))
        for row in golden["expected_timeline"]
        if row["event_type"] == "BATCH_MATERIAL_ISSUE"
        and row.get("production_order_id") == "MO-0876"
    )
    if issued != Decimal("400"):
        raise Phase4ValidationError("golden material issue total mismatch")
    if golden["state_at_as_of"]["transferable_quantity"] != "400":
        raise Phase4ValidationError("golden state transfer quantity mismatch")
    checks = golden.get("source_derived_checks", {})
    if checks.get("demand_revenue_at_risk") != "1600000":
        raise Phase4ValidationError("golden demand source check mismatch")
    if checks.get("demand_breach_count") != 2:
        raise Phase4ValidationError("golden demand breach source check mismatch")
    if checks.get("hybrid_intervention_cost") != "132000":
        raise Phase4ValidationError("golden intervention source check mismatch")
    if evidence is not None:
        evidence_ids = {row["document_id"] for row in evidence["documents"]}
        for candidate in golden["expected_candidate_results"]:
            if not set(candidate["evidence_references"]) <= evidence_ids:
                raise Phase4ValidationError(
                    f"golden evidence reference mismatch: {candidate['candidate_id']}"
                )


def validate_supporting_demos_release(demos: dict[str, list[dict[str, Any]]]) -> None:
    """Validate the frozen supporting demonstration catalogue."""
    expected = {
        "DEMO-002",
        "DEMO-003",
        "DEMO-004",
        "DEMO-005",
        "DEMO-006",
        "DEMO-007",
    }
    actual = {row["scenario_id"] for row in demos["scenarios"]}
    if actual != expected:
        raise Phase4ValidationError("supporting demo scenario set mismatch")
    by_id = {row["scenario_id"]: row for row in demos["scenarios"]}
    if by_id["DEMO-003"]["expected_outcome"] != "NO_FEASIBLE_INTERVENTION":
        raise Phase4ValidationError("no-feasible demo outcome mismatch")
    if by_id["DEMO-006"]["expected_outcome"] != "INSUFFICIENT_DATA":
        raise Phase4ValidationError("insufficient-data demo outcome mismatch")
    if any(row["test_specific_branch"] != "false" for row in demos["scenarios"]):
        raise Phase4ValidationError("supporting demo contains test-specific branching")
    if any(
        not row["source_record_ids"] or not row["candidate_ids"]
        for row in demos["scenarios"]
    ):
        raise Phase4ValidationError("supporting demo lacks cross-layer references")


def validate_benchmark_release(
    benchmarks: dict[str, Any],
    master: dict[str, list[dict[str, Any]]] | None = None,
    purchase_orders: list[dict[str, Any]] | None = None,
    demand: dict[str, list[dict[str, Any]]] | None = None,
    history: dict[str, Any] | None = None,
    evidence: dict[str, Any] | None = None,
) -> None:
    """Validate the frozen 60-case catalogue, partitions, and balance rules."""
    scenarios = benchmarks["scenarios"]
    expected = benchmarks["expected"]
    if len(scenarios) != 60 or len(expected) != 60:
        raise Phase4ValidationError("benchmark must contain exactly 60 scenarios")
    scenario_ids = {row["scenario_id"] for row in scenarios}
    if len(scenario_ids) != 60 or {
        row["scenario_id"] for row in expected
    } != scenario_ids:
        raise Phase4ValidationError("benchmark scenario identifier mismatch")
    partitions = {
        name: rows
        for name, rows in benchmarks["partition_manifest"][
            "exclusive_partitions"
        ].items()
    }
    if {name: len(rows) for name, rows in partitions.items()} != {
        "development": 24,
        "validation": 12,
        "test": 18,
        "golden": 3,
        "adversarial-only": 3,
    }:
        raise Phase4ValidationError("benchmark partition counts mismatch")
    if len(set().union(*partitions.values())) != 60:
        raise Phase4ValidationError("benchmark partitions overlap")
    category_counts: dict[str, int] = defaultdict(int)
    for scenario in scenarios:
        category_counts[scenario["category"]] += 1
        for field in (
            "reference_supplier_id",
            "reference_component_id",
            "reference_purchase_order_id",
            "reference_customer_order_id",
            "evidence_query_id",
        ):
            if not scenario.get(field):
                raise Phase4ValidationError(
                    f"benchmark reference missing: {scenario['scenario_id']}"
                )
    expected_counts = {
        "FULL_SUPPLIER_OUTAGE": 18,
        "PARTIAL_SUPPLIER_OUTAGE": 8,
        "SELECTED_COMPONENT_OUTAGE": 6,
        "PURCHASE_ORDER_DISRUPTION": 4,
        "INVENTORY_TRANSFER_CONSTRAINT": 4,
        "ALTERNATE_SUPPLIER_CONSTRAINT": 4,
        "BUDGET_CONSTRAINED_RECOVERY": 4,
        "NO_OPERATIONAL_IMPACT": 3,
        "NO_FEASIBLE_INTERVENTION": 3,
        "INSUFFICIENT_CRITICAL_DATA": 3,
        "TIE_OR_PARETO_EQUIVALENT": 3,
    }
    if dict(category_counts) != expected_counts:
        raise Phase4ValidationError("benchmark category distribution mismatch")
    test_ids = set(partitions["test"])
    test_recommendations = {
        row["recommended_intervention"]
        for row in expected
        if row["scenario_id"] in test_ids
    }
    required_interventions = {
        "HYBRID",
        "RESCHEDULE",
        "EXPEDITE",
        "TRANSFER",
        "ALTERNATE_SUPPLY",
    }
    if not required_interventions <= test_recommendations:
        raise Phase4ValidationError("benchmark test set lacks intervention diversity")
    if sum(
        row["recommended_intervention"] == "NO_FEASIBLE_INTERVENTION"
        for row in expected
        if row["scenario_id"] in test_ids
    ) < 3:
        raise Phase4ValidationError("benchmark test set lacks no-feasible cases")
    test_scenarios = [
        row for row in scenarios if row["scenario_id"] in test_ids
    ]
    if sum(row["partial_fulfillment"] for row in test_scenarios) < 5:
        raise Phase4ValidationError("benchmark test set lacks partial fulfilment")
    if sum(
        row["requires_temporal_reconstruction"] for row in test_scenarios
    ) < 5:
        raise Phase4ValidationError("benchmark test set lacks temporal reconstruction")
    if sum(row["has_misleading_evidence"] for row in test_scenarios) < 5:
        raise Phase4ValidationError("benchmark test set lacks misleading evidence")
    if sum(row["multi_product_impact"] for row in scenarios) < 12:
        raise Phase4ValidationError("benchmark lacks multi-product impact coverage")
    if sum(
        row["category"] == "INSUFFICIENT_CRITICAL_DATA" for row in test_scenarios
    ) < 3 or sum(
        row["category"] == "TIE_OR_PARETO_EQUIVALENT" for row in test_scenarios
    ) < 3:
        raise Phase4ValidationError("benchmark test set lacks adversarial balance")
    if any(value is None for value in (master, purchase_orders, demand, history, evidence)):
        return
    assert master is not None
    assert purchase_orders is not None
    assert demand is not None
    assert history is not None
    assert evidence is not None
    supplier_ids = _ids(master["suppliers"])
    component_ids = _ids(master["components"])
    purchase_order_ids = _ids(purchase_orders)
    customer_order_ids = {row["customer_order_id"] for row in demand["orders"]}
    evidence_query_ids = {row["query_id"] for row in evidence["queries"]}
    for scenario in scenarios:
        if (
            scenario["reference_supplier_id"] not in supplier_ids
            or scenario["reference_component_id"] not in component_ids
            or scenario["reference_purchase_order_id"] not in purchase_order_ids
            or scenario["reference_customer_order_id"] not in customer_order_ids
            or scenario["evidence_query_id"] not in evidence_query_ids
        ):
            raise Phase4ValidationError(
                f"benchmark cross-layer reference mismatch: {scenario['scenario_id']}"
            )
    if not history["replay_input_events"]:
        raise Phase4ValidationError("benchmark history references are unavailable")
