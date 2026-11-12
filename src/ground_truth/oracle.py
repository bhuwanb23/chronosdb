"""Transparent Phase 3L/3N oracle for the locked golden scenario."""

from __future__ import annotations

from decimal import Decimal
from typing import Any


def golden_scenario() -> dict[str, Any]:
    """Return the corrected Phase 2 golden input state."""
    return {
        "scenario_id": "SCN-GOLD-001",
        "as_of_time": "2026-11-11T02:30:00Z",
        "objective_mode": "MINIMIZE_SLA_BREACHES",
        "budget_inr": "200000.00",
        "component_id": "CMP-MCU-42",
        "product_id": "PRD-CONTROLLER-X",
        "supplier_id": "S-104",
        "disruption": {
            "id": "DIS-GOLD-S104",
            "event_type": "SUPPLIER_OUTAGE",
            "supplier_id": "S-104",
            "start_time": "2026-11-11T02:30:00Z",
            "end_time": "2026-11-25T02:30:00Z",
            "recovery_lag_days": 2,
        },
        "bom_quantity_per_product": 2,
        "pune_inventory": 400,
        "pune_safety_stock": 100,
        "chennai_inventory": 700,
        "chennai_committed_demand": 180,
        "chennai_safety_stock": 120,
        "transferable_quantity": 400,
        "purchase_order_id": "PO-2208",
        "purchase_order_quantity": 800,
        "disrupted_arrival": "2026-11-27T00:00:00Z",
        "production_capacity_per_day": 100,
        "delivery_lead_time_days": 1,
        "unit_revenue_inr": "4000.00",
        "orders": [
            {
                "production_order_id": "MO-0876",
                "customer_order_id": "CO-0701",
                "quantity": 200,
                "promised_delivery": "2026-11-15T00:00:00Z",
            },
            {
                "production_order_id": "MO-0882",
                "customer_order_id": "CO-0704",
                "quantity": 200,
                "promised_delivery": "2026-11-18T00:00:00Z",
            },
            {
                "production_order_id": "MO-0889",
                "customer_order_id": "CO-0711",
                "quantity": 200,
                "promised_delivery": "2026-11-21T00:00:00Z",
            },
        ],
        "customer_order_lines": [
            {"id": "COL-CO-0701-01", "customer_order_id": "CO-0701", "quantity": 200},
            {"id": "COL-CO-0704-01", "customer_order_id": "CO-0704", "quantity": 200},
            {"id": "COL-CO-0711-01", "customer_order_id": "CO-0711", "quantity": 200},
        ],
    }


def _line_result(
    order: dict[str, Any],
    delivery: str,
    late_quantity: int,
    delay_days: int,
    unit_revenue_inr: str,
) -> dict[str, Any]:
    revenue = Decimal(str(late_quantity)) * Decimal(unit_revenue_inr)
    return {
        "customer_order_id": order["customer_order_id"],
        "production_order_id": order["production_order_id"],
        "projected_delivery": delivery,
        "promised_delivery": order["promised_delivery"],
        "late_quantity": late_quantity,
        "delay_hours": delay_days * 24,
        "revenue_at_risk_inr": str(revenue),
    }


def _outcome(
    name: str,
    lines: list[dict[str, Any]],
    intervention_cost: Decimal,
    reference_revenue_at_risk: Decimal,
) -> dict[str, Any]:
    breached = [line for line in lines if line["late_quantity"] > 0]
    revenue_at_risk = sum((Decimal(line["revenue_at_risk_inr"]) for line in lines), Decimal("0"))
    total_delay = sum(line["late_quantity"] * line["delay_hours"] for line in lines)
    return {
        "candidate_id": name,
        "customer_lines": lines,
        "breached_customer_orders": len(breached),
        "revenue_at_risk_inr": str(revenue_at_risk),
        "total_delay_hours": total_delay,
        "intervention_cost_inr": str(intervention_cost),
        "revenue_protected_inr": str(
            max(Decimal("0"), reference_revenue_at_risk - revenue_at_risk)
        ),
        "net_protected_value_inr": str(
            max(Decimal("0"), reference_revenue_at_risk - revenue_at_risk)
            - intervention_cost
        ),
    }


