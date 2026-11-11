"""Validate Phase 3H–3O generated artifacts and frozen outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data_generator.export import read_csv_rows
from data_generator.generator import ENTITY_FILES
from data_generator.scenarios import validate_documents, validate_scenarios
from data_generator.validation import validate_master, validate_operational
from ground_truth.oracle import calculate_golden


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--scale", choices=("tiny", "standard", "stress"), default="tiny")
    args = parser.parse_args()
    root = args.root
    master_dir = root / "data" / "generated" / "master" / args.scale
    master = {entity: read_csv_rows(master_dir / f"{entity}.csv") for entity in ENTITY_FILES}
    validate_master(master)
    operation_dir = root / "data" / "generated" / "operational"
    operational_names = (
        "customer_orders",
        "customer_order_lines",
        "production_orders",
        "production_customer_allocations",
        "production_material_requirements",
        "purchase_orders",
        "inventory_transactions",
        "inventory_snapshots",
    )
    operational = {
        name: read_csv_rows(operation_dir / f"{name}.csv") for name in operational_names
    }
    validate_operational(master, operational)
    scenario_dir = root / "data" / "generated" / "scenarios"
    scenarios = {
        "scenario_definitions": _json(scenario_dir / "scenario_definitions.json"),
        "scenario_constraints": _json(scenario_dir / "scenario_constraints.json"),
        "disruptions": read_csv_rows(scenario_dir / "disruptions.csv"),
        "candidate_parameters": read_csv_rows(scenario_dir / "candidate_parameters.csv"),
        "intervention_costs": read_csv_rows(scenario_dir / "intervention_costs.csv"),
    }
    validate_scenarios(scenarios)
    documents = [
        json.loads(line)
        for line in (root / "data" / "generated" / "documents" / "documents.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
    ]
    validate_documents(documents)
    golden = calculate_golden()
    if _json(root / "data" / "golden" / "expected_recommendation.json") != golden["recommendation"]:
        raise ValueError("golden recommendation mismatch")
    if _json(root / "data" / "golden" / "expected_do_nothing.json") != golden["do_nothing"]:
        raise ValueError("golden do-nothing mismatch")
    expected = _json(root / "data" / "benchmarks" / "expected.json")
    partitions = _json(root / "data" / "benchmarks" / "partitions.json")
    if len(expected) != 60:
        raise ValueError("benchmark expected-output count mismatch")
    broad = partitions["development"] + partitions["validation"] + partitions["test"]
    if len(broad) != len(set(broad)):
        raise ValueError("benchmark partition overlap")
    fixtures = _json(root / "data" / "fixtures" / "expected_errors.json")
    if len(fixtures) != 30:
        raise ValueError("fixture count mismatch")
    print(f"Phase 3H–3O validation passed for {args.scale}")


if __name__ == "__main__":
    main()
