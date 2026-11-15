"""Phase 7L: deterministic provenance and audit references."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .contracts import (
    CandidateMetrics,
    ConstraintResult,
    FeasibilityResult,
    NormalizedMetrics,
    OptimizationValidationError,
    OptimizationResult,
    ParetoResult,
    Recommendation,
    SensitivityResult,
    UtilityScore,
    canonical_hash,
)


def _hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True)
class ProvenanceTracker:
    """Build immutable audit references without wall-clock time or UUIDs."""

    def build(
        self,
        scenario_id: str,
        candidate_ids: Sequence[str],
        simulation_hashes: Sequence[str],
        constraint_version: str,
        rule_set_version: str,
        objective: Any,
        recommendation: Recommendation,
        sensitivity: SensitivityResult,
    ) -> dict[str, Any]:
        if len(candidate_ids) != len(simulation_hashes):
            raise OptimizationValidationError("candidate and simulation hash counts differ")
        package = {
            "scenario_id": scenario_id,
            "candidate_ids": list(candidate_ids),
            "simulation_hashes": list(simulation_hashes),
            "constraint_version": constraint_version,
            "rule_set_version": rule_set_version,
            "objective": objective.to_dict() if hasattr(objective, "to_dict") else objective,
            "selected_candidate_id": recommendation.candidate_id,
            "sensitivity_stable": sensitivity.stable,
            "sensitivity_switches": list(sensitivity.switches_to),
        }
        return {
            "audit_reference": f"audit:{_hash(package)[:16]}",
            "ledger_hash": _hash(package),
            "package": package,
        }

    def attach(self, result: OptimizationResult, package: Mapping[str, Any]) -> OptimizationResult:
        return OptimizationResult(
            **{
                key: getattr(result, key)
                for key in result.__dataclass_fields__
                if key != "provenance"
            },
            provenance=dict(package),
        )

    def verify(self, result: OptimizationResult) -> bool:
        if not result.provenance:
            return False
        candidate_ids = [item.candidate_id for item in result.candidates]
        simulation_hashes = [item.simulation_hash for item in result.candidates]
        expected = self.build(
            result.scenario_id,
            candidate_ids,
            simulation_hashes,
            result.constraint_version,
            result.rule_set_version,
            result.objective,
            result.recommendation,
            result.sensitivity,
        )
        return expected["ledger_hash"] == result.provenance.get("ledger_hash")
