"""Phase 7P: benchmark evaluation against frozen expected data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .contracts import OptimizationValidationError


@dataclass(frozen=True)
class BenchmarkEvaluator:
    expected: Mapping[str, Any]

    @classmethod
    def from_file(cls, path: Path) -> "BenchmarkEvaluator":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise OptimizationValidationError("benchmark file must be a mapping")
        return cls(expected=payload)

    def evaluate(self, result: Any) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        expected_selected = self.expected.get("selected_candidate_id")
        actual_selected = result.recommendation.candidate_id
        recommendation_accuracy = (
            1.0 if actual_selected == expected_selected else 0.0
        )
        checks.append(
            {
                "check": "selected_candidate",
                "expected": expected_selected,
                "actual": actual_selected,
                "passed": recommendation_accuracy == 1.0,
            }
        )

        expected_feasibility = self.expected.get("feasibility", {})
        actual_feasibility = {
            item.candidate_id: item.status.value for item in result.feasibility
        }
        feasibility_matches = sum(
            1
            for candidate_id, expected in expected_feasibility.items()
            if actual_feasibility.get(candidate_id) == expected
        )
        feasibility_accuracy = (
            feasibility_matches / len(expected_feasibility)
            if expected_feasibility
            else 1.0
        )
        checks.append(
            {
                "check": "feasibility_accuracy",
                "expected": expected_feasibility,
                "actual": actual_feasibility,
                "passed": feasibility_accuracy == 1.0,
            }
        )

        expected_utilities = self.expected.get("utilities", {})
        actual_utilities = {
            item.candidate_id: item.utility_score for item in result.utilities
        }
        utility_matches = sum(
            1
            for candidate_id, expected in expected_utilities.items()
            if abs(float(actual_utilities.get(candidate_id, float("nan"))) - float(expected))
            <= 1e-9
        )
        utility_fidelity = (
            utility_matches / len(expected_utilities) if expected_utilities else 1.0
        )
        checks.append(
            {
                "check": "utility_fidelity",
                "expected": expected_utilities,
                "actual": actual_utilities,
                "passed": utility_fidelity == 1.0,
            }
        )

        expected_frontier = set(self.expected.get("pareto_frontier", ()))
        actual_frontier = {
            item.candidate_id
            for item in result.pareto
            if item.status.value == "PARETO_OPTIMAL"
        }
        denominator = len(expected_frontier | actual_frontier)
        pareto_accuracy = (
            len(expected_frontier & actual_frontier) / denominator
            if denominator
            else 1.0
        )
        checks.append(
            {
                "check": "pareto_accuracy",
                "expected": sorted(expected_frontier),
                "actual": sorted(actual_frontier),
                "passed": pareto_accuracy >= 0.98,
            }
        )

        constraint_accuracy = feasibility_accuracy
        checks.append(
            {
                "check": "constraint_accuracy",
                "value": constraint_accuracy,
                "passed": constraint_accuracy == 1.0,
            }
        )
        overall_score = (
            feasibility_accuracy * 0.20
            + utility_fidelity * 0.20
            + constraint_accuracy * 0.20
            + pareto_accuracy * 0.20
            + recommendation_accuracy * 0.20
        )
        passed = (
            feasibility_accuracy >= 1.0
            and utility_fidelity >= 1.0
            and constraint_accuracy >= 1.0
            and pareto_accuracy >= 0.98
            and recommendation_accuracy >= 0.90
            and overall_score >= 0.90
        )
        return {
            "passed": passed,
            "score": overall_score,
            "feasibility_accuracy": feasibility_accuracy,
            "utility_fidelity": utility_fidelity,
            "constraint_accuracy": constraint_accuracy,
            "pareto_accuracy": pareto_accuracy,
            "recommendation_accuracy": recommendation_accuracy,
            "checks": checks,
        }
