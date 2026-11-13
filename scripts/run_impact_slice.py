"""Run the deterministic Phase 5A–5G golden supply-impact slice."""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from chronosdb.impact.contracts import SimulationHorizon
from chronosdb.impact.contracts.requests import parse_time
from chronosdb.impact.contracts.results import canonical_hash
from chronosdb.impact.disruption import (
    Disruption,
    resolve_purchase_order_impacts,
    validate_disruption,
)
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor
from chronosdb.impact.supply import project_receipts

ROOT = Path(__file__).resolve().parents[1]


def _validate_result_artifact(result: dict[str, object]) -> None:
    schema = json.loads(
        (ROOT / "schemas" / "impact-result.schema.json").read_text(encoding="utf-8")
    )
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(result),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise RuntimeError(f"impact result schema validation failed: {errors[0].message}")
    expected_hash = result["result_hash"]
    actual_hash = canonical_hash(
        {key: value for key, value in result.items() if key != "result_hash"}
    )
    if expected_hash != actual_hash:
        raise RuntimeError("impact result hash validation failed")


def run() -> dict[str, object]:
    scenario = json.loads(
        (ROOT / "data" / "releases" / "v1.0.0" / "golden" / "scenario.json").read_text(
            encoding="utf-8"
        )
    )
    as_of = parse_time(scenario["as_of_time"])
    horizon = SimulationHorizon(as_of, as_of + timedelta(days=30))
    state = ReleaseStateReconstructor(ROOT).reconstruct(as_of)
    disruption = Disruption.from_state(state, scenario["event_id"])
    validate_disruption(disruption)
    impacts = resolve_purchase_order_impacts(state, disruption)
    receipts = project_receipts(impacts, horizon)
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    result = calculate_impact(
        state, disruption, horizon, rules, scenario_id=scenario["scenario_id"]
    ).to_dict()
    artifact_root = ROOT / "artifacts" / "phase-5"
    artifact_root.mkdir(parents=True, exist_ok=True)
    no_duplicate_event_ids = len({receipt.event_id for receipt in receipts}) == len(receipts)
    state_report = {
        "status": "PASS" if not state.warnings else "WARN",
        "state_identity": state.identity.__dict__,
        "record_counts": {name: len(rows) for name, rows in state.records.items()},
        "warnings": list(state.warnings),
    }
    disruption_report = {
        "status": "PASS",
        "event_id": disruption.event_id,
        "purchase_order_impacts": [impact.to_dict() for impact in impacts],
    }
    supply_report = {
        "status": "PASS" if no_duplicate_event_ids else "FAIL",
        "projected_receipts": [receipt.to_dict() for receipt in receipts],
        "no_duplicate_event_ids": no_duplicate_event_ids,
    }
    validation_errors = [] if no_duplicate_event_ids else ["duplicate projected receipt event IDs"]
    if validation_errors:
        result["errors"] = validation_errors
        result["result_hash"] = canonical_hash(
            {key: value for key, value in result.items() if key != "result_hash"}
        )
    _validate_result_artifact(result)
    for name, payload in (
        ("state-reconstruction.json", state_report),
        ("disruption-resolution.json", disruption_report),
        ("supply-projection.json", supply_report),
        ("golden-impact-slice.json", result),
    ):
        (artifact_root / name).write_text(
            json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8",
        )
    return result


if __name__ == "__main__":
    output = run()
    print(f"Phase 5A–5G impact slice: {output['status']}")
    if output["errors"]:
        raise SystemExit(1)