def _validate_golden_state(scenario: dict[str, Any]) -> dict[str, Any]:
    transferable = (
        scenario["chennai_inventory"]
        - scenario["chennai_committed_demand"]
        - scenario["chennai_safety_stock"]
    )
    required = scenario["orders"][0]["quantity"] * scenario["bom_quantity_per_product"]
    if transferable != scenario["transferable_quantity"]:
        raise ValueError("golden transferable quantity is not conserved")
    if required != 400 or scenario["pune_inventory"] - required != 0:
        raise ValueError("golden opening material state is inconsistent")
    return {
        "transferable_quantity": transferable,
        "required_quantity_per_production_order": required,
        "transfer_arrival": "2026-11-13T00:00:00Z",
        "alternate_arrival": "2026-11-16T00:00:00Z",
        "disrupted_receipt": scenario["disrupted_arrival"],
    }


def calculate_golden() -> dict[str, Any]:
    """Calculate baseline, do-nothing, candidates, and causal traces."""
    scenario = golden_scenario()
    intermediate = _validate_golden_state(scenario)
    orders = scenario["orders"]
    baseline_lines = [
        _line_result(order, promised, 0, 0, scenario["unit_revenue_inr"])
        for order in orders
        for promised in [order["promised_delivery"]]
    ]
    do_nothing_lines = [
        _line_result(orders[0], "2026-11-15T00:00:00Z", 0, 0, scenario["unit_revenue_inr"]),
        _line_result(orders[1], "2026-11-30T00:00:00Z", 200, 12, scenario["unit_revenue_inr"]),
        _line_result(orders[2], "2026-12-02T00:00:00Z", 200, 11, scenario["unit_revenue_inr"]),
    ]
    one_order_late = [
        _line_result(orders[0], "2026-11-15T00:00:00Z", 0, 0, scenario["unit_revenue_inr"]),
        _line_result(orders[1], "2026-11-18T00:00:00Z", 0, 0, scenario["unit_revenue_inr"]),
        _line_result(orders[2], "2026-12-02T00:00:00Z", 200, 11, scenario["unit_revenue_inr"]),
    ]
    alternate_lines = [
        _line_result(orders[0], "2026-11-15T00:00:00Z", 0, 0, scenario["unit_revenue_inr"]),
        _line_result(orders[1], "2026-11-19T00:00:00Z", 200, 1, scenario["unit_revenue_inr"]),
        _line_result(orders[2], "2026-12-02T00:00:00Z", 200, 11, scenario["unit_revenue_inr"]),
    ]
    do_nothing_reference = sum(
        (Decimal(line["revenue_at_risk_inr"]) for line in do_nothing_lines),
        Decimal("0"),
    )
    outcomes = {
        "baseline": _outcome("BASELINE", baseline_lines, Decimal("0"), Decimal("0")),
        "do_nothing": _outcome("DO-NOTHING", do_nothing_lines, Decimal("0"), do_nothing_reference),
        "INT-GOLD-A": _outcome(
            "INT-GOLD-A", one_order_late, Decimal("60000"), do_nothing_reference
        ),
        "INT-GOLD-B": _outcome(
            "INT-GOLD-B", alternate_lines, Decimal("72000"), do_nothing_reference
        ),
        "INT-GOLD-C": _outcome(
            "INT-GOLD-C",
            [
                _line_result(orders[0], "2026-11-15T00:00:00Z", 0, 0, scenario["unit_revenue_inr"]),
                _line_result(orders[1], "2026-11-18T00:00:00Z", 0, 0, scenario["unit_revenue_inr"]),
                _line_result(orders[2], "2026-11-21T00:00:00Z", 0, 0, scenario["unit_revenue_inr"]),
            ],
            Decimal("132000"),
            do_nothing_reference,
        ),
    }
    traces = [
        {
            "trace_id": "CT-GOLD-CO-0704",
            "scenario_id": scenario["scenario_id"],
            "simulation_run_id": "SIM-GOLD-DO-NOTHING",
            "state_version": "STATE-GOLD-001",
            "rule_version": "2.0",
            "target": {
                "customer_order_line_id": "COL-CO-0704-01",
                "metric": "projected_delay_hours",
            },
            "steps": [
                {
                    "edge_id": "CE-001",
                    "source_type": "disruption_event",
                    "source_id": "DIS-GOLD-S104",
                    "output": "affected_purchase_order",
                    "rule_id": "DIS-001",
                },
                {
                    "edge_id": "CE-002",
                    "source_type": "purchase_order",
                    "source_id": "PO-2208",
                    "output": "delayed_receipt",
                    "rule_id": "DIS-002",
                },
                {
                    "edge_id": "CE-004",
                    "source_type": "inventory_and_requirement",
                    "source_id": "CMP-MCU-42",
                    "output": "shortage",
                    "rule_id": "INV-003",
                },
                {
                    "edge_id": "CE-006",
                    "source_type": "production_order",
                    "source_id": "MO-0882",
                    "output": "projected_completion",
                    "rule_id": "PROD-003",
                },
                {
                    "edge_id": "CE-008",
                    "source_type": "customer_order_line",
                    "source_id": "COL-CO-0704-01",
                    "output": "projected_delivery",
                    "rule_id": "SLA-001",
                },
            ],
            "result": {
                "value": 288,
                "unit": "hours",
                "reference_case": "DO-NOTHING",
                "evidence_status": "complete",
            },
        },
        {
            "trace_id": "CT-GOLD-CO-0711",
            "scenario_id": scenario["scenario_id"],
            "simulation_run_id": "SIM-GOLD-DO-NOTHING",
            "state_version": "STATE-GOLD-001",
            "rule_version": "2.0",
            "target": {
                "customer_order_line_id": "COL-CO-0711-01",
                "metric": "projected_delay_hours",
            },
            "steps": [
                {
                    "edge_id": "CE-001",
                    "source_type": "disruption_event",
                    "source_id": "DIS-GOLD-S104",
                    "output": "affected_purchase_order",
                    "rule_id": "DIS-001",
                },
                {
                    "edge_id": "CE-002",
                    "source_type": "purchase_order",
                    "source_id": "PO-2208",
                    "output": "delayed_receipt",
                    "rule_id": "DIS-002",
                },
                {
                    "edge_id": "CE-004",
                    "source_type": "inventory_and_requirement",
                    "source_id": "CMP-MCU-42",
                    "output": "shortage",
                    "rule_id": "INV-003",
                },
                {
                    "edge_id": "CE-006",
                    "source_type": "production_order",
                    "source_id": "MO-0889",
                    "output": "projected_completion",
                    "rule_id": "PROD-003",
                },
                {
                    "edge_id": "CE-008",
                    "source_type": "customer_order_line",
                    "source_id": "COL-CO-0711-01",
                    "output": "projected_delivery",
                    "rule_id": "SLA-001",
                },
            ],
            "result": {
                "value": 264,
                "unit": "hours",
                "reference_case": "DO-NOTHING",
                "evidence_status": "complete",
            },
        },
    ]
    return {
        "scenario": scenario,
        "intermediate_calculations": intermediate,
        "baseline": outcomes["baseline"],
        "do_nothing": outcomes["do_nothing"],
        "interventions": [
            outcomes["INT-GOLD-A"],
            outcomes["INT-GOLD-B"],
            outcomes["INT-GOLD-C"],
        ],
        "recommendation": {
            "objective_mode": scenario["objective_mode"],
            "recommended_intervention": "INT-GOLD-C",
            "expected_optimal_set": ["INT-GOLD-C"],
            "hard_constraints_satisfied": True,
        },
        "causal_traces": traces,
        "provenance": {
            "scenario_id": scenario["scenario_id"],
            "oracle_version": "0.1.0",
            "formula_version": "2.0",
            "reference_case": "NO_DISRUPTION_BASELINE",
            "unit": "INR",
        },
    }
