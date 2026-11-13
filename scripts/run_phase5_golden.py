"""Run and freeze the complete Phase 5 do-nothing golden result."""

from __future__ import annotations

import argparse
import json
from datetime import timedelta
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from chronosdb.impact.contracts.requests import SimulationHorizon, parse_time
from chronosdb.impact.contracts.results import canonical_hash
from chronosdb.impact.disruption import Disruption, validate_disruption
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor

ROOT = Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_result(root: Path, result: dict[str, Any]) -> None:
    schema = _read_json(root / "schemas" / "impact-result.schema.json")
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(result),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise RuntimeError(f"golden result schema validation failed: {errors[0].message}")
    expected_hash = canonical_hash(
        {key: value for key, value in result.items() if key != "result_hash"}
    )
    if result["result_hash"] != expected_hash:
        raise RuntimeError("golden result hash validation failed")


def _checks(result: dict[str, Any], expected: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = result["headline_metrics"]
    checks = [
        (
            "breached_customer_order_count",
            metrics["breached_customer_order_count"],
            expected["breached_customer_orders"],
        ),
        (
            "late_quantity",
            metrics["late_quantity"],
            str(sum(line["late_quantity"] for line in expected["customer_lines"])),
        ),
        (
            "total_delay_unit_hours",
            metrics["total_delay_unit_hours"],
            str(expected["total_delay_hours"]),
        ),
        ("revenue_at_risk", metrics["revenue_at_risk"]["amount"], expected["revenue_at_risk_inr"]),
        (
            "affected_purchase_orders",
            [row["purchase_order_id"] for row in result["affected_purchase_orders"]],
            ["PO-2208"],
        ),
        ("affected_components", result["affected_components"], ["CMP-MCU-42"]),
        (
            "affected_production_orders",
            [row["production_order_id"] for row in result["affected_production_orders"]],
            ["MO-0882", "MO-0889"],
        ),
        (
            "affected_customer_orders",
            [row["customer_order_id"] for row in result["affected_customer_orders"]],
            ["CO-0704", "CO-0711"],
        ),
        (
            "causal_trace_count",
            len(result["causal_traces"]),
            len(expected["customer_lines"]) - 1,
        ),
    ]
    return [
        {
            "name": name,
            "actual": actual,
            "expected": wanted,
            "status": "PASS" if actual == wanted else "FAIL",
        }
        for name, actual, wanted in checks
    ]


def run(root: Path = ROOT) -> dict[str, Any]:
    scenario = _read_json(root / "data" / "golden" / "scenario.json")
    expected = _read_json(root / "data" / "golden" / "expected_do_nothing.json")
    as_of = parse_time(scenario["as_of_time"])
    horizon = SimulationHorizon(as_of, as_of + timedelta(days=30))
    state = ReleaseStateReconstructor(root).reconstruct(as_of)
    disruption = Disruption.from_state(state, "EVT-GOLD-001")
    validate_disruption(disruption)
    rules = load_rule_set(root / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    result = calculate_impact(
        state,
        disruption,
        horizon,
        rules,
        scenario_id=scenario["scenario_id"],
    ).to_dict()
    _validate_result(root, result)
    checks = _checks(result, expected)
    if any(check["status"] == "FAIL" for check in checks):
        failed = ", ".join(check["name"] for check in checks if check["status"] == "FAIL")
        raise RuntimeError(f"golden comparison failed: {failed}")

    artifact_dir = root / "artifacts" / "phase-5"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "golden-impact-result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_lines = [
        "# Phase 5 Golden Comparison",
        "",
        f"- Scenario: `{scenario['scenario_id']}`",
        f"- State hash: `{state.identity.state_hash}`",
        f"- Rule set: `{rules.version}`",
        f"- Result hash: `{result['result_hash']}`",
        "",
        "All frozen checks passed:",
        "",
    ]
    report_lines.extend(
        f"- `{check['name']}`: `{check['actual']}`"
        for check in checks
    )
    (artifact_dir / "golden-comparison-report.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = run(args.root)
    print(f"Phase 5 golden result: {result['result_hash']}")


if __name__ == "__main__":
    main()
