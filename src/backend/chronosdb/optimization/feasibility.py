"""Phase 7E: deterministic feasibility screening before any scoring."""

from __future__ import annotations

from typing import Iterable

from .constraints import ConstraintRegistry, ConstraintSet
from .contracts import (
    CandidateMetrics,
    ConstraintSeverity,
    FeasibilityResult,
    FeasibilityStatus,
    OptimizationValidationError,
)


FEASIBLE = FeasibilityStatus.FEASIBLE.value
CONDITIONALLY_FEASIBLE = FeasibilityStatus.CONDITIONALLY_FEASIBLE.value
INFEASIBLE = FeasibilityStatus.INFEASIBLE.value


class FeasibilityValidationEngine:
    """Apply versioned constraints and classify every candidate."""

    def __init__(self, constraints: ConstraintSet) -> None:
        if not isinstance(constraints, ConstraintSet):
            raise OptimizationValidationError(
                "FeasibilityValidationEngine requires a ConstraintSet"
            )
        self.constraints = constraints

    @classmethod
    def from_registry(
        cls,
        registry: ConstraintRegistry,
        overrides: dict[str, object] | None = None,
    ) -> "FeasibilityValidationEngine":
        return cls(registry.with_overrides(overrides))

    def evaluate(self, candidate: CandidateMetrics) -> FeasibilityResult:
        results = self.constraints.evaluate(candidate)
        hard = tuple(
            item.name
            for item in results
            if item.applicable
            and not item.passed
            and item.severity == ConstraintSeverity.HARD.value
        )
        soft = tuple(
            item.name
            for item in results
            if item.applicable
            and not item.passed
            and item.severity == ConstraintSeverity.SOFT.value
        )
        warnings = tuple(candidate.warnings)
        if hard:
            status = FeasibilityStatus.INFEASIBLE
        elif soft or warnings:
            status = FeasibilityStatus.CONDITIONALLY_FEASIBLE
        else:
            status = FeasibilityStatus.FEASIBLE

        reasons = [
            item.reason
            for item in results
            if item.applicable and not item.passed and item.reason
        ]
        if warnings and not hard:
            reasons.append("simulation warnings require review")
        return FeasibilityResult(
            candidate_id=candidate.candidate_id,
            status=status,
            constraint_results=results,
            reason="; ".join(reasons),
            hard_violations=hard,
            soft_violations=soft,
        )

    def evaluate_many(
        self, candidates: Iterable[CandidateMetrics]
    ) -> tuple[FeasibilityResult, ...]:
        return tuple(self.evaluate(candidate) for candidate in candidates)

    # Compatibility names used by earlier Phase 7 scaffolding.
    def validate_candidate(self, candidate: CandidateMetrics | dict[str, object]):
        if isinstance(candidate, dict):
            candidate = CandidateMetrics.from_dict(candidate)
        return self.evaluate(candidate)

    def validate_candidates(self, candidates):
        normalized = [
            item if isinstance(item, CandidateMetrics) else CandidateMetrics.from_dict(item)
            for item in candidates
        ]
        return list(self.evaluate_many(normalized))

    def validate(self, candidates):
        return self.validate_candidates(candidates)
