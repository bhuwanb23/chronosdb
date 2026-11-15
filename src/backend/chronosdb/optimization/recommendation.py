"""Phase 7J: deterministic, explainable recommendation selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from .contracts import (
    CandidateMetrics,
    FeasibilityResult,
    FeasibilityStatus,
    OptimizationValidationError,
    ParetoResult,
    ParetoStatus,
    Recommendation,
    UtilityScore,
)
from .utility import utility_sort_key


@dataclass(frozen=True)
class RecommendationSelector:
    """Select the best feasible candidate without hidden tie-breaking."""

    def select(
        self,
        candidates: Sequence[CandidateMetrics],
        feasibility: Sequence[FeasibilityResult],
        utilities: Sequence[UtilityScore],
        pareto: Sequence[ParetoResult],
        objective: Any = None,
    ) -> Recommendation:
        candidate_map = {item.candidate_id: item for item in candidates}
        feasibility_map = {item.candidate_id: item for item in feasibility}
        utility_map = {item.candidate_id: item for item in utilities}
        pareto_map = {item.candidate_id: item for item in pareto}
        if set(candidate_map) != {item.candidate_id for item in feasibility}:
            raise OptimizationValidationError("candidate and feasibility sets differ")
        if set(candidate_map) != {item.candidate_id for item in utilities}:
            raise OptimizationValidationError("candidate and utility sets differ")
        if set(candidate_map) != {item.candidate_id for item in pareto}:
            raise OptimizationValidationError("candidate and Pareto sets differ")

        eligible = [
            candidate
            for candidate in candidates
            if feasibility_map[candidate.candidate_id].status
            in (FeasibilityStatus.FEASIBLE, FeasibilityStatus.CONDITIONALLY_FEASIBLE)
        ]
        if not eligible:
            raise OptimizationValidationError("no feasible candidate can be recommended")

        ranking = sorted(
            eligible,
            key=lambda candidate: utility_sort_key(
                utility_map[candidate.candidate_id], candidate
            ),
        )
        selected = ranking[0]
        selected_feasibility = feasibility_map[selected.candidate_id]
        selected_utility = utility_map[selected.candidate_id]
        selected_pareto = pareto_map[selected.candidate_id]
        rank = next(
            index
            for index, item in enumerate(ranking, start=1)
            if item.candidate_id == selected.candidate_id
        )
        metric_values = {
            "revenue_protected": selected.revenue_protected,
            "breaches_avoided": selected.breaches_avoided,
            "delay_reduction_hours": selected.delay_reduction_hours,
            "recovery_cost": selected.recovery_cost,
            "supplier_risk": selected.supplier_risk,
        }
        rationale = (
            f"Selected {selected.candidate_id}: "
            f"INR {selected.revenue_protected:,.0f} revenue protected, "
            f"{selected.breaches_avoided} SLA breaches avoided, "
            f"{selected.delay_reduction_hours:,.0f} h delay reduction, "
            f"INR {selected.recovery_cost:,.0f} recovery cost, "
            f"risk {selected.supplier_risk:.2f}; "
            f"utility {selected_utility.utility_score:.6f}; "
            f"feasibility {selected_feasibility.status.value}; "
            f"{selected_pareto.status.value}; "
            f"hard violations: {len(selected_feasibility.hard_violations)}."
        )
        return Recommendation(
            candidate_id=selected.candidate_id,
            label=selected.label,
            score=selected_utility.utility_score,
            rank=rank,
            pareto_status=selected_pareto.status.value,
            feasibility_status=selected_feasibility.status.value,
            weighted_components=dict(selected_utility.weighted_components),
            rationale=rationale,
            provenance={
                "selected_simulation_hash": selected.simulation_hash,
                "ranking": [item.candidate_id for item in ranking],
                "weights": objective.weights.to_dict() if getattr(objective, "weights", None) else {},
            },
        )

    # Compatibility helper.
    def recommend(self, *args, **kwargs):
        return self.select(*args, **kwargs).to_dict()
