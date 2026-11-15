"""Phase 7/11G: Optimization service backed by the real Phase 7 engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from src.backend.chronosdb.optimization.engine import OptimizationEngine


class OptimizationService:
    """
    Phase 11G: Expose Phase 7 engine
    
    Endpoints:
    - POST /api/v1/scenarios/{id}/optimize (Optimize)
    - GET /api/v1/optimization/{id}/candidates (Candidate Rankings)
    """
    
    def __init__(self):
        self.optimizations = {}
        
    def optimize(self, scenario_id: str) -> Dict[str, Any]:
        """
        POST /api/v1/scenarios/{id}/optimize
        Response: {recommended_candidate, utility_score}
        """
        optimization_id = f"OPT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Phase 7 Optimization Engine (deterministic)
        recommended_candidate = "HYBRID"
        utility_score = 0.91
        
        optimization = {
            "optimization_id": optimization_id,
            "scenario_id": scenario_id,
            "recommended_candidate": recommended_candidate,
            "utility_score": utility_score,
            "status": "COMPLETED",
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.optimizations[optimization_id] = optimization
        return {
            "optimization_id": optimization_id,
            "recommended_candidate": recommended_candidate,
            "utility_score": utility_score,
        }
        
    def get_candidates(self, optimization_id: str) -> Optional[Dict[str, Any]]:
        """
        GET /api/v1/optimization/{id}/candidates
        """
        optimization = self.optimizations.get(optimization_id)
        if optimization:
            return {
                "optimization_id": optimization_id,
                "candidates": ["HYBRID", "TRANSFER", "EXPEDITE"],
                "scores": [0.91, 0.85, 0.78]
            }
        return None

    def optimize(self, scenario_id: str) -> Dict[str, Any]:
        result = self.engine.run()
        optimization_id = result.optimization_run_id
        self.optimizations[optimization_id] = result
        return {
            "optimization_id": optimization_id,
            "scenario_id": result.scenario_id,
            "recommended_candidate": result.recommendation.candidate_id,
            "utility_score": result.recommendation.score,
            "result_hash": result.result_hash,
            "status": "COMPLETED",
        }

    def get_candidates(self, optimization_id: str) -> Optional[Dict[str, Any]]:
        result = self.optimizations.get(optimization_id)
        if result is None:
            return None
        return {
            "optimization_id": optimization_id,
            "ranking": list(result.recommendation.ranking),
            "candidates": [
                item.candidate_id for item in result.candidates
            ],
            "utility_scores": {
                item.candidate_id: item.utility_score for item in result.utilities
            },
            "result_hash": result.result_hash,
        }
