"""Phase 6K: Overlay Application Engine."""

from dataclasses import dataclass
from typing import Dict, Any, List
from chronosdb.simulation.phase6b_contract import InterventionOverlay
from chronosdb.simulation.phase6e_baseline import SimulationBaseline
from chronosdb.simulation.phase6f_transfer import simulate_inventory_transfer
from chronosdb.simulation.phase6g_expedition import simulate_expedition
from chronosdb.simulation.phase6h_alternate_supplier import simulate_alternate_supplier
from chronosdb.simulation.phase6i_production_rescheduling import simulate_production_rescheduling
from chronosdb.simulation.phase6j_hybrid_intervention import simulate_hybrid_intervention

@dataclass(frozen=True)
class SimulationState:
    """Final simulation state after overlay application."""
    baseline_id: str
    overlay_hashes: List[str]
    generated_events: List[Dict[str, Any]]
    derived_state: Dict[str, Any]
    causal_evidence: List[str]
    runtime_ms: int
    result_hash: str

class OverlayApplicationEngine:
    """
    Phase 6K: Overlay Application Engine.
    
    Architecture:
    1. Load Baseline
    2. Apply Virtual Changes
    3. Generate Overlay Events
    4. Recompute Derived State
    
    Critical: No operational records modified. Ever.
    """
    
    def __init__(self, rules: Any = None):
        self.rules = rules or type('Rules', (), {'version': '1.0.0'})()
    
    def apply_overlays(self, baseline: SimulationBaseline, overlays: List[InterventionOverlay]) -> SimulationState:
        """Apply overlays to baseline and generate simulation state."""
        import time
        start_time = time.time()
        
        # Step 1: Load Baseline (already loaded in parameter)
        
        # Step 2: Apply Virtual Changes & Step 3: Generate Overlay Events
        if len(overlays) == 1:
            # Single overlay - route to specific simulator
            overlay = overlays[0]
            if overlay.action == "TRANSFER_INVENTORY":
                from chronosdb.simulation.phase6f_transfer import simulate_inventory_transfer
                result = simulate_inventory_transfer(baseline, overlay, self.rules)
                events = [result.modified_supply["event"]]
                causal_edges = ["TRANSFER_COMPLETED", "INVENTORY_AVAILABLE"]
                cost = 0.0  # Mock
            elif overlay.action == "ALTERNATE_SUPPLIER":
                result = simulate_alternate_supplier(baseline, overlay, self.rules)
                events = [result.modified_supply["event"]]
                causal_edges = result.causal_edges
                cost = result.intervention_cost
            elif overlay.action == "EXPEDITE_PO":
                from chronosdb.simulation.phase6g_expedition import simulate_expedition
                result = simulate_expedition(baseline, overlay, self.rules)
                events = [result.modified_supply]
                causal_edges = ["ACCELERATES_DELIVERY", "PROTECTS_REVENUE"]
                cost = result.intervention_cost
            elif overlay.action == "RESCHEDULE_PRODUCTION":
                result = simulate_production_rescheduling(baseline, overlay, self.rules)
                events = [result.modified_schedule["event"]]
                causal_edges = ["PRIORITY_CHANGED", "DELAYS_SHIFTED"]
                cost = result.intervention_cost
            else:
                raise ValueError(f"Unknown action: {overlay.action}")
            
            execution_order = [overlay.action]
            total_cost = cost
            all_causal_edges = causal_edges
            
        else:
            # Multiple overlays - use hybrid simulator
            result = simulate_hybrid_intervention(baseline, overlays, self.rules)
            events = result.modified_state["events"]
            total_cost = result.total_intervention_cost
            all_causal_edges = result.causal_edges
            execution_order = result.execution_order
        
        # Step 4: Recompute Derived State (Phase 6M Delta Computation)
        derived_state = self._compute_derived_state(baseline, events, total_cost)
        
        runtime_ms = int((time.time() - start_time) * 1000)
        
        # Generate result hash (mock)
        import hashlib
        state_str = f"{baseline.baseline_id}-{'-'.join([o.overlay_id for o in overlays])}-{runtime_ms}"
        result_hash = hashlib.sha256(state_str.encode()).hexdigest()[:16]
        
        return SimulationState(
            baseline_id=baseline.baseline_id,
            overlay_hashes=[o.overlay_id for o in overlays],
            generated_events=events,
            derived_state=derived_state,
            causal_evidence=all_causal_edges,
            runtime_ms=runtime_ms,
            result_hash=result_hash
        )
    
    def _compute_derived_state(self, baseline: SimulationBaseline, events: List[Dict[str, Any]], total_cost: float) -> Dict[str, Any]:
        """Phase 6M: Delta Computation Engine."""
        # Mock delta computation
        revenue_protected = 800000.0  # ₹800k
        breaches_avoided = 1
        delay_reduction_hours = 168
        
        return {
            "revenue_protected": revenue_protected,
            "breaches_avoided": breaches_avoided,
            "delay_reduction_hours": delay_reduction_hours,
            "intervention_cost": total_cost,
            "net_benefit": revenue_protected - total_cost,
            "event_count": len(events)
        }
