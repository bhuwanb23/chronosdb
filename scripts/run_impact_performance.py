"""Measure deterministic Phase 5 impact stages at representative workloads."""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
import tracemalloc
from collections.abc import Callable
from datetime import timedelta
from functools import partial
from pathlib import Path
from statistics import median
from typing import Any

from chronosdb.impact.causality import build_causal_traces
from chronosdb.impact.contracts.requests import SimulationHorizon, parse_time
from chronosdb.impact.contracts.results import canonical_hash
from chronosdb.impact.disruption import Disruption, resolve_purchase_order_impacts
from chronosdb.impact.fulfilment import (
    build_customer_fulfilment,
    calculate_sla_and_financial_impact,
)
from chronosdb.impact.inventory import build_inventory_timelines, detect_shortages
from chronosdb.impact.materials import allocate_materials, build_material_requirements
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.persistence import ExecutionLedger
from chronosdb.impact.production import schedule_production
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor
from chronosdb.impact.supply import project_receipts

ROOT = Path(__file__).resolve().parents[1]
SCALES = {"tiny": 1, "demo": 2, "standard": 4, "stress": 8}
STAGES = (
    "state_reconstruction_ms",
    "disruption_resolution_ms",
    "inventory_projection_ms",
    "material_allocation_ms",
    "production_scheduling_ms",
    "customer_impact_ms",
    "causal_trace_build_ms",
    "persistence_ms",
    "total_ms",
)


def _measure(function: Callable[[], Any]) -> tuple[Any, float]:
    started = time.perf_counter()
    value = function()
    return value, (time.perf_counter() - started) * 1000


def _percentile(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int((len(ordered) * percentile) + 0.999999) - 1))
    return ordered[index]


