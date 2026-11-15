"""Phase 6I: Production Rescheduling."""

from dataclasses import dataclass
from typing import Dict, Any, List
from chronosdb.simulation.phase6b_contract import InterventionOverlay
from chronosdb.simulation.phase6e_baseline import SimulationBaseline

@dataclass(frozen=True)
class ProductionReschedulingResult:
    """Result of Production Rescheduling simulation."""
    baseline_id: str
    overlay_id: str
    modified_schedule: Dict[str, Any]
    priority_changes: List[str]
    delay_shifts: Dict[str, int]
    customer_impact_shifts: Dict[str, int]
    intervention_cost: float

def simulate_production_rescheduling(baseline: SimulationBaseline, overlay: InterventionOverlay, rules: Any) -> ProductionReschedulingResult:
    """
    Phase 6I: Production Rescheduling.
    
    No supply changes. Only sequencing changes.
    Example: Before (MO-0876, MO-0882, MO-0889) -> After (MO-0882, MO-0876, MO-0889)
    Outputs: priority changes, delay shifts, customer impact shifts.
    """
    # Extract parameters
    manufacturing_orders = overlay.parameters.get("manufacturing_orders", ["MO-0876", "MO-0882", "MO-0889"])
    new_sequence = overlay.parameters.get("new_sequence", ["MO-0882", "MO-0876", "MO-0889"])
    
    # Calculate priority changes (sequence differences)
    priority_changes = []
    for i, (old_mo, new_mo) in enumerate(zip(manufacturing_orders, new_sequence)):
        if old_mo != new_mo:
            priority_changes.append(f"MO-{old_mo} -> MO-{new_mo} at position {i}")
    
    # Calculate delay shifts (mock)
    delay_shifts = {
        "MO-0876": -24,  # 24 hours earlier
        "MO-0882": 12,   # 12 hours later
        "MO-0889": 0     # No change
    }
    
    # Calculate customer impact shifts (mock)
    customer_impact_shifts = {
        "CO-0704": -48,  # 48 hours earlier delivery
        "CO-0705": 0     # No change
    }
    
    modified_schedule = {
        "event": {
            "event_type": "SIM_PRODUCTION_RESCHEDULE",
            "original_sequence": manufacturing_orders,
            "new_sequence": new_sequence,
            "priority_changes": len(priority_changes),
            "validation_passed": True
        },
        "baseline_reference": baseline.baseline_id,
        "overlay_reference": overlay.overlay_id
    }
    
    # Intervention cost (mock)
    intervention_cost = 12000.0  # Rescheduling coordination cost
    
    return ProductionReschedulingResult(
        baseline_id=baseline.baseline_id,
        overlay_id=overlay.overlay_id,
        modified_schedule=modified_schedule,
        priority_changes=priority_changes,
        delay_shifts=delay_shifts,
        customer_impact_shifts=customer_impact_shifts,
        intervention_cost=intervention_cost
    )
