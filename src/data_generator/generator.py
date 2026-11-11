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
    money_decimal_places: int
    quantity_decimal_places: int
    history_days: int
    planning_horizon_days: int


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
        money_decimal_places=generation["serialization"]["money_decimal_places"],
        quantity_decimal_places=generation["serialization"]["quantity_decimal_places"],
        history_days=generation["history_days"],
        planning_horizon_days=generation["planning_horizon_days"],
    )


def _id(prefix: str, number: int) -> str:
    return f"{prefix}-{number:04d}"


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
        else:
            row = {
                "id": _id("LOC", index + 1),
                "city": f"Site-{index + 1:03d}",
                "country": "IN",
            }
        locations.append(row)

    configured_facilities = config.enterprise["facilities"]
    facilities = []
    for index in range(counts["facilities"]):
        if index < len(configured_facilities):
            row = dict(configured_facilities[index])
            row["capacity_unit"] = "EA"
            row["status"] = "ACTIVE"
        else:
            row = {
                "id": _id("FAC", index + 1),
                "location_id": locations[index % len(locations)]["id"],
                "daily_capacity_units": 60 + (index % 5) * 20,
                "capacity_unit": "EA",
                "status": "ACTIVE",
            }
        facilities.append(row)
    configured_warehouses = config.enterprise["warehouses"]
    warehouses = []
    for index in range(counts["warehouses"]):
        if index < len(configured_warehouses):
            row = dict(configured_warehouses[index])
            row["status"] = "ACTIVE"
        else:
            row = {
                "id": _id("WH", index + 1),
                "location_id": locations[index % len(locations)]["id"],
                "status": "ACTIVE",
            }
        warehouses.append(row)
    start = config.reference_time - timedelta(days=config.history_days)
    end = config.reference_time + timedelta(days=config.planning_horizon_days)
    transfer_lanes: list[dict[str, Any]] = []
    for source in warehouses:
        for destination in warehouses:
            if source["id"] == destination["id"]:
                continue
            index = len(transfer_lanes)
            transfer_lanes.append(
                {
                    "id": _id("LANE", index + 1),
                    "source_warehouse": source["id"],
                    "destination_warehouse": destination["id"],
                    "lead_time_hours": 24 + (index % 3) * 24,
                    "fixed_cost": 20_000 + index * 1_000,
                    "variable_cost_per_unit": 25 + index % 6,
                    "currency": "INR",
                    "active_from": _date(start),
                    "active_to": _date(end),
                }
            )
    suppliers = [
        {
            "id": _id("SUP", index + 1),
            "name": f"Asterion Supplier {index + 1:03d}",
            "approval_status": "APPROVED" if index % 10 else "APPROVED",
            "status": "ACTIVE",
            "country": "IN",
            "region": ("WEST", "SOUTH", "NORTH", "EAST")[index % 4],
            "effective_from": _date(start),
            "effective_to": _date(end),
        }
        for index in range(counts["suppliers"])
    ]
    components = [
        {
            "id": _id("CMP", index + 1),
            "name": f"Component-{index + 1:03d}",
            "unit": "EA",
            "component_type": "ELECTRONIC",
            "criticality": ("CRITICAL", "HIGH", "MEDIUM", "LOW")[index % 4],
            "safety_stock_units": 10 + (index % 10) * 5,
            "standard_unit_cost_inr": float(25 + (index % 20) * 125),
            "status": "ACTIVE",
        }
        for index in range(counts["components"])
    ]
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
        has_newer_version = versions_per_product[index % len(products)] > version_for_product
        version_count = versions_per_product[index % len(products)]
        bom_start = config.reference_time - timedelta(
            days=min(30, max(1, config.history_days // 2))
        )
        if version_for_product == 1:
            effective_from = start
        else:
            effective_from = start + (bom_start - start) * (
                version_for_product - 1
            ) / (version_count - 1)
        effective_to = (
            start + (bom_start - start) * version_for_product / (version_count - 1)
            if has_newer_version
            else end
        )
        bom_versions.append(
            {
                "id": f"BOM-{index + 1:04d}-V{version_for_product:02d}",
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
            "customer_class": ("INDUSTRIAL", "DISTRIBUTOR", "OEM")[index % 3],
            "sla_class": ("STANDARD", "PRIORITY", "EXTENDED")[index % 3],
            "default_sla_policy_id": _id("SLA", (index % 3) + 1),
            "effective_from": _date(start),
            "effective_to": _date(end),
        }
        for index in range(counts["customers"])
    ]
    sla_policies = [
        {
            "id": _id("SLA", index + 1),
            "name": name,
            "delivery_lead_time_days": lead,
            "late_tolerance_hours": 0,
            "effective_from": _date(start),
            "effective_to": _date(end),
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
            for row in rows:
                writer.writerow(
                    {
                        key: (
                            ""
                            if value is None
                            else str(value).lower()
                            if isinstance(value, bool)
                            else f"{value:.{config.money_decimal_places}f}"
                            if isinstance(value, (int, float))
                            and any(token in key for token in ("cost", "price"))
                            else f"{value:.{config.quantity_decimal_places}f}"
                            if isinstance(value, (int, float))
                            and any(
                                token in key
                                for token in (
                                    "quantity",
                                    "capacity",
                                    "stock",
                                    "minimum_order",
                                    "per_unit",
                                )
                            )
                            else value
                        )
                        for key, value in row.items()
                    }
                )
        files.append(
            {
                "path": path.relative_to(config.root).as_posix(),
                "rows": len(rows),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    config_paths = (
        Path("config/enterprise.yaml"),
        Path("config/generation.yaml"),
        Path(f"config/scales/{config.scale}.yaml"),
    )
    if all((config.root / relative).exists() for relative in config_paths):
        config_bytes = b"".join((config.root / relative).read_bytes() for relative in config_paths)
    else:
        config_bytes = json.dumps(
            {"scale": config.scale, "counts": config.counts, "enterprise": config.enterprise},
            sort_keys=True,
        ).encode()
    manifest = {
        "dataset_name": "chronosdb-synthetic-supply-chain",
        "version": config.dataset_version,
        "dataset_version": config.dataset_version,
        "generator_version": config.generator_version,
        "domain_model_version": "2.0",
        "phase": "3G",
        "layer": "master",
        "scale": config.scale,
        "seed": config.seed,
        "random_seed": config.seed,
        "reference_time": _date(config.reference_time),
        "generated_at": _date(config.reference_time),
        "currency": "INR",
        "canonical_timezone": "UTC",
        "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "files": files,
        "seed_streams": STREAMS,
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return output
