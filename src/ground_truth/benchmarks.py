"""Deterministic benchmark expected-outcome construction."""

from __future__ import annotations

from decimal import Decimal
from typing import Any


def expected_for_scenario(
    scenario: dict[str, Any],
    candidates: list[dict[str, Any]],
    costs: list[dict[str, Any]],
    constraint: dict[str, Any],
) -> dict[str, Any]:
    """Emit an expected-output envelope from scenario candidate inputs."""
    category = scenario["category"]
    insufficient = category == "INSUFFICIENT_CRITICAL_DATA"
    no_impact = category == "NO_OPERATIONAL_IMPACT"
    no_feasible = category == "NO_FEASIBLE_INTERVENTION"
    if insufficient:
        validity = "INSUFFICIENT_DATA"
        quality = "PARTIAL_CRITICAL"
    elif no_feasible:
        validity = "NO_FEASIBLE_INTERVENTION"
        quality = "COMPLETE"
    else:
        validity = "VALID"
        quality = "COMPLETE"
    candidate_ids = [candidate["id"] for candidate in candidates]
    cost_rows = {row["candidate_id"]: row for row in costs}
    budget = Decimal(str(constraint["maximum_recovery_budget_inr"]))
    quantities = {
        candidate["id"]: Decimal(str(candidate["quantity"])) for candidate in candidates
    }
    cost_values = {
        candidate_id: Decimal(str(cost_rows[candidate_id]["fixed_transfer_cost_inr"]))
        + Decimal(str(cost_rows[candidate_id]["variable_transfer_cost_per_unit_inr"]))
        * quantities[candidate_id]
        + Decimal(str(cost_rows[candidate_id]["alternate_supplier_premium_inr"]))
        + Decimal(str(cost_rows[candidate_id]["rescheduling_cost_inr"]))
        for candidate_id in candidate_ids
    }
    feasibility = {
        candidate_id: (
            cost_values[candidate_id] <= budget
            and not no_feasible
            and not insufficient
            and candidate["approval_status"] == "APPROVED"
        )
        for candidate_id, candidate in ((row["id"], row) for row in candidates)
    }
    feasible = [candidate_id for candidate_id in candidate_ids if feasibility[candidate_id]]
    if no_impact or insufficient or no_feasible or not feasible:
        breaches = 0 if no_impact else None
        risk = Decimal("0") if no_impact else None
        optimal = []
        recommendation = None
    elif category == "TIE_OR_PARETO_EQUIVALENT":
        breaches = 0
        risk = Decimal("0")
        optimal = feasible
        recommendation = None
    else:
        breaches = 0
        risk = Decimal("0")
        minimum_cost = min(cost_values[candidate_id] for candidate_id in feasible)
        optimal = [
            candidate_id
            for candidate_id in feasible
            if cost_values[candidate_id] == minimum_cost
        ]
        recommendation = optimal[0]
    return {
        "scenario_id": scenario["id"],
        "expected_validity": validity,
        "expected_affected_components": [] if no_impact else [scenario["reference_component_id"]],
        "expected_shortages": [] if no_impact else [scenario["reference_component_id"]],
        "expected_affected_production_orders": (
            [] if no_impact else [scenario["reference_production_order_id"]]
        ),
        "expected_affected_customer_orders": (
            [] if no_impact else [scenario["reference_customer_order_id"]]
        ),
        "expected_sla_breaches": breaches,
        "expected_revenue_at_risk_inr": str(risk) if risk is not None else None,
        "expected_candidate_feasibility": feasibility,
        "expected_candidate_metrics": {
            candidate_id: {"intervention_cost_inr": str(cost_values[candidate_id])}
            for candidate_id in candidate_ids
        },
        "expected_optimal_set": optimal,
        "expected_recommendation": recommendation,
        "expected_data_quality_state": quality,
        "expected_causal_trace_roots": [] if no_impact or insufficient else ["DISRUPTION_EVENT"],
        "provenance": {
            "scenario_id": scenario["id"],
            "formula_version": "2.0",
            "oracle_version": "0.1.0",
            "reference_case": "NO_DISRUPTION_BASELINE",
            "unit": "INR",
        },
    }


def build_partitions(scenario_ids: list[str]) -> dict[str, list[str]]:
    """Freeze exclusive development, validation, test, golden, and adversarial sets."""
    return {
        "development": scenario_ids[:24],
        "validation": scenario_ids[24:36],
        "test": scenario_ids[36:54],
        "golden": ["SCN-GOLD-001", "SCN-GOLD-002", "SCN-GOLD-003"],
        "adversarial": scenario_ids[54:57],
    }
