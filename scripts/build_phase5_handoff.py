"""Build the immutable Phase 5 release and Phase 6 handoff package."""

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


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(root: Path = ROOT) -> dict[str, Any]:
    scenario = _read(root / "data" / "golden" / "scenario.json")
    as_of = parse_time(scenario["as_of_time"])
    horizon = SimulationHorizon(as_of, as_of + timedelta(days=30))
    rules = load_rule_set(root / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    state = ReleaseStateReconstructor(root).reconstruct(as_of)
    disruption = Disruption.from_state(state, "EVT-GOLD-001")
    first = calculate_impact(
        state, disruption, horizon, rules, scenario_id=scenario["scenario_id"]
    ).to_dict()
    second = calculate_impact(
        state, disruption, horizon, rules, scenario_id=scenario["scenario_id"]
    ).to_dict()

    output_dir = root / "artifacts" / "phase-5-handoff"
    output_dir.mkdir(parents=True, exist_ok=True)
    _write(
        output_dir / "impact-engine-contract.json",
        {
            "contract_version": "1.0.0",
            "engine_id": "chronosdb-impact-engine-v1.0.0",
            "request_contract": "chronosdb.impact.contracts.requests.ImpactRequest",
            "result_schema": "schemas/impact-result.schema.json",
            "baseline_mode": "DO_NOTHING",
            "input_state_immutable": True,
            "deterministic": True,
            "phase6_overlay_boundary": "intervention overlay must not mutate operational state",
        },
    )
    _write(
        output_dir / "rule-set-manifest.json",
        {
            "version": rules.version,
            "domain_model_version": rules.domain_model_version,
            "dataset_compatibility": list(rules.dataset_compatibility),
            "rules": [rule.__dict__ for rule in rules.rules],
        },
    )
    _write(output_dir / "golden-impact-result.json", first)
    _write(
        output_dir / "benchmark-summary.json",
        _read(root / "artifacts" / "phase-5" / "impact-benchmark-results.json"),
    )
    _write(
        output_dir / "determinism-report.json",
        {
            "status": "PASS" if first == second else "FAIL",
            "state_hash": state.identity.state_hash,
            "first_result_hash": first["result_hash"],
            "second_result_hash": second["result_hash"],
            "same_result": first == second,
            "canonical_result_hash": canonical_hash(
                {key: value for key, value in first.items() if key != "result_hash"}
            ),
        },
    )
    _write(
        output_dir / "performance-report.json",
        {
            "performance_artifacts": [
                f"artifacts/phase-5/performance/{scale}-performance.json"
                for scale in ("tiny", "demo", "standard", "stress")
            ],
            "report": "artifacts/phase-5/performance/performance-report.md",
            "memory": "artifacts/phase-5/performance/memory.json",
        },
    )
    _write(
        output_dir / "error-catalogue.json",
        {
            "errors": [
                {
                    "code": "INVALID_CONTRACT",
                    "exception": "ContractError",
                    "terminal_status": "REJECTED",
                },
                {
                    "code": "INVALID_DISRUPTION",
                    "exception": "DisruptionValidationError",
                    "terminal_status": "REJECTED",
                },
                {
                    "code": "INSUFFICIENT_STATE",
                    "exception": "StateReconstructionError",
                    "terminal_status": "REJECTED or PARTIALLY_COMPLETED",
                },
                {
                    "code": "PERSISTENCE_FAILURE",
                    "exception": "PersistenceError",
                    "terminal_status": "FAILED",
                },
            ]
        },
    )
    _write(
        output_dir / "causal-trace-schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["trace_id", "target", "nodes", "edges", "rule_version", "state_hash"],
            "properties": {
                "trace_id": {"type": "string"},
                "target": {"type": "object"},
                "attribution": {"type": "string"},
                "nodes": {"type": "array", "items": {"type": "object"}},
                "edges": {"type": "array", "items": {"type": "object"}},
                "rule_version": {"type": "string"},
                "state_hash": {"type": "string"},
                "source_record_ids": {"type": "array", "items": {"type": "string"}},
            },
        },
    )
    completion = [
        "# Phase 5 Completion Report",
        "",
        "## Release",
        "",
        "- Engine: `chronosdb-impact-engine-v1.0.0`",
        f"- State hash: `{state.identity.state_hash}`",
        f"- Golden result hash: `{first['result_hash']}`",
        f"- Rule set: `{rules.version}`",
        "- Baseline: `DO_NOTHING`",
        "",
        "## Phase 6 handoff",
        "",
        "Phase 6 may reuse this deterministic core and apply isolated transfer, "
        "expedition, alternate-supplier, rescheduling, and hybrid overlays. The "
        "operational state, disruption, horizon, policies, and rule set remain "
        "the comparison identity for every candidate.",
        "",
        "The handoff package contains the frozen result, contract, rules, benchmark "
        "summary, determinism evidence, performance references, error catalogue, "
        "and causal trace schema.",
    ]
    (output_dir / "phase-5-completion-report.md").write_text(
        "\n".join(completion) + "\n",
        encoding="utf-8",
    )
    return first


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = run(args.root)
    print(f"Phase 5 handoff built from {result['result_hash']}")


if __name__ == "__main__":
    main()
