"""Phase 7S: Observability.

Required Metrics:
- Candidates Evaluated
- Candidates Rejected
- Pareto Size
- Winning Score
- Constraint Violations
- Optimization Runtime
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import time

@dataclass(frozen=True)
class ObservabilityMetrics:
    """Observability metrics."""
    timestamp: str
    candidates_evaluated: int
    candidates_rejected: int
    pareto_size: int
    winning_score: float
    constraint_violations: int
    optimization_runtime_ms: float
    analysis_details: Dict[str, Any]

class ObservabilityEngine:
    """
    Phase 7S: Observability.
    
    Tracks and reports optimization metrics.
    """
    
    def __init__(self):
        self.metrics_history = []
    
    def track_optimization_run(
        self,
        candidates_evaluated: int,
        candidates_rejected: int,
        pareto_size: int,
        winning_score: float,
        constraint_violations: int,
        optimization_runtime_ms: float,
        analysis_details: Dict[str, Any]
    ) -> ObservabilityMetrics:
        """Track optimization run metrics."""
        from datetime import datetime
        
        metrics = ObservabilityMetrics(
            timestamp=datetime.now().isoformat(),
            candidates_evaluated=candidates_evaluated,
            candidates_rejected=candidates_rejected,
            pareto_size=pareto_size,
            winning_score=winning_score,
            constraint_violations=constraint_violations,
            optimization_runtime_ms=optimization_runtime_ms,
            analysis_details=analysis_details
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_history(self) -> List[ObservabilityMetrics]:
        """Get history of observability metrics."""
        return self.metrics_history
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate observability report."""
        if not self.metrics_history:
            return {"status": "no_data", "metrics_count": 0}
        
        latest = self.metrics_history[-1]
        
        return {
            "status": "success",
            "total_runs": len(self.metrics_history),
            "latest_run": {
                "timestamp": latest.timestamp,
                "candidates_evaluated": latest.candidates_evaluated,
                "candidates_rejected": latest.candidates_rejected,
                "pareto_size": latest.pareto_size,
                "winning_score": latest.winning_score,
                "constraint_violations": latest.constraint_violations,
                "optimization_runtime_ms": latest.optimization_runtime_ms,
                "passed_targets": {
                    "runtime_under_500ms": latest.optimization_runtime_ms <= 500,
                    "pareto_size_reasonable": latest.pareto_size > 0,
                    "candidates_evaluated_positive": latest.candidates_evaluated > 0
                }
            },
            "history_count": len(self.metrics_history)
        }

# Phase 7S Status: IMPLEMENTED
