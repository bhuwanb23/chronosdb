from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from chronosdb.impact.contracts.requests import SimulationHorizon
from chronosdb.impact.disruption import Disruption
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.persistence import ExecutionLedger
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor

ROOT = Path(__file__).resolve().parents[3]
AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)
END = AS_OF + timedelta(days=30)


def _inputs():
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    disruption = Disruption.from_state(state, "EVT-GOLD-001")
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    return state, disruption, SimulationHorizon(AS_OF, END), rules


def test_pipeline_preserves_golden_headline_and_rule_version() -> None:
    state, disruption, horizon, rules = _inputs()
    result = calculate_impact(
        state, disruption, horizon, rules, scenario_id="SCN-GOLD-001"
    ).to_dict()
    assert result["status"] == "COMPLETED"
    assert result["rule_set_version"] == "impact-rules-v1.0.0"
    assert result["input_state_hash"] == state.identity.state_hash
    assert result["headline_metrics"]["sla_breached_customer_order_count"] == 2
    assert result["headline_metrics"]["revenue_at_risk"] == {
        "amount": "1600000.00",
        "currency": "INR",
    }


def test_same_fingerprint_returns_immutable_ledger_result() -> None:
    state, disruption, horizon, rules = _inputs()
    ledger = ExecutionLedger()
    first = calculate_impact(
        state,
        disruption,
        horizon,
        rules,
        scenario_id="SCN-GOLD-001",
        ledger=ledger,
    )
    second = calculate_impact(
        state,
        disruption,
        horizon,
        rules,
        scenario_id="SCN-GOLD-001",
        ledger=ledger,
    )
    assert first.result_hash == second.result_hash
    assert len(ledger.all()) == 1
    assert ledger.all()[0].status == "COMPLETED"


def test_calculation_does_not_mutate_release_inputs() -> None:
    state, disruption, horizon, rules = _inputs()
    before = json.dumps(
        {name: list(rows) for name, rows in state.records.items()},
        sort_keys=True,
    )
    calculate_impact(state, disruption, horizon, rules, scenario_id="SCN-GOLD-001")
    after = json.dumps(
        {name: list(rows) for name, rows in state.records.items()},
        sort_keys=True,
    )
    assert before == after


def test_rule_set_has_explicit_versions_and_inputs() -> None:
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    assert rules.version == "impact-rules-v1.0.0"
    assert rules.domain_model_version
    for rule in rules.rules:
        assert rule.rule_id
        assert rule.version
        assert rule.inputs
        assert rule.outputs
        assert rule.rounding
