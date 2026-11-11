"""Invariant validation for Phase 3G master data."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from .generator import ENTITY_FILES


class ValidationError(ValueError):
    """Raised when generated data violates a Phase 3 invariant."""


def read_entities(directory: Path) -> dict[str, list[dict[str, str]]]:
    return {
        entity: list(csv.DictReader((directory / f"{entity}.csv").open(encoding="utf-8")))
        for entity in ENTITY_FILES
    }


def _ids(rows: list[dict[str, Any]]) -> set[str]:
    return {row["id"] for row in rows}


def validate_master(entities: dict[str, list[dict[str, Any]]]) -> None:
    """Validate counts-independent referential, temporal, and domain invariants."""
    required = set(ENTITY_FILES)
    if set(entities) != required:
        raise ValidationError(f"entity set mismatch: {set(entities) ^ required}")
    all_ids: set[str] = set()
    for entity, rows in entities.items():
        ids = _ids(rows)
        if len(ids) != len(rows):
            raise ValidationError(f"duplicate IDs in {entity}")
        if all_ids & ids:
            raise ValidationError(f"cross-entity ID collision in {entity}")
        all_ids.update(ids)

    location_ids = _ids(entities["locations"])
    facility_ids = _ids(entities["facilities"])
    warehouse_ids = _ids(entities["warehouses"])
    supplier_ids = _ids(entities["suppliers"])
    component_ids = _ids(entities["components"])
    product_ids = _ids(entities["products"])
    bom_ids = _ids(entities["bom_versions"])
    sla_ids = _ids(entities["sla_policies"])

    for row in entities["facilities"] + entities["warehouses"]:
        if row["location_id"] not in location_ids:
            raise ValidationError(f"unknown location: {row}")
    for row in entities["transfer_lanes"]:
        if row["source_warehouse"] not in warehouse_ids:
            raise ValidationError(f"unknown transfer source: {row}")
        if row["destination_warehouse"] not in warehouse_ids:
            raise ValidationError(f"unknown transfer destination: {row}")
        if row["source_warehouse"] == row["destination_warehouse"]:
            raise ValidationError(f"self transfer lane: {row}")
        if (
            float(row["lead_time_hours"]) <= 0
            or float(row["fixed_cost"]) < 0
            or float(row["variable_cost_per_unit"]) < 0
        ):
            raise ValidationError(f"invalid transfer lane values: {row}")
        if row["currency"] != "INR":
            raise ValidationError(f"invalid transfer currency: {row}")
        effective_from = datetime.fromisoformat(row["active_from"].replace("Z", "+00:00"))
        effective_to = datetime.fromisoformat(row["active_to"].replace("Z", "+00:00"))
        if effective_from >= effective_to:
            raise ValidationError(f"invalid transfer interval: {row}")
    lane_pairs = {
        (row["source_warehouse"], row["destination_warehouse"])
        for row in entities["transfer_lanes"]
    }
    if len(lane_pairs) != len(entities["transfer_lanes"]):
        raise ValidationError("duplicate transfer lane pair")
    for row in entities["supplier_component_agreements"]:
        if row["supplier_id"] not in supplier_ids or row["component_id"] not in component_ids:
            raise ValidationError(f"unknown agreement reference: {row}")
        if row["approval_status"] != "APPROVED":
            raise ValidationError(f"unapproved generated agreement: {row}")
        if float(row["lead_time_days"]) <= 0 or float(row["unit_price_inr"]) <= 0:
            raise ValidationError(f"invalid agreement values: {row}")
        effective_from = datetime.fromisoformat(row["effective_from"].replace("Z", "+00:00"))
        effective_to = datetime.fromisoformat(row["effective_to"].replace("Z", "+00:00"))
        if effective_from >= effective_to:
            raise ValidationError(f"invalid agreement interval: {row}")
    agreement_pairs = {
        (row["supplier_id"], row["component_id"])
        for row in entities["supplier_component_agreements"]
    }
    if len(agreement_pairs) != len(entities["supplier_component_agreements"]):
        raise ValidationError("duplicate active supplier-component agreement")
    for row in entities["products"]:
        if row["facility_id"] not in facility_ids:
            raise ValidationError(f"unknown product facility: {row}")
    bom_by_product: dict[str, list[dict[str, Any]]] = {}
    for row in entities["bom_versions"]:
        if row["product_id"] not in product_ids or row["status"] not in {"ACTIVE", "SUPERSEDED"}:
            raise ValidationError(f"invalid BOM: {row}")
        effective_from = datetime.fromisoformat(row["effective_from"].replace("Z", "+00:00"))
        effective_to = datetime.fromisoformat(row["effective_to"].replace("Z", "+00:00"))
        if effective_from >= effective_to:
            raise ValidationError(f"invalid BOM interval: {row}")
        bom_by_product.setdefault(row["product_id"], []).append(row)
    for row in entities["bom_lines"]:
        if row["bom_version_id"] not in bom_ids or row["component_id"] not in component_ids:
            raise ValidationError(f"unknown BOM line reference: {row}")
        if float(row["quantity_per"]) <= 0 or not 0 <= float(row["scrap_factor"]) < 1:
            raise ValidationError(f"invalid BOM line quantity: {row}")
        component = next(
            item for item in entities["components"] if item["id"] == row["component_id"]
        )
        if component["status"] != "ACTIVE":
            raise ValidationError(f"inactive BOM component: {row}")
    for product_id, boms in bom_by_product.items():
        ordered = sorted(boms, key=lambda row: row["effective_from"])
        active = [row for row in ordered if row["status"] == "ACTIVE"]
        if len(active) != 1:
            raise ValidationError(f"product must have exactly one active BOM: {product_id}")
        for previous, current in zip(ordered, ordered[1:], strict=False):
            if previous["effective_to"] > current["effective_from"]:
                raise ValidationError(f"overlapping BOM intervals: {product_id}")
        for bom in ordered:
            lines = [
                row["component_id"]
                for row in entities["bom_lines"]
                if row["bom_version_id"] == bom["id"]
            ]
            if len(lines) != len(set(lines)) or not lines:
                raise ValidationError(f"invalid BOM lines: {bom['id']}")
    for row in entities["customers"]:
        if row["default_sla_policy_id"] not in sla_ids or row["status"] != "ACTIVE":
            raise ValidationError(f"unknown customer SLA: {row}")
        effective_from = datetime.fromisoformat(row["effective_from"].replace("Z", "+00:00"))
        effective_to = datetime.fromisoformat(row["effective_to"].replace("Z", "+00:00"))
        if effective_from >= effective_to:
            raise ValidationError(f"invalid customer interval: {row}")
    for row in entities["sla_policies"]:
        if float(row["delivery_lead_time_days"]) < 0:
            raise ValidationError(f"invalid SLA lead time: {row}")
        effective_from = datetime.fromisoformat(row["effective_from"].replace("Z", "+00:00"))
        effective_to = datetime.fromisoformat(row["effective_to"].replace("Z", "+00:00"))
        if effective_from >= effective_to:
            raise ValidationError(f"invalid SLA interval: {row}")

    component_agreements = {
        row["component_id"] for row in entities["supplier_component_agreements"]
    }
    bom_components = {row["component_id"] for row in entities["bom_lines"]}
    if component_agreements != component_ids:
        raise ValidationError("every component must have an agreement")
    if not bom_components.issubset(component_ids):
        raise ValidationError("BOM references unknown component")
    for product in product_ids:
        product_boms = [row for row in entities["bom_versions"] if row["product_id"] == product]
        if not any(row["status"] == "ACTIVE" for row in product_boms):
            raise ValidationError(f"product has no active BOM: {product}")


def validate_operational(
    master: dict[str, list[dict[str, Any]]],
    operational: dict[str, list[dict[str, Any]]],
) -> None:
    """Validate Phase 3H relationships, temporal rules, and inventory conservation."""
    required = {
        "customer_orders",
        "customer_order_lines",
        "production_orders",
        "production_customer_allocations",
        "production_material_requirements",
        "purchase_orders",
        "inventory_transactions",
        "inventory_snapshots",
    }
    if set(operational) != required:
        raise ValidationError(f"operational entity set mismatch: {set(operational) ^ required}")
    customer_ids = _ids(master["customers"])
    product_ids = _ids(master["products"])
    facility_ids = _ids(master["facilities"])
    warehouse_ids = _ids(master["warehouses"])
    component_ids = _ids(master["components"])
    agreement_ids = _ids(master["supplier_component_agreements"])
    order_ids = _ids(operational["customer_orders"])
    line_ids = _ids(operational["customer_order_lines"])
    production_ids = _ids(operational["production_orders"])
    po_ids = _ids(operational["purchase_orders"])
    requirement_ids = _ids(operational["production_material_requirements"])
    for row in operational["customer_orders"]:
        if row["customer_id"] not in customer_ids:
            raise ValidationError(f"unknown customer order customer: {row}")
    for row in operational["customer_order_lines"]:
        if row["customer_order_id"] not in order_ids or row["product_id"] not in product_ids:
            raise ValidationError(f"unknown customer order line reference: {row}")
        if int(row["ordered_quantity"]) <= 0:
            raise ValidationError(f"invalid customer order quantity: {row}")
        order_time = next(
            order["order_time"]
            for order in operational["customer_orders"]
            if order["id"] == row["customer_order_id"]
        )
        promised = datetime.fromisoformat(row["promised_delivery"].replace("Z", "+00:00"))
        if promised <= datetime.fromisoformat(order_time.replace("Z", "+00:00")):
            raise ValidationError(f"promised date is not after order time: {row}")
    for row in operational["production_orders"]:
        if row["facility_id"] not in facility_ids or row["product_id"] not in product_ids:
            raise ValidationError(f"unknown production reference: {row}")
        if int(row["planned_quantity"]) <= 0:
            raise ValidationError(f"invalid planned quantity: {row}")
        planned_start = datetime.fromisoformat(row["planned_start"].replace("Z", "+00:00"))
        planned_completion = datetime.fromisoformat(
            row["planned_completion"].replace("Z", "+00:00")
        )
        if planned_completion < planned_start:
            raise ValidationError(f"production time ordering: {row}")
    for row in operational["production_customer_allocations"]:
        if (
            row["production_order_id"] not in production_ids
            or row["customer_order_line_id"] not in line_ids
        ):
            raise ValidationError(f"unknown production allocation: {row}")
        if int(row["allocated_quantity"]) <= 0:
            raise ValidationError(f"invalid allocation: {row}")
    for row in operational["production_material_requirements"]:
        if (
            row["production_order_id"] not in production_ids
            or row["component_id"] not in component_ids
        ):
            raise ValidationError(f"unknown material requirement: {row}")
        if row["id"] not in requirement_ids or int(row["required_quantity"]) <= 0:
            raise ValidationError(f"invalid material requirement: {row}")
    for row in operational["purchase_orders"]:
        if (
            row["component_id"] not in component_ids
            or row["destination_warehouse_id"] not in warehouse_ids
        ):
            raise ValidationError(f"unknown purchase order reference: {row}")
        if int(row["ordered_quantity"]) <= 0 or int(row["received_quantity"]) > int(
            row["ordered_quantity"]
        ):
            raise ValidationError(f"invalid purchase order quantity: {row}")
    for row in operational["inventory_transactions"]:
        if row["warehouse_id"] not in warehouse_ids or row["component_id"] not in component_ids:
            raise ValidationError(f"unknown inventory transaction reference: {row}")
        if int(row["quantity"]) < 0:
            raise ValidationError(f"negative inventory transaction: {row}")
        if (
            row["reference_id"]
            and row["transaction_type"] == "PURCHASE_RECEIPT"
            and row["reference_id"] not in po_ids
        ):
            raise ValidationError(f"unknown receipt purchase order: {row}")
    snapshot_keys = {
        (row["snapshot_time"], row["warehouse_id"], row["component_id"])
        for row in operational["inventory_snapshots"]
    }
    if len(snapshot_keys) != len(operational["inventory_snapshots"]):
        raise ValidationError("duplicate inventory snapshot")
    if not agreement_ids:
        raise ValidationError("operational data requires supply agreements")
    latest_snapshot_time = max(row["snapshot_time"] for row in operational["inventory_snapshots"])
    for snapshot in operational["inventory_snapshots"]:
        if snapshot["snapshot_time"] != latest_snapshot_time:
            continue
        relevant = [
            transaction
            for transaction in operational["inventory_transactions"]
            if transaction["warehouse_id"] == snapshot["warehouse_id"]
            and transaction["component_id"] == snapshot["component_id"]
            and transaction["event_time"] <= latest_snapshot_time
        ]
        expected = sum(
            int(transaction["quantity"])
            * (
                1
                if transaction["transaction_type"]
                in {"OPENING_BALANCE", "PURCHASE_RECEIPT", "PRODUCTION_RETURN"}
                else -1
            )
            for transaction in relevant
        )
        if int(snapshot["on_hand_quantity"]) != expected:
            raise ValidationError(f"inventory conservation failure: {snapshot['id']}")
