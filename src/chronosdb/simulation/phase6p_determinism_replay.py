"""Phase 6P: Determinism and Replay."""

import hashlib
import time
from typing import List, Dict, Any
from chronosdb.simulation.phase6b_contract import InterventionOverlay
from chronosdb.simulation.phase6e_baseline import SimulationBaseline
from chronosdb.simulation.phase6l_execution_engine import SimulationExecutionEngine

class DeterminismAndReplayEngine:
    """
    Phase 6P: Determinism and Replay.
    
    Target: Unique business outputs = 1 (for 100 runs of Golden Transfer Scenario)
    Benchmark: 20 scenarios, 10 reruns each = 200 stable outputs
    Replay: Restart, Re-run, Cross-process, Cross-host -> Same result
    """
    
    def __init__(self, execution_engine: SimulationExecutionEngine = None):
        self.execution_engine = execution_engine or SimulationExecutionEngine()
    
    def run_determinism_test(self, baseline: SimulationBaseline, overlays: List[InterventionOverlay], 
                            runs: int = 100) -> Dict[str, Any]:
        """
        Run determinism test: execute same scenario multiple times.
        Target: Unique business outputs = 1
        """
        results = []
        unique_outputs = set()
        
        for i in range(runs):
            simulation_run_id = f"SIM-DET-{i:03d}"
            result = self.execution_engine.execute_simulation(baseline, overlays, simulation_run_id)
            results.append(result)
            
            # Create output signature (revenue, breaches, delay, cost)
            output_signature = f"{result.simulation_state.derived_state['revenue_protected']}-" \
                               f"{result.simulation_state.derived_state['breaches_avoided']}-" \
                               f"{result.simulation_state.derived_state['delay_reduction_hours']}-" \
                               f"{result.simulation_state.derived_state['intervention_cost']}"
            unique_outputs.add(output_signature)
        
        is_deterministic = len(unique_outputs) == 1
        
        return {
            "total_runs": runs,
            "unique_outputs": len(unique_outputs),
            "is_deterministic": is_deterministic,
            "first_result_hash": results[0].result_hash,
            "last_result_hash": results[-1].result_hash,
            "unique_signatures": list(unique_outputs)
        }
    
    def run_replay_test(self, baseline: SimulationBaseline, overlays: List[InterventionOverlay], 
                       simulation_run_id: str) -> Dict[str, Any]:
        """
        Run replay test: restart and re-run same simulation.
        Target: Same result (cross-process, cross-host compatible)
        """
        # First run
        result1 = self.execution_engine.execute_simulation(baseline, overlays, simulation_run_id)
        
        # Replay (restart and re-run)
        result2 = self.execution_engine.execute_simulation(baseline, overlays, f"{simulation_run_id}-REPLAY")
        
        # Compare results
        hashes_match = result1.result_hash == result2.result_hash
        derived_states_match = (
            result1.simulation_state.derived_state == result2.simulation_state.derived_state
        )
        
        return {
            "original_run_id": simulation_run_id,
            "replay_run_id": f"{simulation_run_id}-REPLAY",
            "original_result_hash": result1.result_hash,
            "replay_result_hash": result2.result_hash,
            "hashes_match": hashes_match,
            "derived_states_match": derived_states_match,
            "runtime_original_ms": result1.runtime_ms,
            "runtime_replay_ms": result2.runtime_ms
        }
