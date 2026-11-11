"""Phase 3O invalid, boundary, contradiction, and retrieval fixtures."""

from __future__ import annotations


def build_fixtures() -> list[dict[str, str]]:
    """Return a compact, named fixture suite with expected failure labels."""
    cases = [
        ("unknown_supplier", "UNKNOWN_ENTITY"),
        ("unknown_component", "UNKNOWN_ENTITY"),
        ("unknown_warehouse", "UNKNOWN_ENTITY"),
        ("unknown_production_order", "UNKNOWN_ENTITY"),
        ("unknown_scenario", "UNKNOWN_ENTITY"),
        ("negative_inventory", "INVALID_QUANTITY"),
        ("zero_ordered_quantity", "INVALID_QUANTITY"),
        ("negative_disruption_duration", "INVALID_INTERVAL"),
        ("transfer_exceeds_source_stock", "INFEASIBLE_INTERVENTION"),
        ("completed_exceeds_planned", "INVALID_QUANTITY"),
        ("arrival_before_order", "INVALID_INTERVAL"),
        ("scenario_before_activation", "INVALID_INTERVAL"),
        ("promised_before_order", "INVALID_INTERVAL"),
        ("outage_end_before_start", "INVALID_INTERVAL"),
        ("overlapping_bom_versions", "INVALID_INTERVAL"),
        ("missing_critical_inventory", "MISSING_CRITICAL_DATA"),
        ("no_active_bom", "MISSING_CRITICAL_DATA"),
        ("missing_promised_date", "MISSING_CRITICAL_DATA"),
        ("missing_supplier_approval", "INFEASIBLE_INTERVENTION"),
        ("missing_intervention_cost", "MISSING_CRITICAL_DATA"),
        ("inactive_supplier_active_agreement", "CONTRADICTORY_STATE"),
        ("received_with_outstanding_quantity", "CONTRADICTORY_STATE"),
        ("inventory_snapshot_disagrees", "CONTRADICTORY_STATE"),
        ("production_without_materials", "CONTRADICTORY_STATE"),
        ("receipt_without_dispatch", "CONTRADICTORY_STATE"),
        ("cheapest_violates_sla", "INFEASIBLE_INTERVENTION"),
        ("best_sla_exceeds_budget", "INFEASIBLE_INTERVENTION"),
        ("tied_candidates", "INFEASIBLE_INTERVENTION"),
        ("no_feasible_candidate", "NO_FEASIBLE_INTERVENTION"),
        ("unauthorized_or_expired_evidence", "UNAUTHORIZED_EVIDENCE"),
    ]
    fixtures: list[dict[str, str]] = []
    for index, (name, error) in enumerate(cases, start=1):
        family = "invalid" if index <= 10 else "boundary" if index <= 20 else "adversarial"
        fixtures.append(
            {
                "fixture_id": f"FIX-{index:04d}",
                "family": family,
                "case": name,
                "expected_error": error,
            }
        )
    return fixtures
