"""Phase 6J: Hybrid Intervention Simulator."""

from dataclasses import dataclass
from typing import Dict, Any, List
from chronosdb.simulation.phase6b_contract import InterventionOverlay
from chronosdb.simulation.phase6e_baseline import SimulationBaseline
from chronosdb.simulation.phase6f_transfer import simulate_inventory_transfer
from chronosdb.simulation.phase6g_expedition import simulate_expedition
from chronosdb.simulation.phase6h_alternate_supplier import simulate_alternate_supplier
from chronosdb.simulation.phase6i_production_rescheduling import simulate_production_rescheduling

@dataclass(frozen=True)
class HybridInterventionResult:
    """Result of Hybrid Intervention simulation."""
    baseline_id: str
    overlay_ids: List[str]
    modified_state: Dict[str, Any]
    total_intervention_cost: float
    causal_edges: List[str]
    execution_order: List[str]

def simulate_hybrid_intervention(baseline: SimulationBaseline, overlays: List[InterventionOverlay], rules: Any) -> HybridInterventionResult:
    """
    Phase 6J: Hybrid Intervention Simulator.
    
    Multiple overlays.
    Deterministic order: Transfer -> Supplier -> Expedition -> Reschedule
    """
    # Apply overlays in deterministic order
    execution_order = []
    modified_state = {
        "baseline_reference": baseline.baseline_id,
        "overlays_applied": len(overlays),
        "events": []
    }
    
    total_cost = 0.0
    all_causal_edges = []
    
    # Group overlays by action type
    transfer_overlays = [o for o in overlays if o.action == "TRANSFER_INVENTORY"]
    supplier_overlays = [o for o in overlays if o.action == "ALTERNATE_SUPPLIER"]
    expedition_overlays = [o for o in overlays if o.action == "EXPEDITE_PO"]
    reschedule_overlays = [o for o in overlays if o.action == "RESCHEDULE_PRODUCTION"]
    
    # 1. Transfer Inventory
    for overlay in transfer_overlays:
        execution_order.append(f"TRANSFER:{overlay.overlay_id}")
        # Mock rules
        rules_obj = type('Rules', (), {'version': '1.0.0'})()
        result = simulate_inventory_transfer(baseline, overlay, rules_obj)
        modified_state["events"].append(result.modified_supply["event"])
        total_cost += result.intervention_cost  # Note: transfer result doesn't have cost in current implementation, mock
        all_causal_edges.extend(["TRANSFER_COMPLETED", "INVENTORY_AVAILABLE"])
    
    # 2. Alternate Supplier
    for overlay in supplier_overlays:
        execution_order.append(f"SUPPLIER:{overlay.overlay_id}")
        result = simulate_alternate_supplier(baseline, overlay, rules)
        modified_state["events"].append(result.modified_supply["event"])
        total_cost += result.intervention_cost
        all_causal_edges.extend(result.causal_edges)
    
    # 3. Expedition
    for overlay in expedition_overlays:
        execution_order.append(f"EXPEDITION:{overlay.overlay_id}")
        # Mock rules
        rules_obj = type('Rules', (), {'version': '1.0.0'})()
        result = simulate_expedition(baseline, overlay, rules_obj)
        modified_state["events"].append(result.modified_supply)
        total_cost += result.intervention_cost
        all_causal_edges.extend(["ACCELERATES_DELIVERY", "PROTECTS_REVENUE"])
    
    # 4. Reschedule Production
    for overlay in reschedule_overlays:
        execution_order.append(f"RESCHEDULE:{overlay.overlay_id}")
        result = simulate_production_rescheduling(baseline, overlay, rules)
        modified_state["events"].append(result.modified_schedule["event"])
        total_cost += result.intervention_cost
        all_causal_edges.extend(["PRIORITY_CHANGED", "DELAYS_SHIFTED"])
    
    return HybridInterventionResult(
        baseline_id=baseline.baseline_id,
        overlay_ids=[o.overlay_id for o in overlays],
        modified_state=modified_state,
        total_intervention_cost=total_cost,
        causal_edges=list(set(all_causal_edges)),  # Unique edges
        execution_order=execution_order
    )
