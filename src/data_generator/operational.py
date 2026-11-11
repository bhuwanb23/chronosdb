"""Phase 3H operational and transactional data generation."""

from __future__ import annotations

import math
import random
from datetime import UTC, datetime, timedelta
from typing import Any

from .generator import STREAMS, GenerationConfig


def _rng(config: GenerationConfig, stream: str) -> random.Random:
    return random.Random(config.seed * 1_000_003 + STREAMS[stream])


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _active_bom(
    product_id: str, planned_time: datetime, boms: list[dict[str, Any]]
) -> dict[str, Any]:
    eligible = [
        bom
        for bom in boms
        if bom["product_id"] == product_id
        and _dt(bom["effective_from"]) <= planned_time < _dt(bom["effective_to"])
    ]
    if len(eligible) != 1:
        raise ValueError(f"expected one active BOM for {product_id}")
    return eligible[0]


def generate_operational(
    config: GenerationConfig, master: dict[str, list[dict[str, Any]]]
) -> dict[str, list[dict[str, Any]]]:
    """Generate connected orders, requirements, POs, transactions, and snapshots."""
    rng = _rng(config, "demand")
    counts = config.counts
    customers = master["customers"]
    products = master["products"]
    facilities = master["facilities"]
    warehouses = master["warehouses"]
    components = master["components"]
    agreements = master["supplier_component_agreements"]
    boms = master["bom_versions"]
    bom_lines = master["bom_lines"]
    reference = config.reference_time
    history_start = reference - timedelta(days=config.history_days)
    horizon_end = reference + timedelta(days=config.planning_horizon_days)

    customer_orders: list[dict[str, Any]] = []
    customer_order_lines: list[dict[str, Any]] = []
    for index in range(counts["customer_orders"]):
        customer = customers[index % len(customers)]
        product = products[index % len(products)]
        order_time = history_start + timedelta(days=(index * 7) % max(1, config.history_days))
        quantity = 50 + (index % 8) * 25
        promised = min(order_time + timedelta(days=7 + index % 14), horizon_end)
        if promised <= order_time:
            promised = order_time + timedelta(days=1)
        order_id = f"CO-{index + 1:06d}"
        line_id = f"COL-{index + 1:06d}-01"
        customer_orders.append(
            {
                "id": order_id,
                "customer_id": customer["id"],
                "order_time": _iso(order_time),
                "status": "OPEN",
                "priority": customer["priority"],
            }
        )
        customer_order_lines.append(
            {
                "id": line_id,
                "customer_order_id": order_id,
                "product_id": product["id"],
                "ordered_quantity": quantity,
                "promised_delivery": _iso(promised),
                "unit_revenue_inr": 4_000 + (index % 5) * 250,
                "priority": customer["priority"],
            }
        )

    production_orders: list[dict[str, Any]] = []
    production_customer_allocations: list[dict[str, Any]] = []
    production_requirements: list[dict[str, Any]] = []
    for index in range(counts["production_orders"]):
        line = customer_order_lines[index % len(customer_order_lines)]
        product = next(row for row in products if row["id"] == line["product_id"])
        facility = next(row for row in facilities if row["id"] == product["facility_id"])
        planned_quantity = 100 + (index % 3) * 50
        planned_start = reference + timedelta(days=index % config.planning_horizon_days)
        capacity = int(facility["daily_capacity_units"])
        duration_days = max(1, math.ceil(planned_quantity / capacity))
        planned_completion = planned_start + timedelta(days=duration_days)
        production_id = f"MO-{index + 1:06d}"
        production_orders.append(
            {
                "id": production_id,
                "product_id": product["id"],
                "facility_id": facility["id"],
                "planned_quantity": planned_quantity,
                "planned_start": _iso(planned_start),
                "planned_completion": _iso(planned_completion),
                "priority": line["priority"],
                "status": "PLANNED",
            }
        )
        production_customer_allocations.append(
            {
                "id": f"PCA-{index + 1:06d}",
                "production_order_id": production_id,
                "customer_order_line_id": line["id"],
                "allocated_quantity": min(planned_quantity, line["ordered_quantity"]),
            }
        )
        active_bom = _active_bom(product["id"], planned_start, boms)
        for bom_line in bom_lines:
            if bom_line["bom_version_id"] != active_bom["id"]:
                continue
            required = planned_quantity * int(bom_line["quantity_per"])
            production_requirements.append(
                {
                    "id": f"MR-{len(production_requirements) + 1:06d}",
                    "production_order_id": production_id,
                    "component_id": bom_line["component_id"],
                    "required_quantity": required,
                    "bom_version_id": active_bom["id"],
                }
            )

    purchase_orders: list[dict[str, Any]] = []
    for index in range(counts["purchase_orders"]):
        component = components[index % len(components)]
        agreement = next(row for row in agreements if row["component_id"] == component["id"])
        supplier = agreement["supplier_id"]
        order_time = history_start + timedelta(days=(index * 3) % config.history_days)
        ordered = int(agreement["minimum_order_quantity"]) * (1 + index % 3)
        expected = order_time + timedelta(days=int(agreement["lead_time_days"]))
        purchase_orders.append(
            {
                "id": f"PO-{index + 1:06d}",
                "supplier_id": supplier,
                "component_id": component["id"],
                "destination_warehouse_id": warehouses[index % len(warehouses)]["id"],
                "order_time": _iso(order_time),
                "ordered_quantity": ordered,
                "received_quantity": ordered,
                "outstanding_quantity": 0,
                "expected_arrival": _iso(expected),
                "status": "RECEIVED",
                "unit_price_inr": agreement["unit_price_inr"],
            }
        )

    inventory_transactions: list[dict[str, Any]] = []
    balances: dict[tuple[str, str], int] = {}
    for warehouse_index, warehouse in enumerate(warehouses):
        for component_index, component in enumerate(components):
            opening = 400 + (warehouse_index + component_index) * 10
            key = (warehouse["id"], component["id"])
            balances[key] = opening
            inventory_transactions.append(
                {
                    "id": f"INVTX-{len(inventory_transactions) + 1:06d}",
                    "warehouse_id": warehouse["id"],
                    "component_id": component["id"],
                    "event_time": _iso(history_start),
                    "transaction_type": "OPENING_BALANCE",
                    "quantity": opening,
                    "reference_id": None,
                }
            )
    for purchase_order in purchase_orders:
        event_time = _dt(purchase_order["expected_arrival"])
        key = (purchase_order["destination_warehouse_id"], purchase_order["component_id"])
        balances[key] += int(purchase_order["received_quantity"])
        inventory_transactions.append(
            {
                "id": f"INVTX-{len(inventory_transactions) + 1:06d}",
                "warehouse_id": purchase_order["destination_warehouse_id"],
                "component_id": purchase_order["component_id"],
                "event_time": _iso(event_time),
                "transaction_type": "PURCHASE_RECEIPT",
                "quantity": purchase_order["received_quantity"],
                "reference_id": purchase_order["id"],
            }
        )
    for requirement in production_requirements:
        facility_id = next(
            order["facility_id"]
            for order in production_orders
            if order["id"] == requirement["production_order_id"]
        )
        facility_index = next(
            index for index, row in enumerate(facilities) if row["id"] == facility_id
        )
        warehouse_id = warehouses[facility_index % len(warehouses)]["id"]
        key = (warehouse_id, requirement["component_id"])
        issue = min(balances[key], int(requirement["required_quantity"]))
        balances[key] -= issue
        if issue:
            production = next(
                order
                for order in production_orders
                if order["id"] == requirement["production_order_id"]
            )
            inventory_transactions.append(
                {
                    "id": f"INVTX-{len(inventory_transactions) + 1:06d}",
                    "warehouse_id": warehouse_id,
                    "component_id": requirement["component_id"],
                    "event_time": production["planned_start"],
                    "transaction_type": "PRODUCTION_ISSUE",
                    "quantity": issue,
                    "reference_id": requirement["production_order_id"],
                }
            )

    inventory_snapshots: list[dict[str, Any]] = []
    for day in range(config.history_days + 1):
        snapshot_time = history_start + timedelta(days=day)
        for warehouse in warehouses:
            for component in components:
                key = (warehouse["id"], component["id"])
                relevant = [
                    transaction
                    for transaction in inventory_transactions
                    if transaction["warehouse_id"] == warehouse["id"]
                    and transaction["component_id"] == component["id"]
                    and _dt(transaction["event_time"]) <= snapshot_time
                ]
                on_hand = sum(
                    int(transaction["quantity"])
                    * (
                        1
                        if transaction["transaction_type"]
                        in {"OPENING_BALANCE", "PURCHASE_RECEIPT", "PRODUCTION_RETURN"}
                        else -1
                    )
                    for transaction in relevant
                )
                inventory_snapshots.append(
                    {
                        "id": f"SNAP-{day:04d}-{warehouse['id']}-{component['id']}",
                        "snapshot_time": _iso(snapshot_time),
                        "warehouse_id": warehouse["id"],
                        "component_id": component["id"],
                        "on_hand_quantity": on_hand,
                        "reserved_quantity": 0,
                        "safety_stock_quantity": next(
                            int(row["safety_stock_units"])
                            for row in components
                            if row["id"] == component["id"]
                        ),
                    }
                )
    # Keep the stream active without affecting referential or conservation rules.
    rng.random()
    return {
        "customer_orders": customer_orders,
        "customer_order_lines": customer_order_lines,
        "production_orders": production_orders,
        "production_customer_allocations": production_customer_allocations,
        "production_material_requirements": production_requirements,
        "purchase_orders": purchase_orders,
        "inventory_transactions": inventory_transactions,
        "inventory_snapshots": inventory_snapshots,
    }


