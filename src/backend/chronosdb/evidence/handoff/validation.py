"""Phase 8A: Phase 7 Handoff Validation.

Verify optimization outputs are retrievable targets.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Phase7Handoff:
    """Aggregated Phase 7 handoff for Phase 8."""
    recommendation: str
    scenario_id: str
    result_hashes: List[str] = field(default_factory=list)
    optimization_run_id: str = ""
    audit_reference: str = ""
    evidence_package_created: bool = False
    candidate_rankings: List[Dict[str, Any]] = field(default_factory=list)
    utility_scores: List[Dict[str, Any]] = field(default_factory=list)
    constraint_results: List[Dict[str, Any]] = field(default_factory=list)
    decision_provenance: Dict[str, Any] = field(default_factory=dict)
    simulation_references: List[str] = field(default_factory=list)

    def validate_handoff(self) -> Dict[str, Any]:
        checks = {
            "recommendation_exists": bool(self.recommendation),
            "scenario_id_exists": bool(self.scenario_id),
            "result_hashes_exist": len(self.result_hashes) > 0 and all(bool(h) for h in self.result_hashes),
            "optimization_run_exists": bool(self.optimization_run_id),
            "audit_references_valid": bool(self.audit_reference),
            "evidence_package_not_created": not self.evidence_package_created,
        }
        is_valid = all(checks.values())
        return {
            "status": "pass" if is_valid else "fail",
            "checks": checks,
            "recommendation": self.recommendation,
            "scenario_id": self.scenario_id,
        }


def validate_phase7_handoff_check(handoff: Phase7Handoff) -> Dict[str, Any]:
    return handoff.validate_handoff()


def is_handoff_valid(handoff: Phase7Handoff) -> bool:
    return validate_phase7_handoff_check(handoff)["status"] == "pass"


Phase7HandoffValidation = Phase7Handoff
HandoffValidation = Phase7Handoff