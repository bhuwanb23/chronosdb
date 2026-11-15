"""Phase 7I: deterministic Pareto dominance and frontier discovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .contracts import (
    CandidateMetrics,
    NormalizedMetrics,
    OptimizationValidationError,
    ParetoResult,
    ParetoStatus,
)


@dataclass(frozen=True)
class DominanceComparison:
    candidate_id: str
    status: ParetoStatus
    dominated_by: tuple[str, ...]
    dominates: tuple[str, ...]


class ParetoEngine:
    """Multi-objective dominance over five oriented metrics.

    A candidate dominates another if it is at least as good on every objective
    and strictly better on one. Costs are already oriented in normalized space,
    but this method uses raw metrics with explicit direction so it can be audited
    without relying on normalization.
    """

    def __init__(self, tolerance: float = 1e-9) -> None:
        self.tolerance = tolerance

    def dominates(self, left: CandidateMetrics, right: CandidateMetrics) -> bool:
        values = (
            (left.revenue_protected, right.revenue_protected),
            (left.breaches_avoided, right.breaches_avoided),
            (left.delay_reduction_hours, right.delay_reduction_hours),
            (right.recovery_cost, left.recovery_cost),
            (right.supplier_risk, left.supplier_risk),
        )
        at_least_equal = all(a >= b - self.tolerance for a, b in values)
        strictly_better = any(a > b + self.tolerance for a, b in values)
        return at_least_equal and strictly_better

    def compute(
        self, candidates: Iterable[CandidateMetrics]
    ) -> tuple[ParetoResult, ...]:
        items = tuple(candidates)
        if not items:
            raise OptimizationValidationError("Pareto analysis requires candidates")
        results: list[ParetoResult] = []
        for candidate in items:
            dominated_by = tuple(
                other.candidate_id
                for other in items
                if other.candidate_id != candidate.candidate_id
                and self.dominates(other, candidate)
            )
            dominates = tuple(
                other.candidate_id
                for other in items
                if other.candidate_id != candidate.candidate_id
                and self.dominates(candidate, other)
            )
            results.append(
                ParetoResult(
                    candidate_id=candidate.candidate_id,
                    status=(
                        ParetoStatus.DOMINATED
                        if dominated_by
                        else ParetoStatus.PARETO_OPTIMAL
                    ),
                    dominated_by=dominated_by,
                    dominates=dominates,
                )
            )
        return tuple(results)

    def get_optimal(self, results: Iterable[ParetoResult]) -> tuple[str, ...]:
        return tuple(
            item.candidate_id
            for item in results
            if item.status == ParetoStatus.PARETO_OPTIMAL
        )

    def analyze(self, candidates: Iterable[CandidateMetrics]) -> list[dict[str, Any]]:
        results = self.compute(candidates)
        return [
            {
                "candidate_id": item.candidate_id,
                "pareto_optimal": item.status == ParetoStatus.PARETO_OPTIMAL,
                "dominated_by": list(item.dominated_by),
                "dominates": list(item.dominates),
            }
            for item in results
        ]

    # Compatibility with the old scaffold, which passed normalized dictionaries.
    def compute_from_normalized(
        self, candidates: Iterable[Mapping[str, Any]]
    ) -> tuple[ParetoResult, ...]:
        return self.compute_from_dicts(candidates)

    def compute_from_dicts(
        self, candidates: Iterable[Mapping[str, Any]]
    ) -> tuple[ParetoResult, ...]:
        converted = []
        for item in candidates:
            converted.append(
                CandidateMetrics(
                    candidate_id=str(item.get("candidate_id", item.get("candidate", ""))),
                    label=str(item.get("candidate_id", item.get("candidate", ""))),
                    revenue_risk=float(item.get("revenue_risk", 0.0)),
                    revenue_protected=float(item.get("revenue_protected", 0.0)),
                    sla_breaches=int(item.get("sla_breaches", 0)),
                    breaches_avoided=int(item.get("breaches_avoided", 0)),
                    delay_hours=float(item.get("delay", item.get("delay_hours", 0.0))),
                    delay_reduction_hours=float(
                        item.get("delay_reduction", item.get("delay_reduction_hours", 0.0))
                    ),
                    recovery_cost=float(item.get("recovery_cost", 0.0)),
                    capacity_utilization_pct=float(
                        item.get("capacity_usage", item.get("capacity_utilization_pct", 0.0))
                    ),
                    inventory_consumed=float(item.get("inventory_consumed", 0.0)),
                    remaining_inventory=float(item.get("remaining_inventory", 0.0)),
                    supplier_risk=float(item.get("supplier_risk", 0.0)),
                    simulation_hash=str(item.get("simulation_hash", "")),
                    rule_set_version=str(item.get("rule_set_version", "candidate-metrics-v1")),
                    baseline_result_hash=str(item.get("baseline_result_hash", "")),
                    source=str(item.get("source", "MANUAL")),
                )
            )
        return self.compute(converted)
