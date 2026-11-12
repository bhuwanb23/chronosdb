"""Deterministic Phase 4 projection of immutable Phase 3 master data."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .release_export import write_release_csv, write_release_json
from .release_profile import ReleaseProfile, release_root

MASTER_FILES = (
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
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _map_value(value: str | None, aliases: dict[str, str]) -> str | None:
    return aliases.get(value, value) if value is not None else None


def _map_row(row: dict[str, Any], aliases: dict[str, str]) -> dict[str, Any]:
    mapped = dict(row)
    for key, value in row.items():
        if key == "id" or key.endswith("_id") or key in {
            "source_warehouse",
            "destination_warehouse",
            "warehouse_id",
            "component_id",
            "product_id",
            "facility_id",
        }:
            mapped[key] = _map_value(str(value) if value is not None else None, aliases)
    return mapped


def project_master(profile: ReleaseProfile) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
    source = profile.root / "data" / "generated" / "master" / profile.source_scale
    aliases: dict[str, str] = {
        "SUP-0001": "SUP-0104",
        "SUP-0002": "SUP-0208",
        "CMP-0001": "CMP-MCU-42",
        "PRD-0001": "PRD-CONTROLLER-X",
        "WH-BENGALURU": "WH-GURUGRAM",
    }
    projected = {
        name: [_map_row(row, aliases) for row in _read_csv(source / f"{name}.csv")]
        for name in MASTER_FILES
    }
    for row in projected["suppliers"]:
        if row["id"] == "SUP-0024":
            row["status"] = "INACTIVE"
            row["supplier_class"] = "INACTIVE_HISTORICAL"
        else:
            row["supplier_class"] = (
                "DOMESTIC_REGIONAL"
                if int(row["id"].split("-")[-1]) % 3 == 0
                else "DOMESTIC_NATIONAL"
            )
    for row in projected["components"]:
        row["source_class"] = (
            "SINGLE_SOURCE"
            if row["id"] == "CMP-MCU-42"
            else "DUAL_SOURCE"
            if int(row["id"].split("-")[-1]) % 3 == 0
            else "MULTI_SOURCE"
        )
    for row in projected["facilities"]:
        row.update(
            {
                "source_warehouse_id": (
                    "WH-PUNE" if row["id"] == "FAC-PUNE" else "WH-CHENNAI"
                ),
                "operating_calendar": "CAL-WEEKDAY-UTC",
                "supported_product_families": "CONTROLLER",
                "effective_from": "2026-05-15T02:30:00Z",
                "effective_to": "2026-12-11T02:30:00Z",
            }
        )
    for row in projected["warehouses"]:
        row.update(
            {
                "region": (
                    "WEST"
                    if row["id"] == "WH-PUNE"
                    else "SOUTH"
                    if row["id"] == "WH-CHENNAI"
                    else "NORTH"
                ),
                "timezone": "Asia/Kolkata",
                "transfer_eligible": "true",
                "component_storage_eligible": "true",
                "effective_from": "2026-05-15T02:30:00Z",
                "effective_to": "2026-12-11T02:30:00Z",
            }
        )
    agreements = projected["supplier_component_agreements"][:150]
    projected["supplier_component_agreements"] = agreements
    active_boms = {
        row["id"] for row in projected["bom_versions"] if row["status"] == "ACTIVE"
    }
    component_ids = [row["id"] for row in projected["components"]]
    lines_by_bom: dict[str, list[dict[str, Any]]] = {}
    for row in projected["bom_lines"]:
        lines_by_bom.setdefault(row["bom_version_id"], []).append(row)
    next_line = len(projected["bom_lines"]) + 1
    for bom_id in active_boms:
        existing = lines_by_bom.setdefault(bom_id, [])
        used = {row["component_id"] for row in existing}
        for component_id in component_ids:
            if len(existing) >= 3:
                break
            if component_id in used:
                continue
            existing.append(
                {
                    "id": f"BOMLINE-P4-{next_line:06d}",
                    "bom_version_id": bom_id,
                    "component_id": component_id,
                    "quantity_per": "1",
                    "scrap_factor": "0.0",
                    "mandatory": "true",
                }
            )
            used.add(component_id)
            next_line += 1
    projected["bom_lines"] = [
        line for lines in lines_by_bom.values() for line in lines
    ]
    return projected, aliases


def write_master_release(
    profile: ReleaseProfile,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
    projected, aliases = project_master(profile)
    output = release_root(profile)
    master_dir = output / "master"
    for name, rows in projected.items():
        write_release_csv(master_dir / f"{name}.csv", rows)
    capabilities = [
            {
                "id": f"CAP-{index:04d}",
                "facility_id": facility["id"],
                "product_family": "CONTROLLER",
                "effective_from": facility["effective_from"],
                "effective_to": facility["effective_to"],
                "status": "ACTIVE",
            }
            for index, facility in enumerate(projected["facilities"], start=1)
            for _ in [0]
        ]
    links = [
            {
                "id": f"WFL-{index:04d}",
                "warehouse_id": facility["source_warehouse_id"],
                "facility_id": facility["id"],
                "effective_from": facility["effective_from"],
                "effective_to": facility["effective_to"],
                "status": "ACTIVE",
            }
            for index, facility in enumerate(projected["facilities"], start=1)
        ]
    write_release_csv(master_dir / "facility_product_capabilities.csv", capabilities)
    write_release_csv(master_dir / "warehouse_facility_links.csv", links)
    projected["facility_product_capabilities"] = capabilities
    projected["warehouse_facility_links"] = links
    write_release_json(output / "metadata" / "id_aliases.json", aliases)
    return projected, aliases
