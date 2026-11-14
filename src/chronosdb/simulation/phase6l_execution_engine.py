"""Phase 6L: Simulation Execution Engine."""

from dataclasses import dataclass
from typing import Dict, Any, List
from chronosdb.simulation.phase6b_contract import InterventionOverlay
from chronosdb.simulation.phase6e_baseline import SimulationBaseline
from chronosdb.simulation.phase6k_overlay_engine import OverlayApplicationEngine, SimulationState

@dataclass(frozen=True)
class ExecutionResult:
    """Final execution result."""
    simulation_run_id: str
    baseline_run_id: str
    overlay_hash: str
    result_hash: str
    runtime_ms: int
    simulation_state: SimulationState
    persisted_outcomes: Dict[str, Any]

class SimulationExecutionEngine:
    """
    Phase 6L: Simulation Execution Engine.
    
    Pipeline:
    1. Load Baseline
    2. Apply Overlay
    3. Execute Phase 5 Engine (reuse)
    4. Capture Results
    5. Persist Outcomes
    
    Critical Principle: Do not rewrite inventory/allocation/scheduling/financial logic.
    Reuse Phase 5. Phase 6 becomes: State Modifier + Impact Engine Runner.
    """
    
    def __init__(self, rules: Any = None):
        self.rules = rules or type('Rules', (), {'version': '1.0.0'})()
        self.overlay_engine = OverlayApplicationEngine(self.rules)
    
    def execute_simulation(self, baseline: SimulationBaseline, overlays: List[InterventionOverlay], simulation_run_id: str) -> ExecutionResult:
        """Execute full simulation pipeline."""
        
        # Step 1 & 2: Load Baseline & Apply Overlay (via Overlay Engine)
        simulation_state = self.overlay_engine.apply_overlays(baseline, overlays)
        
        # Step 3: Execute Phase 5 Engine (reuse - mock for Phase 6)
        # In real implementation, this would call Phase 5 engine with modified state
        phase5_execution_result = {
            "engine_version": "5.3.2",
            "execution_status": "success",
            "no_logic_rewritten": True  # Critical principle
        }
        
        # Step 4: Capture Results (already in simulation_state)
        
        # Step 5: Persist Outcomes (Phase 6O Persistence and Scenario Ledger)
        persisted_outcomes = self._persist_outcomes(
            simulation_run_id=simulation_run_id,
            baseline_run_id=baseline.impact_run_id,
            overlay_hash="-".join(simulation_state.overlay_hashes),
            result_hash=simulation_state.result_hash,
            runtime_ms=simulation_state.runtime_ms,
            simulation_state=simulation_state,
            phase5_result=phase5_execution_result
        )
        
        return ExecutionResult(
            simulation_run_id=simulation_run_id,
            baseline_run_id=baseline.impact_run_id,
            overlay_hash="-".join(simulation_state.overlay_hashes),
            result_hash=simulation_state.result_hash,
            runtime_ms=simulation_state.runtime_ms,
            simulation_state=simulation_state,
            persisted_outcomes=persisted_outcomes
        )
    
    def _persist_outcomes(self, simulation_run_id: str, baseline_run_id: str, overlay_hash: str, 
                         result_hash: str, runtime_ms: int, simulation_state: SimulationState, 
                         phase5_result: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6O: Persistence and Scenario Ledger."""
        # Required records: SIMULATION_RUN, SIMULATION_INPUT, SIMULATION_ACTION, 
        # SIMULATION_RESULT, SIMULATION_DELTA, SIMULATION_WARNING, SIMULATION_ERROR
        
        return {
            "simulation_run": {
                "simulation_run_id": simulation_run_id,
                "baseline_run_id": baseline_run_id,
                "overlay_hash": overlay_hash,
                "result_hash": result_hash,
                "runtime_ms": runtime_ms
            },
            "simulation_input": {
                "baseline_id": simulation_state.baseline_id,
                "overlay_count": len(simulation_state.overlay_hashes),
                "phase5_engine_version": phase5_result["engine_version"]
            },
            "simulation_action": {
                "events_generated": len(simulation_state.generated_events),
                "causal_evidence_count": len(simulation_state.causal_evidence)
            },
            "simulation_result": {
                "revenue_protected": simulation_state.derived_state["revenue_protected"],
                "breaches_avoided": simulation_state.derived_state["breaches_avoided"],
                "delay_reduction_hours": simulation_state.derived_state["delay_reduction_hours"],
                "net_benefit": simulation_state.derived_state["net_benefit"]
            },
            "simulation_delta": simulation_state.derived_state,
            "simulation_warning": [],  # No warnings in mock
            "simulation_error": []     # No errors in mock
        }
