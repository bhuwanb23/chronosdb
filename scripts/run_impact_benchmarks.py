"""Evaluate the supported deterministic impact benchmark partitions."""

from __future__ import annotations

import argparse
import json
from datetime import timedelta
from pathlib import Path
from typing import Any

from chronosdb.impact.contracts.requests import SimulationHorizon, parse_time
from chronosdb.impact.contracts.results import canonical_hash
from chronosdb.impact.disruption import Disruption
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor

ROOT = Path(__file__).resolve().parents[1]


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _golden_metrics(root: Path) -> dict[str, Any]:
    scenario = _json(root / "data" / "golden" / "scenario.json")
    as_of = parse_time(scenario["as_of_time"])
    state = ReleaseStateReconstructor(root).reconstruct(as_of)
    result = calculate_impact(
        state,
        Disruption.from_state(state, "EVT-GOLD-001"),
        SimulationHorizon(as_of, as_of + timedelta(days=30)),
        load_rule_set(root / "config" / "rules" / "impact-rules-v1.0.0.yaml"),
        scenario_id=scenario["scenario_id"],
    ).to_dict()
    expected = _json(root / "data" / "golden" / "expected_do_nothing.json")
    expected_traces = _json(root / "data" / "golden" / "expected_causal_traces.json")
    expected_engine_traces = _json(
        root / "data" / "golden" / "expected_engine_causal_traces.json"
    )
    expected_orders = {
        line["customer_order_id"]
        for line in expected["customer_lines"]
        if line["late_quantity"] > 0
    }
    actual_orders = {
        line["customer_order_id"] for line in result["affected_customer_orders"]
    }
    expected_production = {
        order["production_order_id"]
        for order in scenario["orders"]
        if order["customer_order_id"] in expected_orders
    }
    actual_production = {
        row["production_order_id"] for row in result["affected_production_orders"]
    }
    expected_components = {scenario["component_id"]}
    actual_components = set(result["affected_components"])
    expected_purchase_orders = {scenario["purchase_order_id"]}
    actual_purchase_orders = {
        row["purchase_order_id"] for row in result["affected_purchase_orders"]
    }

    def ratio(actual: set[str], wanted: set[str]) -> dict[str, Any]:
        true_positive = len(actual & wanted)
        return {
            "precision": true_positive / len(actual) if actual else 1.0,
            "recall": true_positive / len(wanted) if wanted else 1.0,
            "actual": sorted(actual),
            "expected": sorted(wanted),
        }

    metrics = result["headline_metrics"]
    exact_fields = {
        "breached_customer_order_count": (
            metrics["breached_customer_order_count"],
            expected["breached_customer_orders"],
        ),
        "late_quantity": (
            metrics["late_quantity"],
            str(sum(line["late_quantity"] for line in expected["customer_lines"])),
        ),
        "total_delay_unit_hours": (
            metrics["total_delay_unit_hours"],
            str(expected["total_delay_hours"]),
        ),
        "revenue_at_risk_inr": (
            metrics["revenue_at_risk"]["amount"],
            expected["revenue_at_risk_inr"],
        ),
    }
    exact_matches = sum(actual == wanted for actual, wanted in exact_fields.values())
    expected_sla = {
        line["customer_order_id"]
        for line in expected["customer_lines"]
        if line["late_quantity"] > 0
    }
    actual_sla = {
        line["customer_order_id"] for line in result["affected_customer_orders"]
    }
    expected_edges = {
        (
            trace["target"]["customer_order_line_id"],
            len(trace["steps"]),
            tuple(sorted(step["source_id"] for step in trace["steps"][1:])),
        )
        for trace in expected_traces
    }
    actual_edges = {
        (
            trace["target"]["entity_id"],
            len(trace["edges"]),
            tuple(
                sorted(
                    source_id
                    for source_id in trace["source_record_ids"]
                    if source_id != "EVT-GOLD-001"
                )
            ),
        )
        for trace in result["causal_traces"]
    }
    causal_precision = (
        len(actual_edges & expected_edges) / len(actual_edges) if actual_edges else 1.0
    )
    causal_recall = (
        len(actual_edges & expected_edges) / len(expected_edges) if expected_edges else 1.0
    )
    expected_trace_hashes = {canonical_hash(trace) for trace in expected_engine_traces}
    actual_trace_hashes = {canonical_hash(trace) for trace in result["causal_traces"]}
    causal_precision = (
        len(actual_trace_hashes & expected_trace_hashes) / len(actual_trace_hashes)
        if actual_trace_hashes
        else 1.0
    )
    causal_recall = (
        len(actual_trace_hashes & expected_trace_hashes) / len(expected_trace_hashes)
        if expected_trace_hashes
        else 1.0
    )
    purchase_order = ratio(actual_purchase_orders, expected_purchase_orders)
    component = ratio(actual_components, expected_components)
    production_order = ratio(actual_production, expected_production)
    customer_order = ratio(actual_orders, expected_orders)
    return {
        "scenario_id": scenario["scenario_id"],
        "result_hash": result["result_hash"],
        "purchase_order": purchase_order,
        "component": component,
        "production_order": production_order,
        "customer_order": customer_order,
        "numerical_exact_match_rate": exact_matches / len(exact_fields),
        "sla_classification_accuracy": float(actual_sla == expected_sla),
        "financial_fidelity": float(
            metrics["revenue_at_risk"]["amount"] == expected["revenue_at_risk_inr"]
        ),
        "causal_edge_precision": causal_precision,
        "causal_edge_recall": causal_recall,
        "data_quality_classification_accuracy": float(
            result["data_quality_status"]
            == ("PARTIAL_NONCRITICAL" if state.warnings else "COMPLETE")
        ),
        "targets_met": all(
            (
                actual_purchase_orders == expected_purchase_orders,
                metrics["breached_customer_order_count"] == expected["breached_customer_orders"],
                metrics["late_quantity"]
                == str(sum(line["late_quantity"] for line in expected["customer_lines"])),
                metrics["total_delay_unit_hours"] == str(expected["total_delay_hours"]),
                metrics["revenue_at_risk"]["amount"] == expected["revenue_at_risk_inr"],
                purchase_order["precision"] == 1.0,
                purchase_order["recall"] == 1.0,
                component["precision"] == 1.0,
                component["recall"] == 1.0,
                production_order["precision"] == 1.0,
                production_order["recall"] == 1.0,
                customer_order["precision"] == 1.0,
                customer_order["recall"] == 1.0,
                exact_matches / len(exact_fields) == 1.0,
                actual_sla == expected_sla,
                metrics["revenue_at_risk"]["amount"] == expected["revenue_at_risk_inr"],
                causal_precision == 1.0,
                causal_recall == 1.0,
                result["data_quality_status"]
                == ("PARTIAL_NONCRITICAL" if state.warnings else "COMPLETE"),
            )
        ),
    }


