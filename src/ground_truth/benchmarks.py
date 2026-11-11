"""Deterministic benchmark expected-outcome construction."""

from __future__ import annotations

from decimal import Decimal
from typing import Any


def expected_for_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    """Emit a complete, conservative expected-output envelope."""
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
    optimal: list[str] = []
    if no_impact:
        breaches = 0
        risk = Decimal("0")
        recommendation = None
    elif insufficient or no_feasible:
        breaches = None
        risk = None
        optimal = []
        recommendation = None
    elif category == "TIE_OR_PARETO_EQUIVALENT":
        breaches = 0
        risk = Decimal("0")
        optimal = ["INT-TIE-TRANSFER", "INT-TIE-ALTERNATE"]
        recommendation = None
    else:
        breaches = 0
        risk = Decimal("0")
        optimal = [f"{scenario['id']}-HYBRID"]
        recommendation = optimal[0]
    number = scenario["id"].split("-")[-1]
    candidate_ids = [
        f"INT-{number}-{candidate}"
        for candidate in ("TRANSFER", "ALTERNATE_SUPPLY", "HYBRID")
    ]
    budget = Decimal("50000") if category == "BUDGET_CONSTRAINED_RECOVERY" else Decimal("200000")
    costs = {
        candidate_ids[0]: Decimal("60000"),
        candidate_ids[1]: Decimal("72000"),
        candidate_ids[2]: Decimal("132000"),
    }
    feasibility = {
        candidate_id: (cost <= budget and not no_feasible and not insufficient)
        for candidate_id, cost in costs.items()
    }
    if category == "BUDGET_CONSTRAINED_RECOVERY":
        optimal = []
        recommendation = None
        validity = "NO_FEASIBLE_INTERVENTION"
    if category == "TIE_OR_PARETO_EQUIVALENT":
        optimal = [candidate_ids[0], candidate_ids[1]]
    if recommendation is not None:
        recommendation = candidate_ids[2]
    return {
        "scenario_id": scenario["id"],
        "expected_validity": validity,
        "expected_affected_components": [] if no_impact else [scenario["reference_component_id"]],
        "expected_shortages": [] if no_impact else ["shortage_from_scenario"],
        "expected_affected_production_orders": [] if no_impact else ["production_from_scenario"],
        "expected_affected_customer_orders": [] if no_impact else ["customer_from_scenario"],
        "expected_sla_breaches": breaches,
        "expected_revenue_at_risk_inr": str(risk) if risk is not None else None,
        "expected_candidate_feasibility": feasibility,
        "expected_candidate_metrics": {
            candidate_id: {"intervention_cost_inr": str(costs[candidate_id])}
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
