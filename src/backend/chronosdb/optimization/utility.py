"""Phase 7H: transparent, normalized utility scoring."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .contracts import (
    CandidateMetrics,
    NormalizedMetrics,
    OptimizationValidationError,
    WeightVector,
    UtilityScore,
)


def utility_sort_key(
    score: UtilityScore, candidate: CandidateMetrics
) -> tuple[float, float, int, float, float, float, str]:
    """Deterministic ordering, including ties described by the contract."""

    return (
        -round(score.utility_score, 12),
        -candidate.revenue_protected,
        -candidate.breaches_avoided,
        -candidate.delay_reduction_hours,
        candidate.recovery_cost,
        candidate.supplier_risk,
        candidate.candidate_id,
    )


class UtilityScoringEngine:
    """U = weighted sum of oriented benefits.

    ``NormalizationEngine`` already reverses cost metrics, so the five terms are
    all positive: revenue protected, SLA breaches avoided, cost efficiency,
    delay reduction, and supplier-risk avoidance. This is algebraically the
    Phase 7 formula with the signs moved into the normalization step.
    """

    def __init__(self, weights: WeightVector | Mapping[str, Any] | None = None) -> None:
        self.weights = (
            weights
            if isinstance(weights, WeightVector)
            else WeightVector.from_mapping(weights)
            if weights is not None
            else WeightVector(0.40, 0.30, 0.15, 0.10, 0.05)
        )

    def score(
        self,
        candidate: CandidateMetrics,
        normalized: NormalizedMetrics,
        weights: WeightVector | None = None,
    ) -> UtilityScore:
        vector = weights or self.weights
        components = {
            "revenue_protected": round(
                vector.revenue * normalized.revenue_protected, 12
            ),
            "sla_saved": round(vector.sla * normalized.breaches_avoided, 12),
            "cost_efficiency": round(vector.cost * normalized.recovery_cost, 12),
            "delay_reduction": round(vector.delay * normalized.delay_reduction, 12),
            "risk_avoidance": round(vector.risk * normalized.supplier_risk, 12),
        }
        total = round(sum(components.values()), 12)
        return UtilityScore(
            candidate_id=candidate.candidate_id,
            utility_score=total,
            weighted_components=components,
        )

    def score_many(
        self,
        candidates: Iterable[CandidateMetrics],
        normalized: Iterable[NormalizedMetrics],
        weights: WeightVector | None = None,
    ) -> tuple[UtilityScore, ...]:
        candidate_map = {item.candidate_id: item for item in candidates}
        normalized_list = tuple(normalized)
        if not normalized_list:
            raise OptimizationValidationError("utility scoring requires candidates")
        if set(candidate_map) != {item.candidate_id for item in normalized_list}:
            raise OptimizationValidationError(
                "candidate and normalized metric sets must match"
            )
        scores = [
            self.score(candidate_map[item.candidate_id], item, weights)
            for item in normalized_list
        ]
        ordered = sorted(
            scores,
            key=lambda item: utility_sort_key(item, candidate_map[item.candidate_id]),
        )
        ranked = [
            UtilityScore(
                candidate_id=item.candidate_id,
                utility_score=item.utility_score,
                weighted_components=item.weighted_components,
                rank=index,
            )
            for index, item in enumerate(ordered, start=1)
        ]
        by_id = {item.candidate_id: item for item in ranked}
        return tuple(by_id[item.candidate_id] for item in scores)

    # Compatibility interface used by the pre-existing scaffold.
    def calculate_utility(self, normalized_metrics: dict[str, Any]) -> UtilityScore:
        candidate_id = str(
            normalized_metrics.get(
                "candidate_id", normalized_metrics.get("candidate", "UNKNOWN")
            )
        )
        normalized = NormalizedMetrics(
            candidate_id=candidate_id,
            revenue_protected=float(
                normalized_metrics.get("revenue_protected_norm", 0.0)
            ),
            breaches_avoided=float(
                normalized_metrics.get("breaches_avoided_norm", 0.0)
            ),
            delay_reduction=float(
                normalized_metrics.get("delay_reduction_norm", 0.0)
            ),
            recovery_cost=float(normalized_metrics.get("recovery_cost_norm", 0.0)),
            supplier_risk=float(normalized_metrics.get("supplier_risk_norm", 0.0)),
        )
        components = {
            "revenue_protected": round(
                self.weights.revenue * normalized.revenue_protected, 12
            ),
            "sla_saved": round(
                self.weights.sla * normalized.breaches_avoided, 12
            ),
            "cost_efficiency": round(
                self.weights.cost * normalized.recovery_cost, 12
            ),
            "delay_reduction": round(
                self.weights.delay * normalized.delay_reduction, 12
            ),
            "risk_avoidance": round(
                self.weights.risk * normalized.supplier_risk, 12
            ),
        }
        return UtilityScore(
            candidate_id=candidate_id,
            utility_score=round(sum(components.values()), 12),
            weighted_components=components,
        )

    def calculate_multiple(
        self, normalized_metrics_list: list[dict[str, Any]]
    ) -> list[UtilityScore]:
        scores = [
            self.calculate_utility(metrics) for metrics in normalized_metrics_list
        ]
        ordered = sorted(scores, key=lambda item: (-item.utility_score, item.candidate_id))
        ranked = {
            item.candidate_id: UtilityScore(
                candidate_id=item.candidate_id,
                utility_score=item.utility_score,
                weighted_components=item.weighted_components,
                rank=index,
            )
            for index, item in enumerate(ordered, start=1)
        }
        return [
            ranked[item.candidate_id]
            for item in scores
        ]
