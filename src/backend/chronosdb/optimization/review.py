"""Phase 7R: deterministic human-review gate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .contracts import (
    FeasibilityResult,
    FeasibilityStatus,
    OptimizationValidationError,
)


@dataclass(frozen=True)
class ReviewGate:
    require_feasible: bool = True
    require_no_hard_violations: bool = True
    require_simulation_success: bool = True

    def evaluate(
        self,
        feasibility: Sequence[FeasibilityResult],
        warnings: Sequence[str] = (),
        simulation_status: str = "COMPLETED",
    ) -> dict[str, Any]:
        failures: list[str] = []
        if self.require_simulation_success and simulation_status != "COMPLETED":
            failures.append(f"simulation status is {simulation_status}")
        if self.require_no_hard_violations:
            for item in feasibility:
                if item.hard_violations:
                    failures.append(
                        f"{item.candidate_id} has hard violations: {', '.join(item.hard_violations)}"
                    )
        if self.require_feasible and not any(
            item.status
            in (FeasibilityStatus.FEASIBLE, FeasibilityStatus.CONDITIONALLY_FEASIBLE)
            for item in feasibility
        ):
            failures.append("no feasible candidate")
        if warnings:
            failures.append(f"simulation warnings: {', '.join(warnings)}")
        return {
            "passed": not failures,
            "failures": failures,
            "requires_human_review": bool(failures),
        }

    def evaluate_context(
        self,
        *,
        feasibility: Sequence[FeasibilityResult],
        selected_candidate: str,
        selected_feasibility: FeasibilityResult,
        warnings: Sequence[str] = (),
        simulation_status: str = "COMPLETED",
        ranking: Sequence[Any] = (),
        utilities: Sequence[Any] = (),
        pareto: Sequence[Any] = (),
    ) -> dict[str, Any]:
        failures: list[str] = []
        checks: dict[str, bool] = {}
        if self.require_simulation_success and simulation_status != "COMPLETED":
            failures.append(f"simulation status is {simulation_status}")
        checks["simulation_success"] = simulation_status == "COMPLETED"
        if not selected_candidate:
            failures.append("no selected candidate")
        checks["selected_candidate"] = bool(selected_candidate)
        if self.require_no_hard_violations and selected_feasibility.hard_violations:
            failures.append(
                f"{selected_candidate} has hard violations: {', '.join(selected_feasibility.hard_violations)}"
            )
        checks["selected_no_hard_violations"] = not selected_feasibility.hard_violations
        if selected_feasibility.status not in (
            FeasibilityStatus.FEASIBLE,
            FeasibilityStatus.CONDITIONALLY_FEASIBLE,
        ):
            failures.append(f"{selected_candidate} is not feasible")
        checks["selected_feasible"] = selected_feasibility.status in (
            FeasibilityStatus.FEASIBLE,
            FeasibilityStatus.CONDITIONALLY_FEASIBLE,
        )
        if self.require_feasible and not any(
            item.status
            in (FeasibilityStatus.FEASIBLE, FeasibilityStatus.CONDITIONALLY_FEASIBLE)
            for item in feasibility
        ):
            failures.append("no feasible candidate")
        checks["feasible_candidates_exist"] = any(
            item.status
            in (FeasibilityStatus.FEASIBLE, FeasibilityStatus.CONDITIONALLY_FEASIBLE)
            for item in feasibility
        )
        if warnings:
            failures.append(f"simulation warnings: {', '.join(warnings)}")
        checks["no_simulation_warnings"] = not bool(warnings)
        if not ranking:
            failures.append("recommendation ranking is empty")
        checks["ranking_present"] = bool(ranking)
        if not utilities:
            failures.append("utility scores are empty")
        checks["utility_scores_present"] = bool(utilities)
        if not pareto:
            failures.append("Pareto results are empty")
        checks["pareto_results_present"] = bool(pareto)
        return {
            "passed": not failures,
            "failures": failures,
            "requires_human_review": bool(failures),
            "checks": checks,
            "review_type": "domain_optimization_audit_judge",
        }
