"""Phase 6O: Persistence and Scenario Ledger (Data Model)."""

from dataclasses import dataclass
from typing import Dict, Any, List
import json
import hashlib

@dataclass
class SimulationRun:
    """SIMULATION_RUN record."""
    simulation_run_id: str
    baseline_run_id: str
    overlay_hash: str
    result_hash: str
    runtime_ms: int

@dataclass
class SimulationInput:
    """SIMULATION_INPUT record."""
    baseline_id: str
    overlay_count: int
    phase5_engine_version: str

@dataclass
class SimulationAction:
    """SIMULATION_ACTION record."""
    events_generated: int
    causal_evidence_count: int

@dataclass
class SimulationResult:
    """SIMULATION_RESULT record."""
    revenue_protected: float
    breaches_avoided: int
    delay_reduction_hours: int
    net_benefit: float

@dataclass
class SimulationDelta:
    """SIMULATION_DELTA record."""
    revenue_protected: float
    breaches_avoided: int
    delay_reduction_hours: int
    baseline_revenue_risk: float
    scenario_revenue_risk: float
    baseline_breaches: int
    scenario_breaches: int
    baseline_delay_hours: int
    scenario_delay_hours: int
    intervention_cost: float

@dataclass
class SimulationWarning:
    """SIMULATION_WARNING record."""
    warning_type: str
    message: str

@dataclass
class SimulationError:
    """SIMULATION_ERROR record."""
    error_type: str
    message: str

class ScenarioLedger:
    """
    Phase 6O: Persistence and Scenario Ledger.
    
    Manages required records for auditability and provenance.
    """
    
    def __init__(self):
        self.ledger = {
            "simulation_runs": [],
            "simulation_inputs": [],
            "simulation_actions": [],
            "simulation_results": [],
            "simulation_deltas": [],
            "simulation_warnings": [],
            "simulation_errors": []
        }
    
    def record_simulation(self, run: SimulationRun, input_rec: SimulationInput, 
                         action: SimulationAction, result: SimulationResult, 
                         delta: SimulationDelta, warnings: List[SimulationWarning] = None, 
                         errors: List[SimulationError] = None) -> str:
        """Record a complete simulation run."""
        
        self.ledger["simulation_runs"].append(run.__dict__)
        self.ledger["simulation_inputs"].append(input_rec.__dict__)
        self.ledger["simulation_actions"].append(action.__dict__)
        self.ledger["simulation_results"].append(result.__dict__)
        self.ledger["simulation_deltas"].append(delta.__dict__)
        
        if warnings:
            self.ledger["simulation_warnings"].extend([w.__dict__ for w in warnings])
        if errors:
            self.ledger["simulation_errors"].extend([e.__dict__ for e in errors])
        
        # Generate ledger entry hash for auditability
        ledger_str = json.dumps({
            "run_id": run.simulation_run_id,
            "baseline_id": input_rec.baseline_id,
            "result_hash": run.result_hash,
            "timestamp": "2026-11-14T00:00:00Z"  # Current date
        }, sort_keys=True)
        
        entry_hash = hashlib.sha256(ledger_str.encode()).hexdigest()[:16]
        
        return entry_hash
    
    def get_ledger_summary(self) -> Dict[str, Any]:
        """Get summary of all ledger entries."""
        return {
            "total_runs": len(self.ledger["simulation_runs"]),
            "total_inputs": len(self.ledger["simulation_inputs"]),
            "total_actions": len(self.ledger["simulation_actions"]),
            "total_results": len(self.ledger["simulation_results"]),
            "total_deltas": len(self.ledger["simulation_deltas"]),
            "total_warnings": len(self.ledger["simulation_warnings"]),
            "total_errors": len(self.ledger["simulation_errors"])
        }