def _scenario_inputs(
    root: Path,
) -> tuple[Any, Disruption, SimulationHorizon, Any, set[str] | None, set[str] | None]:
    scenario = json.loads(
        (root / "data" / "golden" / "scenario.json").read_text(encoding="utf-8")
    )
    as_of = parse_time(scenario["as_of_time"])
    state = ReleaseStateReconstructor(root).reconstruct(as_of)
    disruption = Disruption.from_state(state, "EVT-GOLD-001")
    horizon = SimulationHorizon(as_of, as_of + timedelta(days=30))
    rules = load_rule_set(root / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    scenario_payload = next(
        item for item in state.scenario_inputs if item.get("scenario_id") == scenario["scenario_id"]
    )
    order_ids = {
        str(item["production_order_id"])
        for item in scenario_payload.get("orders", [])
        if item.get("production_order_id")
    }
    line_ids = {
        str(item["id"])
        for item in scenario_payload.get("customer_order_lines", [])
        if item.get("id")
    }
    return state, disruption, horizon, rules, order_ids or None, line_ids or None


def _sample(
    root: Path,
    workload: int,
) -> dict[str, float]:
    measurements = {stage: [] for stage in STAGES}
    for _ in range(workload):
        state, disruption, horizon, rules, order_ids, line_ids = _scenario_inputs(root)
        _, state_ms = _measure(
            partial(ReleaseStateReconstructor(root).reconstruct, horizon.as_of_time)
        )
        measurements["state_reconstruction_ms"].append(state_ms)
        impacts, disruption_ms = _measure(
            partial(resolve_purchase_order_impacts, state, disruption)
        )
        measurements["disruption_resolution_ms"].append(disruption_ms)
        receipts = project_receipts(impacts, horizon)
        timelines, inventory_ms = _measure(
            partial(build_inventory_timelines, state, horizon, receipts)
        )
        measurements["inventory_projection_ms"].append(inventory_ms)
        requirements = build_material_requirements(
            state,
            horizon.as_of_time,
            horizon.simulation_end_time,
            production_order_ids=order_ids,
        )
        allocations, allocation_ms = _measure(
            partial(allocate_materials, requirements, timelines)
        )
        measurements["material_allocation_ms"].append(allocation_ms)
        shortages = detect_shortages(allocations, horizon.simulation_end_time)
        production_impacts, production_ms = _measure(
            partial(schedule_production, state, requirements, allocations, horizon)
        )
        measurements["production_scheduling_ms"].append(production_ms)
        customer_impacts, customer_ms = _measure(
            partial(
                build_customer_fulfilment,
                state,
                production_impacts,
                horizon,
                production_order_ids=order_ids,
                customer_order_line_ids=line_ids,
            )
        )
        measurements["customer_impact_ms"].append(customer_ms)
        sla_results, _ = calculate_sla_and_financial_impact(
            customer_impacts,
            disruption_caused_production_order_ids={
                shortage.production_order_id for shortage in shortages
            },
            horizon_end=horizon.simulation_end_time,
        )
        _, causal_ms = _measure(
            partial(
                build_causal_traces,
                disruption,
                impacts,
                production_impacts,
                sla_results,
                state.identity,
                rules.version,
            )
        )
        measurements["causal_trace_build_ms"].append(causal_ms)
        impact_result, total_ms = _measure(
            partial(
                calculate_impact,
                state,
                disruption,
                horizon,
                rules,
                scenario_id="SCN-GOLD-001",
            )
        )
        measurements["total_ms"].append(total_ms)
        ledger = ExecutionLedger()
        _, persistence_ms = _measure(
            partial(
                _persist_result,
                ledger,
                impact_result,
            )
        )
        measurements["persistence_ms"].append(persistence_ms)
    return {stage: sum(values) / workload for stage, values in measurements.items()}


def _persist_result(ledger: ExecutionLedger, result: Any) -> None:
    run = ledger.begin(
        impact_run_id=result.impact_run_id,
        scenario_id=result.scenario_id,
        request_fingerprint=canonical_hash(result.to_dict()),
        input_state_hash=result.input_state_hash,
        rule_set_version=result.rule_set_version,
        data_quality_status=result.data_quality_status.value,
    )
    ledger.complete(
        run.impact_run_id,
        status=result.status.value,
        data_quality_status=result.data_quality_status.value,
        result_hash=result.result_hash,
        payload=result.to_dict(),
    )


def _run_scale(root: Path, scale: str, repetitions: int) -> dict[str, Any]:
    sample_count = max(1, repetitions * SCALES[scale])
    samples = [_sample(root, 1) for _ in range(sample_count)]
    summary: dict[str, Any] = {
        "scale": scale,
        "workload_count": SCALES[scale],
        "repetitions": repetitions,
        "request_samples": sample_count,
        "stages": {},
    }
    for stage in STAGES:
        values = [sample[stage] for sample in samples]
        summary["stages"][stage] = {
            "median_ms": round(median(values), 3),
            "p95_ms": round(_percentile(values, 0.95), 3),
            "maximum_ms": round(max(values), 3),
            "samples_ms": [round(value, 3) for value in values],
        }
    return summary


def run(root: Path = ROOT, repetitions: int = 3) -> dict[str, Any]:
    results = [_run_scale(root, scale, repetitions) for scale in SCALES]
    payload = {
        "performance_version": "impact-engine-v1.0.0",
        "dataset_version": "1.0.0",
        "environment": {
            "cpu": platform.processor(),
            "memory_note": "Peak traced Python allocation is recorded per scale.",
            "operating_system": platform.platform(),
            "python": sys.version,
            "db2": "not used by release-file benchmark",
            "rule_set_version": "impact-rules-v1.0.0",
            "warm_or_cold": "warm process, cold state reconstruction per workload",
        },
        "scales": results,
        "result_hash": "",
    }
    payload["result_hash"] = canonical_hash(payload)
    output_dir = root / "artifacts" / "phase-5" / "performance"
    output_dir.mkdir(parents=True, exist_ok=True)
    for result in results:
        (output_dir / f"{result['scale']}-performance.json").write_text(
            json.dumps({**payload, "scales": [result]}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    (output_dir / "performance-report.md").write_text(
        "\n".join(
            [
                "# Impact Engine Performance Report",
                "",
                f"- Result hash: `{payload['result_hash']}`",
                f"- Platform: `{payload['environment']['operating_system']}`",
                f"- Python: `{platform.python_version()}`",
                "",
                "Each scale measures the complete deterministic pipeline plus separately "
                "timed domain stages. Results are release-file runs without Db2 latency.",
                "",
                *[
                    f"- `{item['scale']}` workload `{item['workload_count']}`: "
                    f"total p95 `{item['stages']['total_ms']['p95_ms']} ms`"
                    for item in results
                ],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    tracemalloc.start()
    result = run(args.root, max(1, args.repetitions))
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    (args.root / "artifacts" / "phase-5" / "performance" / "memory.json").write_text(
        json.dumps({"peak_traced_bytes": peak}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Impact performance result: {result['result_hash']}")


if __name__ == "__main__":
    main()
