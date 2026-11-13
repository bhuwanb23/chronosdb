"""Phase 4K intervention capability and cost generation."""

from __future__ import annotations

from typing import Any

from .release_export import write_release_csv
from .release_profile import ReleaseProfile, release_root


def build_interventions(
    profile: ReleaseProfile,
    inventory: dict[str, list[dict[str, Any]]],
    procurement: dict[str, list[dict[str, Any]]],
    manufacturing: dict[str, list[dict[str, Any]]],
    demand: dict[str, list[dict[str, Any]]],
    disruptions: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Materialize feasible and infeasible recovery capabilities."""
    transfers = [
        {
            "id": "INT-GOLD-A",
            "candidate_type": "TRANSFER",
            "source_warehouse_id": "WH-CHENNAI",
            "destination_warehouse_id": "WH-PUNE",
            "component_id": "CMP-MCU-42",
            "available_quantity": "400",
            "requested_quantity": "400",
            "dispatch_time": "2026-11-11T02:30:00Z",
            "lead_time_days": "2",
            "fixed_cost_inr": "40000",
            "variable_cost_per_unit_inr": "50",
            "safety_stock_protected": "true",
            "feasibility_status": "FEASIBLE",
            "rejection_reason": "",
        },
        {
            "id": "INT-GOLD-TRANSFER-500",
            "candidate_type": "TRANSFER",
            "source_warehouse_id": "WH-CHENNAI",
            "destination_warehouse_id": "WH-PUNE",
            "component_id": "CMP-MCU-42",
            "available_quantity": "400",
            "requested_quantity": "500",
            "dispatch_time": "2026-11-11T02:30:00Z",
            "lead_time_days": "2",
            "fixed_cost_inr": "40000",
            "variable_cost_per_unit_inr": "50",
            "safety_stock_protected": "false",
            "feasibility_status": "INFEASIBLE",
            "rejection_reason": "SOURCE_SAFETY_STOCK_VIOLATION",
        },
    ]
    expedites = [
        {
            "id": "INT-GOLD-EXPEDITE",
            "candidate_type": "EXPEDITE",
            "purchase_order_id": "PO-2208",
            "supplier_id": "SUP-0104",
            "component_id": "CMP-MCU-42",
            "eligible": "false",
            "earliest_achievable_arrival": "2026-11-27T02:30:00Z",
            "fixed_fee_inr": "15000",
            "variable_fee_inr": "0",
            "outage_compatible": "false",
            "rejection_reason": "COMPLETE_SUPPLIER_OUTAGE",
        },
        {
            "id": "INT-BENCH-EXPEDITE",
            "candidate_type": "EXPEDITE",
            "purchase_order_id": "PO-2208",
            "supplier_id": "SUP-0104",
            "component_id": "CMP-MCU-42",
            "eligible": "true",
            "earliest_achievable_arrival": "2026-11-13T02:30:00Z",
            "fixed_fee_inr": "15000",
            "variable_fee_inr": "0",
            "outage_compatible": "true",
            "rejection_reason": "",
        },
    ]
    alternates = [
        {
            "id": "INT-GOLD-B",
            "candidate_type": "ALTERNATE_SUPPLY",
            "supplier_id": "SUP-0208",
            "component_id": "CMP-MCU-42",
            "quantity": "400",
            "approval_status": "APPROVED",
            "effective_from": "2026-05-15T02:30:00Z",
            "effective_to": "2026-12-11T02:30:00Z",
            "lead_time_days": "5",
            "available_capacity": "400",
            "minimum_order_quantity": "100",
            "unit_price_inr": "1180",
            "baseline_unit_price_inr": "1000",
            "incremental_premium_inr": "72000",
            "currency": "INR",
            "component_compatible": "true",
            "feasibility_status": "FEASIBLE",
        }
    ]
    rescheduling = [
        {
            "id": f"INT-GOLD-RESCHEDULE-{index}",
            "candidate_type": "RESCHEDULE",
            "production_order_id": order_id,
            "order_status": "PLANNED",
            "lock_status": "UNLOCKED",
            "priority": "HIGH",
            "facility_capacity_available": "100",
            "reschedule_penalty_inr": "10000",
            "downstream_customer_impact": "PROTECTS_SLA",
            "feasibility_status": "FEASIBLE",
        }
        for index, order_id in enumerate(("MO-0876", "MO-0882", "MO-0889"), start=1)
    ]
    costs = [
        {
            "id": "COST-INT-GOLD-A",
            "candidate_id": "INT-GOLD-A",
            "fixed_cost_inr": "40000",
            "variable_cost_inr": "20000",
            "total_cost_inr": "60000",
            "currency": "INR",
        },
        {
            "id": "COST-INT-GOLD-B",
            "candidate_id": "INT-GOLD-B",
            "fixed_cost_inr": "0",
            "variable_cost_inr": "72000",
            "total_cost_inr": "72000",
            "currency": "INR",
        },
        {
            "id": "COST-INT-GOLD-C",
            "candidate_id": "INT-GOLD-C",
            "fixed_cost_inr": "40000",
            "variable_cost_inr": "92000",
            "total_cost_inr": "132000",
            "currency": "INR",
        },
        {
            "id": "COST-INT-GOLD-TRANSFER-500",
            "candidate_id": "INT-GOLD-TRANSFER-500",
            "fixed_cost_inr": "40000",
            "variable_cost_inr": "25000",
            "total_cost_inr": "65000",
            "currency": "INR",
        },
    ]
    output = release_root(profile) / "interventions"
    write_release_csv(output / "transfer_capabilities.csv", transfers)
    write_release_csv(output / "expedite_capabilities.csv", expedites)
    write_release_csv(output / "alternate_supply_capabilities.csv", alternates)
    write_release_csv(output / "rescheduling_constraints.csv", rescheduling)
    write_release_csv(output / "intervention_cost_parameters.csv", costs)
    return {
        "transfers": transfers,
        "expedites": expedites,
        "alternates": alternates,
        "rescheduling": rescheduling,
        "costs": costs,
    }
