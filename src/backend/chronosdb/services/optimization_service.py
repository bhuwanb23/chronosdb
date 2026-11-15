"""Phase 7/11G: Optimization service backed by the real Phase 7 engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from src.backend.chronosdb.optimization.engine import OptimizationEngine


class OptimizationService:
    def __init__(self, root: Optional[Path] = None) -> None:
        self.root = Path(root) if root is not None else Path(__file__).resolve().parents[4]
        self.engine = OptimizationEngine(root=self.root)
        self.engine.warm()
        self.optimizations: Dict[str, Any] = {}

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
