"""Deterministic Phase 3G master-data generator."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

ENTITY_FILES = (
    "locations",
    "facilities",
    "warehouses",
    "transfer_lanes",
    "suppliers",
    "components",
    "supplier_component_agreements",
    "products",
    "bom_versions",
    "bom_lines",
    "customers",
    "sla_policies",
)
STREAMS = {
    "master": 101,
    "demand": 202,
    "supply": 303,
    "inventory": 404,
    "disruption": 505,
    "document": 606,
    "benchmark": 707,
}


@dataclass(frozen=True)
class GenerationConfig:
    root: Path
    scale: str
    seed: int
    dataset_version: str
    generator_version: str
    reference_time: datetime
    counts: dict[str, int]
    enterprise: dict[str, Any]


def _utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def load_config(root: Path, scale: str, seed: int | None = None) -> GenerationConfig:
    """Load the documented enterprise and scale configuration."""
    with (root / "config" / "enterprise.yaml").open(encoding="utf-8") as stream:
        enterprise = yaml.safe_load(stream)
    with (root / "config" / "generation.yaml").open(encoding="utf-8") as stream:
        generation = yaml.safe_load(stream)
    with (root / "config" / "scales" / f"{scale}.yaml").open(encoding="utf-8") as stream:
        scale_config = yaml.safe_load(stream)
    return GenerationConfig(
        root=root,
        scale=scale,
        seed=generation["seed"] if seed is None else seed,
        dataset_version=generation["dataset_version"],
        generator_version=generation["generator_version"],
        reference_time=_utc(generation["reference_time"]),
        counts=scale_config["counts"],
        enterprise=enterprise,
    )


def _id(prefix: str, number: int) -> str:
    return f"{prefix}-{number:06d}"


def _rng(config: GenerationConfig, stream: str) -> random.Random:
    return random.Random(config.seed * 1_000_003 + STREAMS[stream])


def _date(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def generate_master(config: GenerationConfig) -> dict[str, list[dict[str, Any]]]:
    """Generate all Phase 3G master entities in dependency order."""
    rng = _rng(config, "master")
    counts = config.counts
    base_locations = config.enterprise["locations"]
    location_count = max(len(base_locations), counts["facilities"], counts["warehouses"])
    locations: list[dict[str, Any]] = []
    for index in range(location_count):
        if index < len(base_locations):
            row = dict(base_locations[index])
            row["id"] = f"LOC-{index + 1:06d}"
        else:
            row = {
                "id": _id("LOC", index + 1),
                "city": f"Site-{index + 1:03d}",
                "country": "IN",
            }
        locations.append(row)

    facilities = [
        {
            "id": _id("FAC", index + 1),
            "location_id": locations[index % len(locations)]["id"],
            "daily_capacity_units": 60 + (index % 5) * 20,
            "capacity_unit": "EA",
            "status": "ACTIVE",
        }
        for index in range(counts["facilities"])
    ]
    warehouses = [
        {
            "id": _id("WH", index + 1),
            "location_id": locations[index % len(locations)]["id"],
            "status": "ACTIVE",
        }
        for index in range(counts["warehouses"])
    ]
    transfer_lanes = [
        {
            "id": _id("LANE", index + 1),
            "source_warehouse_id": warehouses[index % len(warehouses)]["id"],
            "destination_warehouse_id": warehouses[(index + 1) % len(warehouses)]["id"],
            "lead_time_days": 1 + index % 3,
            "fixed_cost_inr": 20_000 + index * 1_000,
            "variable_cost_per_unit_inr": 25 + index % 6,
        }
        for index in range(max(1, len(warehouses) * (len(warehouses) - 1)))
    ]
    suppliers = [
        {
            "id": _id("SUP", index + 1),
            "name": f"Asterion Supplier {index + 1:03d}",
            "approval_status": "APPROVED" if index % 10 else "APPROVED",
            "status": "ACTIVE",
            "country": "IN",
        }
        for index in range(counts["suppliers"])
    ]
    components = [
        {
            "id": _id("CMP", index + 1),
            "name": f"Component-{index + 1:03d}",
            "unit": "EA",
            "component_type": "ELECTRONIC",
            "status": "ACTIVE",
        }
        for index in range(counts["components"])
    ]
    start = config.reference_time - timedelta(days=365)
    end = config.reference_time + timedelta(days=365)
    agreements: list[dict[str, Any]] = []
    for index, component in enumerate(components):
        supplier_id = suppliers[index % len(suppliers)]["id"]
        agreements.append(
            {
                "id": _id("AGR", len(agreements) + 1),
                "supplier_id": supplier_id,
                "component_id": component["id"],
                "approval_status": "APPROVED",
                "lead_time_days": 3 + rng.randrange(12),
                "unit_price_inr": float(25 + rng.randrange(20) * 125),
                "minimum_order_quantity": 10 + (index % 10) * 10,
                "daily_capacity_units": 100 + (index % 8) * 50,
                "effective_from": _date(start),
                "effective_to": _date(end),
            }
        )
        if len(suppliers) > 1:
            alternate = suppliers[(index + 1) % len(suppliers)]["id"]
            agreements.append(
                {
                    "id": _id("AGR", len(agreements) + 1),
                    "supplier_id": alternate,
                    "component_id": component["id"],
                    "approval_status": "APPROVED",
                    "lead_time_days": 5 + rng.randrange(10),
                    "unit_price_inr": float(50 + rng.randrange(20) * 140),
                    "minimum_order_quantity": 20 + (index % 8) * 10,
                    "daily_capacity_units": 100 + (index % 5) * 50,
                    "effective_from": _date(start),
                    "effective_to": _date(end),
                }
            )
    products = [
        {
            "id": _id("PRD", index + 1),
            "name": f"Controller-{index + 1:03d}",
            "unit": "EA",
            "status": "ACTIVE",
            "facility_id": facilities[index % len(facilities)]["id"],
        }
        for index in range(counts["products"])
    ]
    bom_versions: list[dict[str, Any]] = []
    versions_per_product = [
        sum(index % len(products) == product_index for index in range(counts["bom_versions"]))
        for product_index in range(len(products))
    ]
    for index in range(counts["bom_versions"]):
        product = products[index % len(products)]
        version_for_product = sum(
            row["product_id"] == product["id"] for row in bom_versions
        ) + 1
        effective_from = (
            start
            if version_for_product == 1
            else config.reference_time - timedelta(days=180)
        )
        has_newer_version = versions_per_product[index % len(products)] > version_for_product
        effective_to = (
            config.reference_time - timedelta(days=180)
            if has_newer_version
            else config.reference_time + timedelta(days=365)
        )
        bom_versions.append(
            {
                "id": _id("BOM", index + 1),
                "product_id": product["id"],
                "version": version_for_product,
                "status": "ACTIVE"
                if effective_from <= config.reference_time < effective_to
                else "SUPERSEDED",
                "effective_from": _date(effective_from),
                "effective_to": _date(effective_to),
            }
        )
    bom_lines: list[dict[str, Any]] = []
    for index, bom in enumerate(bom_versions):
        line_count = 1 + (index % min(4, len(components)))
        for line in range(line_count):
            bom_lines.append(
                {
                    "id": _id("BOMLINE", len(bom_lines) + 1),
                    "bom_version_id": bom["id"],
                    "component_id": components[(index + line) % len(components)]["id"],
                    "quantity_per": 1 + (line % 3),
                    "scrap_factor": 0.0,
                    "mandatory": True,
                }
            )
    customers = [
        {
            "id": _id("CUS", index + 1),
            "name": f"Asterion Customer {index + 1:04d}",
            "priority": ("HIGH", "MEDIUM", "LOW")[index % 3],
            "status": "ACTIVE",
            "default_sla_policy_id": _id("SLA", (index % 3) + 1),
        }
        for index in range(counts["customers"])
    ]
    sla_policies = [
        {
            "id": _id("SLA", index + 1),
            "name": name,
            "delivery_lead_time_days": lead,
            "late_tolerance_hours": 0,
        }
        for index, (name, lead) in enumerate(
            (("STANDARD", 1), ("PRIORITY", 0), ("EXTENDED", 3))
        )
    ]
    return {
        "locations": locations,
        "facilities": facilities,
        "warehouses": warehouses,
        "transfer_lanes": transfer_lanes,
        "suppliers": suppliers,
        "components": sorted(components, key=lambda row: row["id"]),
        "supplier_component_agreements": agreements,
        "products": products,
        "bom_versions": bom_versions,
        "bom_lines": bom_lines,
        "customers": customers,
        "sla_policies": sla_policies,
    }


def write_master(
    config: GenerationConfig, entities: dict[str, list[dict[str, Any]]]
) -> Path:
    """Write canonical CSV files and a content-addressed manifest."""
    output = config.root / "data" / "generated" / "master" / config.scale
    output.mkdir(parents=True, exist_ok=True)
    files: list[dict[str, Any]] = []
    for entity in ENTITY_FILES:
        rows = sorted(entities[entity], key=lambda row: str(row["id"]))
        path = output / f"{entity}.csv"
        fieldnames = sorted({key for row in rows for key in row})
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        files.append(
            {
                "path": path.relative_to(config.root).as_posix(),
                "rows": len(rows),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    manifest = {
        "dataset_version": config.dataset_version,
        "generator_version": config.generator_version,
        "phase": "3G",
        "layer": "master",
        "scale": config.scale,
        "seed": config.seed,
        "reference_time": _date(config.reference_time),
        "files": files,
        "seed_streams": STREAMS,
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return output
