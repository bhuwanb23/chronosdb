"""Phase 7S: handoff package for Phase 8 evidence generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .contracts import OptimizationResult, OptimizationValidationError


@dataclass(frozen=True)
class HandoffEngine:
    def prepare(
        self,
        result: OptimizationResult,
        run_id: str,
        audit_reference: str,
    ) -> dict[str, Any]:
        return {
            "schema_version": "phase7-to-phase8-v1",
            "recommendation": result.recommendation.to_dict(),
            "scenario_id": result.scenario_id,
            "result_hash": result.result_hash,
            "engine_version": result.engine_version,
            "optimization_run_id": run_id,
            "audit_reference": audit_reference,
            "evidence_package_created": False,
            "candidate_ranking": list(result.recommendation.provenance.get("ranking", [])),
            "selected_candidate_id": result.recommendation.candidate_id,
            "utilities": {
                item.candidate_id: item.to_dict() for item in result.utilities
            },
            "constraints": result.constraint_set,
            "constraint_version": result.constraints_version,
            "provenance": result.provenance.to_dict(),
            "simulation_references": {
                item.candidate_id: item.simulation_hash for item in result.candidates
            },
            "baseline_state_hash": result.baseline_state_hash,
        }

    def validate(self, package: Mapping[str, Any]) -> tuple[bool, list[str]]:
        required = [
            "recommendation",
            "scenario_id",
            "result_hash",
            "optimization_run_id",
            "audit_reference",
            "evidence_package_created",
            "candidate_ranking",
            "utilities",
            "constraints",
            "provenance",
            "simulation_references",
        ]
        errors = [f"missing {key}" for key in required if key not in package]
        if package.get("evidence_package_created") is not False:
            errors.append("evidence_package_created must be false")
        if not package.get("candidate_ranking"):
            errors.append("candidate_ranking must not be empty")
        if not package.get("simulation_references"):
            errors.append("simulation_references must not be empty")
        return not errors, errors

    # Compatibility names.
    def create_handoff(self, result: OptimizationResult, run_id: str, audit_reference: str):
        return self.prepare(result, run_id, audit_reference)

    def validate_handoff(self, package: Mapping[str, Any]):
        ok, errors = self.validate(package)
        return {"valid": ok, "errors": errors}


class HandoffValidation:
    def __init__(self) -> None:
        self.engine = HandoffEngine()

    def validate(self, package: Mapping[str, Any]):
        ok, errors = self.engine.validate(package)
        return {"valid": ok, "errors": errors}