def run(root: Path = ROOT) -> dict[str, Any]:
    partitions = _json(root / "data" / "benchmarks" / "partitions.json")
    result = {
        "benchmark_version": "impact-engine-v1.0.0",
        "dataset_version": "1.0.0",
        "partitions": {name: len(values) for name, values in partitions.items()},
        "supported_scenarios": ["SCN-GOLD-001"],
        "unsupported_intervention_scenarios": [
            scenario_id
            for name, values in partitions.items()
            for scenario_id in values
            if scenario_id != "SCN-GOLD-001"
        ],
        "golden": _golden_metrics(root),
    }
    if not result["golden"]["targets_met"]:
        raise RuntimeError("golden correctness targets were not met")
    result["result_hash"] = canonical_hash(result)
    output_dir = root / "artifacts" / "phase-5"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "impact-benchmark-results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report = [
        "# Impact Benchmark Report",
        "",
        "The deterministic Phase 5 do-nothing engine is evaluated against the "
        "frozen complete golden scenario.",
        "",
        f"- Result hash: `{result['result_hash']}`",
        f"- Supported scenarios: `{len(result['supported_scenarios'])}`",
        f"- Frozen partition counts: `{result['partitions']}`",
        "",
        "Golden correctness targets:",
        "",
        f"- Affected components: precision `{result['golden']['component']['precision']:.3f}`, "
        f"recall `{result['golden']['component']['recall']:.3f}`",
        f"- Production orders: precision "
        f"`{result['golden']['production_order']['precision']:.3f}`, "
        f"recall `{result['golden']['production_order']['recall']:.3f}`",
        f"- Customer orders: precision "
        f"`{result['golden']['customer_order']['precision']:.3f}`, "
        f"recall `{result['golden']['customer_order']['recall']:.3f}`",
        f"- Numerical exact-match rate: `{result['golden']['numerical_exact_match_rate']:.3f}`",
        f"- SLA classification accuracy: `{result['golden']['sla_classification_accuracy']:.3f}`",
        f"- Financial fidelity: `{result['golden']['financial_fidelity']:.3f}`",
        f"- Causal precision/recall: `{result['golden']['causal_edge_precision']:.3f}`/"
        f"`{result['golden']['causal_edge_recall']:.3f}`",
        "",
        "Intervention benchmark scenarios remain explicitly out of scope for the "
        "Phase 5 do-nothing engine and are reserved for Phase 6.",
    ]
    (output_dir / "impact-benchmark-report.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = run(args.root)
    print(f"Impact benchmark result: {result['result_hash']}")


if __name__ == "__main__":
    main()
