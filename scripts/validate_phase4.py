"""Validate one Phase 4A–4G release profile."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from data_generator.phase4_validation import (
    Phase4ValidationError,
    validate_capacity,
    validate_demand_release,
    validate_inventory_release,
    validate_manufacturing_release,
    validate_master_release,
    validate_procurement,
)
from data_generator.release_profile import load_release_profile, release_root


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _validate_manifest(root: Path, output: Path) -> None:
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    nested_profiles = {"tiny", "demo", "standard", "stress"}
    actual: dict[str, str] = {}
    for path in output.rglob("*"):
        relative_to_output = path.relative_to(output)
        if (
            path.is_file()
            and path.name != "manifest.json"
            and not (
                manifest.get("profile") == "demo"
                and relative_to_output.parts[0] in nested_profiles
            )
        ):
            actual[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    declared = {
        item["path"]: item["sha256"]
        for item in manifest.get("files", [])
    }
    if declared != actual:
        missing = sorted(set(actual) - set(declared))
        extra = sorted(set(declared) - set(actual))
        changed = sorted(
            path for path in set(actual) & set(declared)
            if actual[path] != declared[path]
        )
        raise Phase4ValidationError(
            f"manifest hash mismatch (missing={missing}, extra={extra}, changed={changed})"
        )


def _load_release(root: Path, profile_name: str) -> dict[str, Any]:
    profile = load_release_profile(root, profile_name)
    output = release_root(profile)
    master_names = (
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
        "facility_product_capabilities",
        "warehouse_facility_links",
    )
    master = {name: _csv(output / "master" / f"{name}.csv") for name in master_names}
    operations = {
        "purchase_orders": _csv(output / "operations" / "purchase_orders.csv"),
        "status_history": _csv(output / "operations" / "purchase_order_status_history.csv"),
        "receipts": _csv(output / "operations" / "purchase_order_receipts.csv"),
        "capacity": _csv(output / "operations" / "supplier_capacity_calendar.csv"),
    }
    inventory = {
        "opening": _csv(output / "inventory" / "inventory_opening_balances.csv"),
        "transactions": _csv(output / "inventory" / "inventory_transactions.csv"),
        "reservations": _csv(output / "inventory" / "inventory_reservations.csv"),
        "snapshots": _csv(output / "inventory" / "inventory_snapshots_daily.csv"),
        "benchmark_snapshots": _csv(
            output / "inventory" / "inventory_snapshots_benchmark.csv"
        ),
        "transfer_transactions": _csv(
            output / "inventory" / "transfer_transactions.csv"
        ),
    }
    manufacturing = {
        "production_orders": _csv(output / "production" / "production_orders.csv"),
        "statuses": _csv(output / "production" / "production_order_status_history.csv"),
        "batches": _csv(output / "production" / "production_batches.csv"),
        "requirements": _csv(
            output / "production" / "production_material_requirements.csv"
        ),
        "allocations": _csv(
            output / "production" / "production_material_allocations.csv"
        ),
        "capacity": _csv(output / "production" / "facility_capacity_calendar.csv"),
    }
    demand = {
        "orders": _csv(output / "demand" / "customer_orders.csv"),
        "lines": _csv(output / "demand" / "customer_order_lines.csv"),
        "statuses": _csv(output / "demand" / "customer_order_status_history.csv"),
        "allocations": _csv(output / "demand" / "production_customer_allocations.csv"),
        "sla_assignments": _csv(output / "demand" / "customer_sla_assignments.csv"),
    }
    history = {
        "entity_versions": _csv(output / "history" / "entity_versions.csv"),
        "business_events": _csv(output / "history" / "business_events.csv"),
        "late_arriving_records": _csv(output / "history" / "late_arriving_records.csv"),
        "historical_inventory_checkpoints": _csv(
            output / "history" / "historical_inventory_checkpoints.csv"
        ),
        "replay_expectations": json.loads(
            (output / "history" / "replay_expectations.json").read_text(
                encoding="utf-8"
            )
        ),
    }
    return {
        "profile": profile,
        "output": output,
        "master": master,
        "operations": operations,
        "inventory": inventory,
        "manufacturing": manufacturing,
        "demand": demand,
        "history": history,
    }


def validate_profile(root: Path, profile_name: str) -> dict[str, Any]:
    release = _load_release(root, profile_name)
    profile = release["profile"]
    _validate_manifest(root, release["output"])
    validate_master_release(
        release["master"],
        require_full_network=profile.profile != "tiny",
    )
    validate_procurement(
        release["operations"]["purchase_orders"],
        release["operations"]["status_history"],
        release["operations"]["receipts"],
        release["operations"]["capacity"],
    )
    validate_inventory_release(release["inventory"])
    validate_manufacturing_release(
        release["manufacturing"]["production_orders"],
        release["manufacturing"]["requirements"],
        release["manufacturing"]["batches"],
        release["manufacturing"]["allocations"],
        release["master"],
    )
    validate_capacity(
        release["manufacturing"]["batches"],
        release["manufacturing"]["capacity"],
    )
    validate_demand_release(
        release["demand"],
        release["master"],
        release["manufacturing"]["production_orders"],
    )
    validate_history_release(release["history"], release["inventory"])
    return {
        "profile": profile.profile,
        "version": profile.version,
        "status": "PASS",
        "counts": {
            "master_files": len(release["master"]),
            "purchase_orders": len(release["operations"]["purchase_orders"]),
            "inventory_snapshots": len(release["inventory"]["snapshots"]),
            "production_orders": len(release["manufacturing"]["production_orders"]),
            "customer_orders": len(release["demand"]["orders"]),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("tiny", "demo", "standard", "stress"), default="demo")
    parser.add_argument("--scope", default="4A-4G")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        report = validate_profile(args.root, args.profile)
    except (OSError, KeyError, ValueError, Phase4ValidationError) as error:
        report = {
            "profile": args.profile,
            "scope": args.scope,
            "status": "FAIL",
            "error": str(error),
        }
        print(json.dumps(report, indent=2))
        raise SystemExit(1) from error
    output = args.root / "artifacts" / "phase-4"
    output.mkdir(parents=True, exist_ok=True)
    (output / f"{args.profile}-validation.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Phase 4 {args.profile} validation passed")


if __name__ == "__main__":
    main()
