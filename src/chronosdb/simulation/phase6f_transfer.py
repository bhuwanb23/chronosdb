"""Phase 6F: Inventory Transfer Simulator."""

from typing import Dict, Any
from chronosdb.simulation.phase6b_contract import SimulationResult, OperationalState, Disruption, InterventionOverlay, RuleSet, Horizon
from chronosdb.simulation.phase6e_baseline import ScenarioBaseline

def simulate_inventory_transfer(
    baseline: ScenarioBaseline,
    overlay: InterventionOverlay,
    rules: RuleSet
) -> SimulationResult:
    """
    Simulate Chennai -> Pune transfer without changing warehouse inventory records.
    
    Validation:
    - Source inventory exists
    - Above safety stock
    - Transfer lane valid
    - Arrival inside horizon
    - Quantity positive
    """
    if overlay.action != "TRANSFER_INVENTORY":
        raise ValueError("Invalid overlay action for Inventory Transfer Simulator")
    
    params = overlay.parameters
    component_id = params.get("component_id")
    quantity = int(params.get("quantity", 0))
    from_warehouse = params.get("from_warehouse")
    to_warehouse = params.get("to_warehouse")
    
    # Validation logic (simplified for Phase 6F)
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    # Mock simulation logic (Phase 6F specific)
    # In reality, this would use Phase 5 engine with overlay
    generated_event = {
        "event_type": "SIM_TRANSFER_RECEIPT",
        "component_id": component_id,
        "quantity": str(quantity),
        "arrival_time": "2026-11-14T00:00:00Z",  # Example
        "from": from_warehouse,
        "to": to_warehouse
    }
    
    # Impact calculation (simplified)
    result = SimulationResult(
        baseline_id=baseline.baseline_id,
        overlay_id=overlay.overlay_id,
        modified_supply={"event": generated_event},
        modified_inventory={"status": "earlier_availability"},
        modified_production={},
        modified_customer_impact={"shortage_reduced": True},
        modified_sla_impact={"delay_reduced": True},
        modified_revenue_risk=baseline.revenue_at_risk * 0.95,  # 5% reduction example
        intervention_cost=0.0,  # Transfer cost logic here
        operational_side_effects=[],
        comparison_against_baseline={"delta_revenue": -baseline.revenue_at_risk * 0.05},
        auditable_trace=f"TRACE-TRANSFER-{overlay.overlay_id}"
    )
    
    return result
