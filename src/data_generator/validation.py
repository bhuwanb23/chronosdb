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
        if row["source_warehouse_id"] not in warehouse_ids:
            raise ValidationError(f"unknown transfer source: {row}")
        if row["destination_warehouse_id"] not in warehouse_ids:
            raise ValidationError(f"unknown transfer destination: {row}")
        if row["source_warehouse_id"] == row["destination_warehouse_id"]:
            raise ValidationError(f"self transfer lane: {row}")
        if float(row["lead_time_days"]) <= 0 or float(row["fixed_cost_inr"]) < 0:
            raise ValidationError(f"invalid transfer lane values: {row}")
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
    for row in entities["products"]:
        if row["facility_id"] not in facility_ids:
            raise ValidationError(f"unknown product facility: {row}")
    for row in entities["bom_versions"]:
        if row["product_id"] not in product_ids or row["status"] not in {"ACTIVE", "SUPERSEDED"}:
            raise ValidationError(f"invalid BOM: {row}")
        effective_from = datetime.fromisoformat(row["effective_from"].replace("Z", "+00:00"))
        effective_to = datetime.fromisoformat(row["effective_to"].replace("Z", "+00:00"))
        if effective_from >= effective_to:
            raise ValidationError(f"invalid BOM interval: {row}")
    for row in entities["bom_lines"]:
        if row["bom_version_id"] not in bom_ids or row["component_id"] not in component_ids:
            raise ValidationError(f"unknown BOM line reference: {row}")
        if float(row["quantity_per"]) <= 0 or not 0 <= float(row["scrap_factor"]) < 1:
            raise ValidationError(f"invalid BOM line quantity: {row}")
    for row in entities["customers"]:
        if row["default_sla_policy_id"] not in sla_ids:
            raise ValidationError(f"unknown customer SLA: {row}")
    for row in entities["sla_policies"]:
        if float(row["delivery_lead_time_days"]) < 0:
            raise ValidationError(f"invalid SLA lead time: {row}")

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
