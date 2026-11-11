from __future__ import annotations

from decimal import Decimal

from ground_truth.oracle import calculate_golden


def test_golden_outputs_are_locked() -> None:
    result = calculate_golden()
    assert result["do_nothing"]["breached_customer_orders"] == 2
    assert result["do_nothing"]["revenue_at_risk_inr"] == "1600000.00"
    hybrid = next(row for row in result["interventions"] if row["candidate_id"] == "INT-GOLD-C")
    assert hybrid["intervention_cost_inr"] == "132000"
    assert hybrid["breached_customer_orders"] == 0
    assert hybrid["revenue_protected_inr"] == "1600000.00"
    assert result["recommendation"]["recommended_intervention"] == "INT-GOLD-C"


def test_golden_costs_use_decimal_values() -> None:
    result = calculate_golden()
    hybrid = next(row for row in result["interventions"] if row["candidate_id"] == "INT-GOLD-C")
    assert Decimal(hybrid["intervention_cost_inr"]) <= Decimal("200000")
