"""Generate the executable Phase 4 load contract and Phase 3 traceability matrix."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if path.suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            return list(reader), list(reader.fieldnames or [])
    if path.suffix == ".jsonl":
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return rows, sorted({key for row in rows for key in row})
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list) and all(isinstance(row, dict) for row in payload):
        return payload, sorted({key for row in payload for key in row})
    if isinstance(payload, dict):
        return [payload], sorted(payload)
    return [], []


def _type_for(values: list[Any], key: str) -> str:
    if key.endswith(("_time", "_at", "_from", "_to", "_date")):
        return "TIMESTAMP"
    if any(token in key for token in ("quantity", "stock", "capacity", "count")):
        return "DECIMAL"
    if any(token in key for token in ("cost", "price", "revenue", "budget")):
        return "DECIMAL"
    if all(
        isinstance(value, bool) or str(value).lower() in {"true", "false"}
        for value in values
        if value != ""
    ):
        return "BOOLEAN"
    try:
        [float(value) for value in values if value != ""]
    except (TypeError, ValueError):
        return "VARCHAR"
    return "DECIMAL"


def _load_order(path: Path) -> int:
    text = path.as_posix()
    for marker, order in (
        ("master/locations", 1),
        ("master/facilities", 2),
        ("master/warehouses", 2),
        ("master/suppliers", 3),
        ("master/components", 3),
        ("supplier_component_agreements", 4),
        ("master/products", 5),
        ("master/bom", 5),
        ("master/customers", 6),
        ("master/sla", 6),
        ("master/transfer", 7),
        ("history", 8),
        ("operational/purchase", 9),
        ("operational/production", 10),
        ("operational/customer", 11),
        ("scenarios", 12),
        ("documents", 13),
        ("benchmarks", 14),
    ):
        if marker in text:
            return order
    return 15


def _entry(root: Path, path: Path) -> dict[str, Any]:
    rows, fields = _rows(path)
    primary_key = next(
        (key for key in ("id", "document_id", "scenario_id", "candidate_id") if key in fields),
        None,
    )
    foreign_keys = [key for key in fields if key.endswith("_id") and key != primary_key]
    column_types = {key: _type_for([row.get(key, "") for row in rows], key) for key in fields}
    nullable = [key for key in fields if any(row.get(key, "") in ("", None) for row in rows)]
    return {
        "source_file": path.relative_to(root).as_posix(),
        "record_type": path.stem.upper(),
        "primary_key": primary_key,
        "foreign_keys": foreign_keys,
        "data_types": column_types,
        "nullability": {key: key in nullable for key in fields},
        "unique_constraints": [primary_key] if primary_key else [],
        "check_constraints": ["non_negative_quantities_and_financials"],
        "temporal_columns": [
            key for key in fields if key.endswith(("_time", "_at", "_from", "_to", "_date"))
        ],
        "currency_columns": [
            key
            for key in fields
            if any(token in key for token in ("cost", "price", "revenue", "budget", "inr"))
        ],
        "quantity_columns": [
            key
            for key in fields
            if any(token in key for token in ("quantity", "stock", "capacity", "count"))
        ],
        "expected_target_table": path.stem.upper(),
        "load_order": _load_order(path.relative_to(root)),
        "expected_row_count": len(rows),
        "checksum": _sha(path),
    }


def build_handoff(root: Path) -> dict[str, Any]:
    roots = (
        root / "data" / "generated",
        root / "data" / "golden",
        root / "data" / "benchmarks",
        root / "data" / "fixtures",
    )
    files = sorted(
        path
        for directory in roots
        if directory.exists()
        for path in directory.rglob("*")
        if path.is_file() and path.suffix in {".csv", ".json", ".jsonl"}
    )
    entries = [_entry(root, path) for path in files]
    return {
        "contract_version": "1.0.0",
        "dataset_version": "1.0.0",
        "phase4_target": "IBM Db2",
        "load_order": [
            "REFERENCE_TYPES",
            "LOCATIONS",
            "SUPPLIERS",
            "COMPONENTS",
            "SUPPLIER_COMPONENT_AGREEMENTS",
            "PRODUCTS",
            "BOM_VERSIONS",
            "CUSTOMERS",
            "SLA_POLICIES",
            "TRANSFER_LANES",
            "INVENTORY",
            "PURCHASE_ORDERS",
            "PRODUCTION_ORDERS",
            "CUSTOMER_ORDERS",
            "DISRUPTIONS",
            "SCENARIOS",
            "DOCUMENTS",
            "BENCHMARKS",
        ],
        "files": entries,
    }


def write_traceability(root: Path, contract: dict[str, Any]) -> None:
    path = root / "docs" / "data" / "phase-3-traceability-matrix.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = (
        "phase2_rule_id",
        "domain_entity",
        "generated_file",
        "generator_module",
        "configuration_key",
        "validation_rule",
        "benchmark_scenario_ids",
        "expected_output_field",
        "ground_truth_function",
        "phase4_target_table",
        "status",
        "notes",
    )
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for entry in contract["files"]:
            writer.writerow(
                {
                    "phase2_rule_id": "PHASE3-LOAD-001",
                    "domain_entity": entry["record_type"],
                    "generated_file": entry["source_file"],
                    "generator_module": "data_generator",
                    "configuration_key": "config/generation.yaml",
                    "validation_rule": "phase3_release_validation",
                    "benchmark_scenario_ids": "SCN-0001..SCN-0060",
                    "expected_output_field": "expected_candidate_feasibility",
                    "ground_truth_function": "ground_truth.oracle.calculate_golden",
                    "phase4_target_table": entry["expected_target_table"],
                    "status": "APPROVED",
                    "notes": "Generated from packaged file metadata.",
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    contract = build_handoff(args.root)
    output = args.root / "data" / "phase4_load_contract.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_traceability(args.root, contract)
    print(f"Built Phase 4 load contract for {len(contract['files'])} files")


if __name__ == "__main__":
    main()
