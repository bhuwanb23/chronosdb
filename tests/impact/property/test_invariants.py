from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from chronosdb.impact.contracts.requests import SimulationHorizon
from chronosdb.impact.disruption import Disruption, resolve_purchase_order_impacts
from chronosdb.impact.fulfilment import (
    baseline_deliveries,
    build_customer_fulfilment,
    calculate_sla_and_financial_impact,
)
from chronosdb.impact.inventory import build_inventory_timelines, detect_shortages
from chronosdb.impact.materials import allocate_materials, build_material_requirements
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.production import schedule_production
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor
from chronosdb.impact.supply import project_receipts

ROOT = Path(__file__).resolve().parents[3]
AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)
END = AS_OF + timedelta(days=30)


def _pieces():
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    disruption = Disruption.from_state(state, "EVT-GOLD-001")
    impacts = resolve_purchase_order_impacts(state, disruption)
    receipts = project_receipts(impacts, SimulationHorizon(AS_OF, END))
    timelines = build_inventory_timelines(state, SimulationHorizon(AS_OF, END), receipts)
    requirements = build_material_requirements(state, AS_OF, END)
    allocations = allocate_materials(requirements, timelines)
    shortages = detect_shortages(allocations, END)
    production = schedule_production(
        state, requirements, allocations, SimulationHorizon(AS_OF, END)
    )
    customer = build_customer_fulfilment(
        state, production, SimulationHorizon(AS_OF, END)
    )
    sla, metrics = calculate_sla_and_financial_impact(
        customer,
        disruption_caused_production_order_ids={
            shortage.production_order_id for shortage in shortages
        },
        horizon_end=END,
        baseline_delivery_by_production_order=baseline_deliveries(production),
        as_of=AS_OF,
    )
    return state, timelines, requirements, allocations, production, customer, sla, metrics


def test_inventory_conservation_for_every_timeline() -> None:
    _, timelines, *_ = _pieces()
    for timeline in timelines:
        assert timeline.ending_balance == timeline.opening_physical + sum(
            (event.delta for event in timeline.events), Decimal("0")
        )
        assert timeline.ending_available == timeline.opening_available + sum(
            (event.delta for event in timeline.events), Decimal("0")
        )


def test_allocation_never_exceeds_requirement() -> None:
    _, _, requirements, allocations, *_ = _pieces()
    assert len(requirements) == len(allocations)
    for allocation in allocations:
        assert allocation.allocated_quantity <= allocation.required_quantity
        assert allocation.shortage_quantity == max(
            Decimal("0"), allocation.required_quantity - allocation.allocated_quantity
        )


def test_customer_fulfilment_never_exceeds_open_quantity() -> None:
    *_, customer, _, _ = _pieces()
    for impact in customer:
        assert impact.fulfilled_quantity <= impact.open_quantity
        assert sum((segment.quantity for segment in impact.segments), Decimal("0")) <= (
            impact.open_quantity
        )


def test_revenue_at_risk_never_includes_on_time_quantity() -> None:
    *_, sla, metrics = _pieces()
    assert metrics["revenue_at_risk"]["currency"] == "INR"
    for result in sla:
        if result.revenue_at_risk is not None:
            assert result.revenue_at_risk == result.late_quantity * result.unit_revenue
            assert result.revenue_at_risk <= result.open_quantity * result.unit_revenue


def test_production_times_are_ordered() -> None:
    _, _, _, _, production, *_ = _pieces()
    for impact in production:
        for batch in impact.batches:
            if batch.projected_start is not None and batch.projected_completion is not None:
                assert batch.projected_completion >= batch.projected_start


def test_golden_pipeline_is_repeatable() -> None:
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    disruption = Disruption.from_state(state, "EVT-GOLD-001")
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    first = calculate_impact(
        state,
        disruption,
        SimulationHorizon(AS_OF, END),
        rules,
        scenario_id="SCN-GOLD-001",
    ).to_dict()
    second = calculate_impact(
        state,
        disruption,
        SimulationHorizon(AS_OF, END),
        rules,
        scenario_id="SCN-GOLD-001",
    ).to_dict()
    assert first == second
