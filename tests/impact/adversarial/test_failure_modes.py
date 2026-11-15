from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from chronosdb.impact.contracts.errors import DisruptionValidationError
from chronosdb.impact.contracts.requests import SimulationHorizon
from chronosdb.impact.disruption import (
    Disruption,
    resolve_purchase_order_impacts,
    validate_disruption,
)
from chronosdb.impact.disruption.validation import validate_disruption_against_state
from chronosdb.impact.fulfilment import (
    CustomerImpact,
    FulfilmentSegment,
    calculate_sla_and_financial_impact,
)
from chronosdb.impact.materials import build_material_requirements
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor

ROOT = Path(__file__).resolve().parents[3]
AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)
END = AS_OF + timedelta(days=30)


def _golden_state_and_disruption():
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    return state, Disruption.from_state(state, "EVT-GOLD-001")


def test_unknown_supplier_is_rejected() -> None:
    state, disruption = _golden_state_and_disruption()
    unknown = replace(disruption, supplier_id="SUP-DOES-NOT-EXIST")
    with pytest.raises(DisruptionValidationError, match="unknown supplier"):
        validate_disruption_against_state(state, unknown)


def test_invalid_disruption_interval_is_rejected() -> None:
    state, disruption = _golden_state_and_disruption()
    invalid = replace(disruption, end_time=disruption.start_time)
    with pytest.raises(DisruptionValidationError):
        validate_disruption(invalid)


def test_fully_received_supplier_has_no_affected_purchase_orders() -> None:
    state, _ = _golden_state_and_disruption()
    disruption = Disruption(
        event_id="EVT-NO-IMPACT",
        event_type="SUPPLIER_OUTAGE",
        supplier_id="SUP-0208",
        start_time=AS_OF,
        end_time=AS_OF + timedelta(days=2),
        recovery_lag=timedelta(days=1),
        scope_type="ALL_SUPPLY",
    )
    assert resolve_purchase_order_impacts(state, disruption) == ()


def test_missing_bom_is_reported_as_data_quality_issue() -> None:
    state, _ = _golden_state_and_disruption()
    no_bom = replace(state, records={**state.records, "bom_versions": ()})
    issues = []
    requirements = build_material_requirements(
        no_bom,
        AS_OF,
        END,
        quality_issues=issues,
    )
    assert requirements == ()
    assert issues
    assert issues[0].code == "MISSING_ACTIVE_BOM"
    assert issues[0].severity.value == "CRITICAL_FOR_ENTITY"


def _customer_impact(projected: datetime) -> CustomerImpact:
    return CustomerImpact(
        customer_order_id="CO-TEST",
        customer_order_line_id="COL-TEST-01",
        production_order_id="MO-TEST",
        product_id="PRD-TEST",
        open_quantity=Decimal("10"),
        promised_delivery=datetime(2026, 11, 10, tzinfo=UTC),
        unit_revenue=Decimal("100"),
        segments=(
            FulfilmentSegment(
                order_line_id="COL-TEST-01",
                quantity=Decimal("10"),
                availability_time=projected,
                projected_delivery=projected,
                production_batch_id="MO-TEST-B01",
                facility_id="FAC-TEST",
            ),
        ),
    )


def test_pre_existing_lateness_is_not_attributed_to_disruption() -> None:
    impact = _customer_impact(datetime(2026, 11, 12, tzinfo=UTC))
    results, _ = calculate_sla_and_financial_impact(
        (impact,),
        baseline_delivery_by_production_order={
            "MO-TEST": datetime(2026, 11, 12, tzinfo=UTC)
        },
        as_of=AS_OF,
    )
    assert results[0].status == "BREACHED"
    assert results[0].attribution == "PRE_EXISTING"


def test_disruption_worsening_of_existing_lateness_is_labelled() -> None:
    impact = _customer_impact(datetime(2026, 11, 12, tzinfo=UTC))
    results, _ = calculate_sla_and_financial_impact(
        (impact,),
        baseline_delivery_by_production_order={
            "MO-TEST": datetime(2026, 11, 11, tzinfo=UTC)
        },
        as_of=AS_OF,
    )
    assert results[0].attribution == "DISRUPTION_WORSENED"


def test_golden_pipeline_still_completes_after_validation_changes() -> None:
    state, disruption = _golden_state_and_disruption()
    result = calculate_impact(
        state,
        disruption,
        SimulationHorizon(AS_OF, END),
        load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml"),
        scenario_id="SCN-GOLD-001",
    ).to_dict()
    assert result["status"] == "COMPLETED"
    assert result["headline_metrics"]["revenue_at_risk"]["amount"] == "1600000.00"
