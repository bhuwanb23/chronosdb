"""Phase 6G: Expedition Simulator."""

from typing import Dict, Any
from chronosdb.simulation.phase6b_contract import SimulationResult, OperationalState, Disruption, InterventionOverlay, RuleSet, Horizon
from chronosdb.simulation.phase6e_baseline import ScenarioBaseline

def simulate_expedition(
    baseline: ScenarioBaseline,
    overlay: InterventionOverlay,
    rules: RuleSet
) -> SimulationResult:
    """
    Goal: Bring supply earlier.
    Example: PO-2208 (Phase 5: 27 Nov -> Expedite: 22 Nov)
    
    Constraints:
    - cannot precede shipment release
    - cannot exceed supplier capability
    - must incur expedition cost
    
    Cost Model:
    Expedition Cost = base freight + premium freight + supplier surcharge
    """
    if overlay.action != "EXPEDITE_PO":
        raise ValueError("Invalid overlay action for Expedition Simulator")
    
    params = overlay.parameters
    po_id = params.get("purchase_order_id")
    reduction_days = int(params.get("lead_time_reduction_days", 0))
    
    # Validation logic (simplified)
    if reduction_days <= 0:
        raise ValueError("Reduction days must be positive")
    
    # Mock cost calculation
    base_freight = 1000.0
    premium_freight = 500.0 * reduction_days
    supplier_surcharge = 200.0
    total_cost = base_freight + premium_freight + supplier_surcharge
    
    # Mock simulation result
    result = SimulationResult(
        baseline_id=baseline.baseline_id,
        overlay_id=overlay.overlay_id,
        modified_supply={"po_id": po_id, "new_arrival": "2026-11-22T00:00:00Z"},
        modified_inventory={},
        modified_production={},
        modified_customer_impact={"supply_earlier": True},
        modified_sla_impact={"breaches_reduced": 1},
        modified_revenue_risk=baseline.revenue_at_risk - 50000.0,
        intervention_cost=total_cost,
        operational_side_effects=["premium_freight_applied"],
        comparison_against_baseline={"delta_revenue": 50000.0, "delta_cost": total_cost},
        auditable_trace=f"TRACE-EXPEDITE-{overlay.overlay_id}"
    )
    
    return result
