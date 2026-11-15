"""Phase 7K: deterministic weight sensitivity analysis."""

from __future__ import annotations

from typing import Sequence

from .contracts import (
    CandidateMetrics,
    FeasibilityResult,
    FeasibilityStatus,
    NormalizedMetrics,
    OptimizationValidationError,
    ParetoResult,
    SensitivityResult,
    SensitivityVariation,
    UtilityScore,
    WeightVector,
)
from .utility import UtilityScoringEngine, utility_sort_key


class SensitivityAnalyzer:
    """Re-run selection under explicit weight variations."""

    def __init__(
        self,
        weights: WeightVector | None = None,
        factors: tuple[float, ...] = (1.2, 0.8),
    ) -> None:
        self.base_weights = weights or WeightVector(0.40, 0.30, 0.15, 0.10, 0.05)
        self.factors = factors

    def analyze(
        self,
        candidates: Sequence[CandidateMetrics],
        feasibility: Sequence[FeasibilityResult],
        normalized: Sequence[NormalizedMetrics],
        pareto: Sequence[ParetoResult],
        base_utilities: Sequence[UtilityScore],
        base_recommendation_id: str,
    ) -> SensitivityResult:
        del pareto, base_utilities
        normalized_map = {item.candidate_id: item for item in normalized}
        feasible_ids = {
            item.candidate_id
            for item in feasibility
            if item.status
            in (FeasibilityStatus.FEASIBLE, FeasibilityStatus.CONDITIONALLY_FEASIBLE)
        }
        eligible = [
            candidate for candidate in candidates if candidate.candidate_id in feasible_ids
        ]
        if not eligible:
            raise OptimizationValidationError("no feasible candidate for sensitivity")

        variations: list[SensitivityVariation] = []
        for weight_name in ("revenue", "sla", "cost", "delay"):
            for factor in self.factors:
                varied = self.base_weights.vary(weight_name, factor)
                engine = UtilityScoringEngine(varied)
                scores = engine.score_many(
                    eligible, (normalized_map[item.candidate_id] for item in eligible)
                )
                by_candidate = {item.candidate_id: item for item in scores}
                winner = min(
                    eligible,
                    key=lambda candidate: utility_sort_key(
                        by_candidate[candidate.candidate_id], candidate
                    ),
                )
                variations.append(
                    SensitivityVariation(
                        category=weight_name,
                        variation=f"{factor:.2f}x",
                        weights=varied.to_dict(),
                        recommended_candidate=winner.candidate_id,
                        score=by_candidate[winner.candidate_id].utility_score,
                        changed=winner.candidate_id != base_recommendation_id,
                    )
                )

        switched = sorted(
            {
                item.recommended_candidate
                for item in variations
                if item.recommended_candidate != base_recommendation_id
            }
        )
        return SensitivityResult(
            stable=not any(item.changed for item in variations),
            winner_changes=sum(1 for item in variations if item.changed),
            base_winner=base_recommendation_id,
            switches_to=tuple(switched),
            variations=tuple(variations),
        )
