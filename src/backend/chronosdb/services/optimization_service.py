"""Phase 7/11G: Optimization service backed by the real Phase 7 engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.backend.chronosdb.optimization.contracts import canonical_hash
from src.backend.chronosdb.optimization.engine import OptimizationEngine


class OptimizationService:
    """Expose the deterministic Phase 7 optimization engine."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root is not None else Path(__file__).resolve().parents[4]
        self.engine = OptimizationEngine(root=self.root)
        self.engine.warm()
        self.optimizations: dict[str, Any] = {}

    def optimize(self, scenario_id: str) -> dict[str, Any]:
        attempt = 1
        run_id = f"opt-{canonical_hash({'scenario_id': scenario_id, 'attempt': attempt})[:16]}"
        while run_id in self.optimizations:
            attempt += 1
            run_id = (
                f"opt-{canonical_hash({'scenario_id': scenario_id, 'attempt': attempt})[:16]}"
            )
        result = self.engine.run(run_id=run_id, scenario_id=scenario_id)
        optimization_id = result.optimization_run_id
        self.optimizations[optimization_id] = result
        return {
            "optimization_id": optimization_id,
            "scenario_id": scenario_id,
            "recommended_candidate": result.recommendation.candidate_id,
            "utility_score": result.recommendation.score,
            "result_hash": result.result_hash,
            "status": "COMPLETED",
        }

    def get_candidates(self, optimization_id: str) -> dict[str, Any] | None:
        result = self.optimizations.get(optimization_id)
        if result is None:
            return None
        return {
            "optimization_id": optimization_id,
            "scenario_id": result.scenario_id,
            "ranking": list(result.recommendation.provenance.get("ranking", ())),
            "candidates": [item.candidate_id for item in result.candidates],
            "utility_scores": {
                item.candidate_id: item.utility_score for item in result.utilities
            },
            "result_hash": result.result_hash,
        }
