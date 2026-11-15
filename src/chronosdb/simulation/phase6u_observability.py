"""Phase 6U: Observability.

Tracks simulation runs, metrics, and provides diagnostics/reporting.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import time
from datetime import datetime


@dataclass(frozen=True)
class SimulationObservabilityMetrics:
    """Observability metrics for a simulation run."""
    timestamp: str
    simulation_run_id: str
    baseline_id: str
    overlays_applied: int
    runtime_ms: float
    revenue_protected: float
    breaches_avoided: int
    delay_reduction_hours: float
    intervention_cost: float
    warnings: int
    errors: int
    status: str


class ObservabilityEngine:
    """Phase 6U: Observability Engine.

    Tracks and reports simulation metrics.
    """

    def __init__(self):
        self.metrics_history: List[SimulationObservabilityMetrics] = []

    def track_simulation_run(
        self,
        simulation_run_id: str,
        baseline_id: str,
        overlays_applied: int,
        runtime_ms: float,
        revenue_protected: float = 0.0,
        breaches_avoided: int = 0,
        delay_reduction_hours: float = 0.0,
        intervention_cost: float = 0.0,
        warnings: int = 0,
        errors: int = 0,
        status: str = "SUCCESS",
    ) -> SimulationObservabilityMetrics:
        metrics = SimulationObservabilityMetrics(
            timestamp=datetime.now().isoformat(),
            simulation_run_id=simulation_run_id,
            baseline_id=baseline_id,
            overlays_applied=overlays_applied,
            runtime_ms=runtime_ms,
            revenue_protected=revenue_protected,
            breaches_avoided=breaches_avoided,
            delay_reduction_hours=delay_reduction_hours,
            intervention_cost=intervention_cost,
            warnings=warnings,
            errors=errors,
            status=status,
        )
        self.metrics_history.append(metrics)
        return metrics

    def get_history(self) -> List[SimulationObservabilityMetrics]:
        return self.metrics_history

    def generate_report(self) -> Dict[str, Any]:
        if not self.metrics_history:
            return {"status": "no_data", "metrics_count": 0}
        latest = self.metrics_history[-1]
        return {
            "status": "success",
            "total_runs": len(self.metrics_history),
            "latest_run": {
                "timestamp": latest.timestamp,
                "simulation_run_id": latest.simulation_run_id,
                "baseline_id": latest.baseline_id,
                "overlays_applied": latest.overlays_applied,
                "runtime_ms": latest.runtime_ms,
                "revenue_protected": latest.revenue_protected,
                "breaches_avoided": latest.breaches_avoided,
                "delay_reduction_hours": latest.delay_reduction_hours,
                "intervention_cost": latest.intervention_cost,
                "warnings": latest.warnings,
                "errors": latest.errors,
                "status": latest.status,
            },
            "history_count": len(self.metrics_history),
        }


# Alias for naming compatibility
SimulationObservabilityEngine = ObservabilityEngine
SimulationObservability = ObservabilityEngine

# Phase 6U Status: IMPLEMENTED