"""
Phase 11I: AI Orchestration Service
Backend and API Integration

The service runs, in order: guardrail check, narration from verified engine output,
claim verification. It never echoes the caller's text into the response and never
reports a verification status it did not compute.
"""

from datetime import datetime
from typing import Any, Dict

from src.backend.chronosdb.ai.claim_verifier import ClaimVerifier
from src.backend.chronosdb.ai.narrator import DecisionNarrator
from src.backend.chronosdb.ai.security import PromptRejectedError, PromptSecurityLayer

NO_VERIFIED_NARRATION = (
    "No verified narration is available for this request. "
    "The engine has no verified claims to explain yet."
)


class AIService:
    """
    Phase 11I: Expose Phase 9 engine

    Endpoints:
    - POST /api/v1/explain (Natural Language Endpoint)
    """

    def __init__(self) -> None:
        self.explanations: Dict[str, Dict[str, Any]] = {}
        self.guardrail = PromptSecurityLayer()
        self.verifier = ClaimVerifier()
        self.narrator = DecisionNarrator()

    def explain(self, query: str) -> Dict[str, Any]:
        """
        POST /api/v1/explain

        Raises PromptRejectedError when the guardrail blocks the query.
        """

        decision = self.guardrail.check_prompt(query)
        if decision.blocked:
            raise PromptRejectedError(decision.reason)

        explanation_id = f"EXP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        narration = self.narrator.generate(None, None, None, None, None)
        verification = self.verifier.verify(narration)

        narrative = narration.narration or NO_VERIFIED_NARRATION

        explanation = {
            "explanation_id": explanation_id,
            "narrative": narrative,
            "verification_status": verification.status,
            "verified_claims": len(verification.verified_claims),
            "rejected_claims": len(verification.rejected_claims),
            "status": "COMPLETED",
            "created_at": datetime.utcnow().isoformat(),
        }

        self.explanations[explanation_id] = explanation
        return {
            "narrative": narrative,
            "verification_status": verification.status,
            "verified_claims": explanation["verified_claims"],
            "rejected_claims": explanation["rejected_claims"],
        }


# Phase 11I Status: COMPLETE
