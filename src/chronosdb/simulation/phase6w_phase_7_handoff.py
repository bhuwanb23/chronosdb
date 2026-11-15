"""Phase 6W: Phase 7 Handoff.

Prepares counterfactual results for Phase 7 optimization engine.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class Phase7CandidateInput:
    """Candidate result handed off to Phase 7."""
    scenario_name: str
    revenue_risk: float
    breaches: int
    delay_hours: float
    intervention_cost: float
    warnings: List[str] = field(default_factory=list)
    feasibility: bool = True
    provenance: str = ""
    result_hash: str = ""


@dataclass(frozen=True)
class Phase7HandoffPayload:
    """Payload for Phase 7."""
    do_nothing: Phase7CandidateInput
    transfer: Phase7CandidateInput
    expedite: Phase7CandidateInput
    alternate_supplier: Phase7CandidateInput
    reschedule: Phase7CandidateInput
    hybrid: Phase7CandidateInput
    metadata: Dict[str, Any] = field(default_factory=dict)


class Phase7HandoffEngine:
    """Phase 6W: Phase 7 Handoff Engine."""

    def build_handoff(self, results: Dict[str, Any]) -> Phase7HandoffPayload:
        """Build handoff payload from simulation results."""

        def _candidate(name: str, r: Dict[str, Any]) -> Phase7CandidateInput:
            return Phase7CandidateInput(
                scenario_name=name,
                revenue_risk=float(r.get("revenue_risk", 0.0)),
                breaches=int(r.get("breaches", 0)),
                delay_hours=float(r.get("delay_hours", 0.0)),
                intervention_cost=float(r.get("intervention_cost", 0.0)),
                warnings=list(r.get("warnings", [])),
                feasibility=bool(r.get("feasibility", True)),
                provenance=str(r.get("provenance", "")),
                result_hash=str(r.get("result_hash", "")),
            )

        return Phase7HandoffPayload(
            do_nothing=_candidate("DO_NOTHING", results.get("do_nothing", {})),
            transfer=_candidate("TRANSFER", results.get("transfer", {})),
            expedite=_candidate("EXPEDITE", results.get("expedite", {})),
            alternate_supplier=_candidate("ALTERNATE_SUPPLIER", results.get("alternate_supplier", {})),
            reschedule=_candidate("RESCHEDULE", results.get("reschedule", {})),
            hybrid=_candidate("HYBRID", results.get("hybrid", {})),
            metadata=dict(results.get("metadata", {})),
        )

    def to_dict(self, payload: Phase7HandoffPayload) -> Dict[str, Any]:
        return {
            "do_nothing": payload.do_nothing.__dict__,
            "transfer": payload.transfer.__dict__,
            "expedite": payload.expedite.__dict__,
            "alternate_supplier": payload.alternate_supplier.__dict__,
            "reschedule": payload.reschedule.__dict__,
            "hybrid": payload.hybrid.__dict__,
            "metadata": payload.metadata,
        }


# Aliases
Phase7Handoff = Phase7HandoffEngine

# Phase 6W Status: IMPLEMENTED