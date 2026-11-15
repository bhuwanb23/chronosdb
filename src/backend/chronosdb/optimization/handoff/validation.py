"""Phase 7A: Phase 6 Handoff Validation.

Confirm optimization operates only on validated simulation outputs.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Phase6Candidate:
    """Phase 6 simulation candidate handed to Phase 7."""
    scenario_name: str
    result_hash: str
    revenue_risk: float
    delay: float
    breaches: int
    cost: float
    warnings: List[str] = field(default_factory=list)
    feasibility_metadata: Dict[str, Any] = field(default_factory=dict)
    provenance: Dict[str, Any] = field(default_factory=dict)
    rule_version: str = "1.0.0"
    simulation_completed: bool = True


@dataclass
class Phase6Handoff:
    """Aggregated Phase 6 handoff for Phase 7."""
    candidates: List[Phase6Candidate]
    rule_version: str = "1.0.0"

    def validate_handoff(self) -> Dict[str, Any]:
        checks = {
            "scenario_hashes_valid": all(bool(c.result_hash) for c in self.candidates),
            "simulation_completed": all(c.simulation_completed for c in self.candidates),
            "metrics_available": all(
                c.revenue_risk is not None and c.delay is not None and c.breaches is not None and c.cost is not None
                for c in self.candidates
            ),
            "rule_versions_consistent": all(c.rule_version == self.rule_version for c in self.candidates),
            "candidate_count_ge_2": len(self.candidates) >= 2,
        }
        is_valid = all(checks.values())
        return {
            "status": "pass" if is_valid else "fail",
            "checks": checks,
            "candidate_count": len(self.candidates),
            "rule_version": self.rule_version,
        }


def validate_phase6_handoff_check(handoff: Phase6Handoff) -> Dict[str, Any]:
    return handoff.validate_handoff()


def is_handoff_valid(handoff: Phase6Handoff) -> bool:
    return validate_phase6_handoff_check(handoff)["status"] == "pass"


# Aliases
Phase6HandoffValidation = Phase6Handoff
HandoffValidation = Phase6Handoff

# Phase 7A Status: IMPLEMENTED