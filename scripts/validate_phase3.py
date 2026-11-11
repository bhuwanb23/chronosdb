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
    operation_dir = root / "data" / "generated" / "operational" / args.scale
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
    history_dir = root / "data" / "generated" / "history" / args.scale
    history_names = (
        "entity_versions",
        "status_events",
        "daily_inventory_snapshots",
        "supplier_performance_history",
        "safety_stock_versions",
        "sla_versions",
        "supplier_delay_history",
        "production_history",
        "historical_disruptions",
        "late_arriving_corrections",
    )
    history = {name: read_csv_rows(history_dir / f"{name}.csv") for name in history_names}
    snapshot_ids = {row["id"] for row in history["daily_inventory_snapshots"]}
    snapshots_by_id = {row["id"]: row for row in history["daily_inventory_snapshots"]}
    for correction in history["late_arriving_corrections"]:
        if correction["entity_id"] not in snapshot_ids:
            raise ValueError(f"orphan temporal correction: {correction['id']}")
        if correction["event_time"] != snapshots_by_id[correction["entity_id"]]["snapshot_time"]:
            raise ValueError(f"correction does not target snapshot time: {correction['id']}")
        if correction["known_at"] <= correction["event_time"]:
            raise ValueError(f"invalid bitemporal ordering: {correction['id']}")
    production_starts = {
        row["id"]: row["planned_start"] for row in operational["production_orders"]
    }
    for event in history["production_history"]:
        if event["event_time"] < production_starts[event["production_order_id"]]:
            raise ValueError(f"production history precedes order: {event['id']}")
    order_times = {row["id"]: row["order_time"] for row in operational["purchase_orders"]}
    for delay in history["supplier_delay_history"]:
        if delay["event_time"] < order_times[delay["purchase_order_id"]]:
            raise ValueError(f"supplier delay precedes purchase order: {delay['id']}")
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
    metadata = [
        json.loads(line)
        for line in (
            root / "data" / "generated" / "documents" / "document_metadata.jsonl"
        ).read_text(encoding="utf-8").splitlines()
    ]
    relevance = _json(root / "data" / "generated" / "documents" / "retrieval_relevance.json")
    document_ids = {row["document_id"] for row in documents}
    if {row["document_id"] for row in metadata} != document_ids or len(relevance) != len(documents):
        raise ValueError("evidence metadata/relevance join mismatch")
    for label in relevance:
        groups = [
            set(label["relevant_document_ids"]),
            set(label["partially_relevant_document_ids"]),
            set(label["irrelevant_document_ids"]),
            set(label["filtered_document_ids"]),
        ]
        if any(group - document_ids for group in groups):
            raise ValueError(f"unknown evidence relevance ID: {label['query_id']}")
        if sum(len(group) for group in groups) != len(set().union(*groups)):
            raise ValueError(f"overlapping evidence relevance labels: {label['query_id']}")
    golden = calculate_golden()
    frozen_scenario = _json(root / "data" / "golden" / "scenario.json")
    if frozen_scenario["disruption"]["supplier_id"] != frozen_scenario["supplier_id"]:
        raise ValueError("golden disruption supplier mismatch")
    line_ids = {row["id"] for row in frozen_scenario["customer_order_lines"]}
    traces = _json(root / "data" / "golden" / "expected_causal_traces.json")
    if any(trace["target"]["customer_order_line_id"] not in line_ids for trace in traces):
        raise ValueError("golden causal trace target mismatch")
    valid_trace_sources = {
        frozen_scenario["disruption"]["id"],
        frozen_scenario["purchase_order_id"],
        frozen_scenario["component_id"],
        *(order["production_order_id"] for order in frozen_scenario["orders"]),
        *line_ids,
    }
    for trace in traces:
        if trace["result"]["reference_case"] != "DO-NOTHING":
            raise ValueError(f"golden trace reference mismatch: {trace['trace_id']}")
        if any(step["source_id"] not in valid_trace_sources for step in trace["steps"]):
            raise ValueError(f"golden trace source mismatch: {trace['trace_id']}")
    if _json(root / "data" / "golden" / "expected_recommendation.json") != golden["recommendation"]:
        raise ValueError("golden recommendation mismatch")
    if _json(root / "data" / "golden" / "expected_do_nothing.json") != golden["do_nothing"]:
        raise ValueError("golden do-nothing mismatch")
    if _json(root / "data" / "golden" / "expected_interventions.json") != golden["interventions"]:
        raise ValueError("golden intervention mismatch")
    expected = _json(root / "data" / "benchmarks" / "expected.json")
    partitions = _json(root / "data" / "benchmarks" / "partitions.json")
    if len(expected) != 60:
        raise ValueError("benchmark expected-output count mismatch")
    scenario_ids = {row["id"] for row in scenarios["scenario_definitions"]}
    if {row["scenario_id"] for row in expected} != scenario_ids:
        raise ValueError("benchmark expected-output scenario join mismatch")
    candidate_ids = {row["id"] for row in scenarios["candidate_parameters"]}
    for outcome in expected:
        if set(outcome["expected_candidate_feasibility"]) != {
            candidate_id
            for candidate_id in candidate_ids
            if candidate_id.startswith(f"INT-{outcome['scenario_id'].split('-')[-1]}-")
        }:
            raise ValueError(f"benchmark candidate join mismatch: {outcome['scenario_id']}")
        recommendation = outcome["expected_recommendation"]
        if recommendation is not None and not outcome["expected_candidate_feasibility"].get(
            recommendation, False
        ):
            raise ValueError(f"infeasible benchmark recommendation: {outcome['scenario_id']}")
    broad = (
        partitions["development"]
        + partitions["validation"]
        + partitions["test"]
        + partitions["adversarial"]
        + partitions["review_holdout"]
    )
    if len(broad) != len(set(broad)):
        raise ValueError("benchmark partition overlap")
    if set(broad) != {f"SCN-{index:04d}" for index in range(1, 61)}:
        raise ValueError("benchmark partition coverage mismatch")
    fixtures = _json(root / "data" / "fixtures" / "expected_errors.json")
    if len(fixtures) < 30:
        raise ValueError("fixture count mismatch")
    print(f"Phase 3H–3O validation passed for {args.scale}")


if __name__ == "__main__":
    main()