def generate_history(
    config: GenerationConfig,
    master: dict[str, list[dict[str, Any]]],
    operational: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Derive historical and bitemporal records from generated operations."""
    start = config.reference_time - timedelta(days=config.history_days)
    end = config.reference_time + timedelta(days=config.planning_horizon_days)
    entity_versions = [
        {
            "id": f"VER-{index + 1:06d}",
            "entity_type": "SUPPLIER_COMPONENT_AGREEMENT",
            "entity_id": row["id"],
            "valid_from": row["effective_from"],
            "valid_to": row["effective_to"],
            "recorded_at": row["effective_from"],
        }
        for index, row in enumerate(master["supplier_component_agreements"])
    ]
    status_events: list[dict[str, Any]] = []
    for index, order in enumerate(operational["purchase_orders"]):
        status_events.append(
            {
                "id": f"STATUS-{index + 1:06d}",
                "entity_type": "PURCHASE_ORDER",
                "entity_id": order["id"],
                "status": order["status"],
                "event_time": order["expected_arrival"],
                "recorded_at": order["expected_arrival"],
            }
        )
    performance = [
        {
            "id": f"SUPPERF-{index + 1:06d}",
            "supplier_id": row["id"],
            "period_start": _iso(start),
            "period_end": _iso(end),
            "on_time_rate": 0.85 + (index % 10) / 100,
            "fill_rate": 0.90 + (index % 5) / 100,
        }
        for index, row in enumerate(master["suppliers"])
    ]
    corrections = [
        {
            "id": "CORR-000001",
            "entity_type": "INVENTORY_SNAPSHOT",
            "entity_id": "SNAP-BITEMPORAL-001",
            "event_time": _iso(config.reference_time - timedelta(days=3, hours=15)),
            "known_at": _iso(config.reference_time - timedelta(days=2, hours=13, minutes=55)),
            "ingested_at": _iso(config.reference_time - timedelta(days=2, hours=13, minutes=50)),
            "corrected_quantity": 390,
            "original_quantity": 400,
        }
    ]
    return {
        "entity_versions": entity_versions,
        "status_events": status_events,
        "daily_inventory_snapshots": operational["inventory_snapshots"],
        "supplier_performance_history": performance,
        "historical_disruptions": [],
        "late_arriving_corrections": corrections,
    }
