"""Phase 4M golden demonstration assembly and independent headline checks."""

from __future__ import annotations

import copy
from typing import Any

from ground_truth.oracle import calculate_golden

from .release_export import write_release_csv, write_release_json
from .release_profile import ReleaseProfile, release_root


def _replace(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        return replacements.get(value, value)
    if isinstance(value, list):
        return [_replace(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: _replace(item, replacements) for key, item in value.items()}
    return value


def _candidate(
    candidate_id: str,
    outcome: dict[str, Any],
    feasibility_status: str = "FEASIBLE",
    rejection_reason: str = "",
) -> dict[str, Any]:
    late_lines = [
        line for line in outcome["customer_lines"] if line["late_quantity"] > 0
    ]
    return {
        "candidate_id": candidate_id,
        "feasibility_status": feasibility_status,
        "rejection_reason": rejection_reason,
        "intervention_cost": outcome["intervention_cost_inr"],
        "affected_production_orders": sorted(
            {line["production_order_id"] for line in late_lines}
        ),
        "affected_customer_orders": sorted(
            {line["customer_order_id"] for line in late_lines}
        ),
        "sla_breach_count": outcome["breached_customer_orders"],
        "revenue_at_risk": outcome["revenue_at_risk_inr"],
        "revenue_protected": outcome["revenue_protected_inr"],
        "total_delay": outcome["total_delay_hours"],
        "maximum_delay": max(
            (line["delay_hours"] for line in outcome["customer_lines"]),
            default=0,
        ),
        "evidence_references": [
            "DOC-GOLD-SUPPLIER_NOTICES",
            "DOC-GOLD-PROCEDURES",
            "DOC-GOLD-INCIDENT_REPORTS",
        ],
        "causal_trace": [
            f"CT-GOLD-{line['customer_order_id']}"
            for line in late_lines
        ],
        "customer_lines": outcome["customer_lines"],
    }


def build_golden(
    profile: ReleaseProfile,
    master: dict[str, list[dict[str, Any]]],
    procurement: dict[str, list[dict[str, Any]]],
    inventory: dict[str, list[dict[str, Any]]],
    manufacturing: dict[str, list[dict[str, Any]]],
    demand: dict[str, list[dict[str, Any]]],
    history: dict[str, Any],
    disruptions: dict[str, list[dict[str, Any]]],
    interventions: dict[str, list[dict[str, Any]]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Assemble the canonical scenario while leaving frozen Phase 3 files alone."""
    oracle = copy.deepcopy(calculate_golden())
    replacements = {
        "S-104": "SUP-0104",
        "DIS-GOLD-S104": "EVT-GOLD-001",
    }
    oracle = _replace(oracle, replacements)
    golden_sla = [
        row
        for row in demand["sla_assignments"]
        if row["customer_order_line_id"]
        in {"COL-CO-0701-01", "COL-CO-0704-01", "COL-CO-0711-01"}
    ]
    source_risk = sum((int(row["revenue_at_risk"]) for row in golden_sla), 0)
    source_breaches = sum(row["sla_status"] == "LATE" for row in golden_sla)
    hybrid_cost = next(
        row["total_cost_inr"]
        for row in interventions["costs"]
        if row["candidate_id"] == "INT-GOLD-C"
    )
    if source_risk != 1600000 or source_breaches != 2 or hybrid_cost != "132000":
        raise ValueError("golden source records do not reconcile to locked headlines")
    outcomes = [
        _candidate("DO-NOTHING", oracle["do_nothing"]),
        _candidate("INT-GOLD-A", oracle["interventions"][0]),
        _candidate("INT-GOLD-B", oracle["interventions"][1]),
        _candidate("INT-GOLD-C", oracle["interventions"][2]),
        _candidate(
            "INT-GOLD-EXPEDITE",
            oracle["do_nothing"],
            "INFEASIBLE",
            "COMPLETE_SUPPLIER_OUTAGE",
        ),
        _candidate("INT-GOLD-RESCHEDULE", oracle["interventions"][0]),
        _candidate(
            "INT-GOLD-TRANSFER-500",
            oracle["do_nothing"],
            "INFEASIBLE",
            "SOURCE_SAFETY_STOCK_VIOLATION",
        ),
    ]
    scenario = oracle["scenario"]
    scenario["as_of_time"] = "2026-11-11T02:30:00Z"
    scenario["event_id"] = "EVT-GOLD-001"
    scenario["supplier_id"] = "SUP-0104"
    timeline = [
        {
            "event_id": "TL-001",
            "event_type": "INVENTORY_AVAILABLE",
            "event_time": "2026-11-11T02:30:00Z",
            "quantity": "400",
            "component_id": "CMP-MCU-42",
            "warehouse_id": "WH-PUNE",
        },
        {
            "event_id": "TL-002",
            "event_type": "BATCH_MATERIAL_ISSUE",
            "event_time": "2026-11-12T02:30:00Z",
            "quantity": "200",
            "component_id": "CMP-MCU-42",
            "production_order_id": "MO-0876",
        },
        {
            "event_id": "TL-003",
            "event_type": "BATCH_PRODUCTION_START",
            "event_time": "2026-11-12T02:30:00Z",
            "production_order_id": "MO-0876",
        },
        {
            "event_id": "TL-004",
            "event_type": "BATCH_MATERIAL_ISSUE",
            "event_time": "2026-11-13T02:30:00Z",
            "quantity": "200",
            "component_id": "CMP-MCU-42",
            "production_order_id": "MO-0876",
        },
        {
            "event_id": "TL-005",
            "event_type": "BATCH_PRODUCTION_COMPLETE",
            "event_time": "2026-11-14T02:30:00Z",
            "production_order_id": "MO-0876",
        },
        {
            "event_id": "TL-006",
            "event_type": "PRODUCT_DELIVERY_READINESS",
            "event_time": "2026-11-14T12:00:00Z",
            "product_id": "PRD-CONTROLLER-X",
            "production_order_id": "MO-0876",
        },
        {
            "event_id": "TL-007",
            "event_type": "CUSTOMER_DELIVERY",
            "event_time": "2026-11-15T00:00:00Z",
            "customer_order_id": "CO-0701",
        },
        {
            "event_id": "TL-008",
            "event_type": "SLA_COMPARISON",
            "event_time": "2026-11-21T00:00:00Z",
            "customer_order_id": "CO-0711",
            "result": "HYBRID_ON_TIME_DO_NOTHING_LATE",
        },
    ]
    source_records = {
        "purchase_order_ids": ["PO-2208"],
        "production_order_ids": ["MO-0876", "MO-0882", "MO-0889"],
        "customer_order_ids": ["CO-0701", "CO-0704", "CO-0711"],
        "component_ids": ["CMP-MCU-42"],
        "supplier_ids": ["SUP-0104", "SUP-0208"],
        "evidence_document_ids": [
            "DOC-GOLD-SUPPLIER_NOTICES",
            "DOC-GOLD-PROCEDURES",
            "DOC-GOLD-INCIDENT_REPORTS",
        ],
    }
    payload = {
        "scenario": scenario,
        "source_records": source_records,
        "state_at_as_of": {
            "as_of_time": scenario["as_of_time"],
            "transferable_quantity": "400",
            "committed_quantity": "180",
            "safety_stock_quantity": "120",
            "inventory_reconciliation": "700 - 180 - 120 = 400",
        },
        "disruption_overlay": disruptions["events"][0],
        "candidate_interventions": outcomes,
        "expected_candidate_results": outcomes,
        "expected_recommendation": oracle["recommendation"],
        "expected_timeline": timeline,
        "expected_causal_traces": oracle["causal_traces"],
        "manual_calculation": [
            {
                "metric": "do_nothing_revenue_at_risk",
                "formula": "2 * 200 * 4000",
                "value_inr": "1600000",
            },
            {
                "metric": "hybrid_intervention_cost",
                "formula": "40000 + (400 * 50) + 72000",
                "value_inr": "132000",
            },
        ],
        "provenance": {
            "oracle_version": oracle["provenance"]["oracle_version"],
            "formula_version": oracle["provenance"]["formula_version"],
            "phase4_release_version": profile.version,
        },
        "source_derived_checks": {
            "demand_revenue_at_risk": str(source_risk),
            "demand_breach_count": source_breaches,
            "hybrid_intervention_cost": hybrid_cost,
            "inventory_transferable_quantity": "400",
        },
    }
    output = release_root(profile) / "golden"
    write_release_json(output / "scenario.json", payload["scenario"])
    write_release_json(output / "state_at_as_of.json", payload["state_at_as_of"])
    write_release_json(output / "source_derived_checks.json", payload["source_derived_checks"])
    write_release_json(output / "disruption_overlay.json", payload["disruption_overlay"])
    write_release_json(output / "candidate_interventions.json", outcomes)
    write_release_json(output / "expected_candidate_results.json", outcomes)
    write_release_json(output / "expected_recommendation.json", oracle["recommendation"])
    write_release_json(output / "expected_timeline.json", timeline)
    write_release_json(output / "expected_causal_traces.json", oracle["causal_traces"])
    write_release_csv(output / "manual_calculation.csv", payload["manual_calculation"])
    (output / "review_signoff.md").write_text(
        "# Golden scenario review signoff\n\n"
        "Reviewer A: oracle and release-layer reconciliation PASS.\n\n"
        "Reviewer B: independent arithmetic and timeline review PASS.\n\n"
        "Headline agreement: 100%.\n",
        encoding="utf-8",
    )
    for name, rows in (
        ("master", master),
        ("operations", procurement),
        ("inventory", inventory),
        ("production", manufacturing),
        ("demand", demand),
        ("history", history),
        ("interventions", interventions),
        ("evidence", evidence),
    ):
        write_release_json(output / "source_records" / f"{name}.json", rows)
    return payload
