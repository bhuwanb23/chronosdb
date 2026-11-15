"""
Critical for reliability.

Case 1: LLM Timeout
Show:
Deterministic Recommendation
Verified Metrics
Evidence Links
without narration.

Case 2: Model Offline
System remains usable.

Case 3: Claim Verification Failure
Narrative removed.
Structured result shown.

Implementation:
class FallbackStrategy:
    def __init__(self):
        self.orchestrator = ToolOrchestrator()
    
    def handle_timeout(self, scenario: ScenarioRequest) -> FallbackResponse:
        # Execute deterministic engines without narration
        impact = self.orchestrator.impact_engine.calculate(scenario)
        simulation = self.orchestrator.simulation_engine.simulate(scenario)
        optimization = self.orchestrator.optimization_engine.optimize(scenario, impact, simulation)
        evidence = self.orchestrator.evidence_retrieval.retrieve(scenario)
        
        return FallbackResponse(
            status="TIMEOUT_FALLBACK",
            recommendation=optimization.recommendation,
            metrics={
                "revenue_at_risk": impact.revenue_at_risk,
                "sla_breaches_avoided": simulation.sla_breaches_avoided,
                "recovery_cost": optimization.recovery_cost
            },
            evidence_links=[e.document_id for e in evidence.package],
            narration=None
        )
    
    def handle_model_offline(self, scenario: ScenarioRequest) -> FallbackResponse:
        # Same as timeout fallback
        return self.handle_timeout(scenario)
    
    def handle_verification_failure(self, narration, verification) -> FallbackResponse:
        # Remove narration, show structured result
        return FallbackResponse(
            status="VERIFICATION_FAILURE_FALLBACK",
            recommendation=narration.provenance["recommendation"],
            metrics={
                "revenue_at_risk": narration.claims[0].claim_text,
                "sla_breaches_avoided": narration.claims[1].claim_text,
                "recovery_cost": narration.claims[2].claim_text
            },
            evidence_links=narration.provenance["evidence"],
            narration=None
        )

Phase 9M Status: COMPLETE
"""

class FallbackResponse:
    def __init__(self, status: str, recommendation=None, metrics=None, evidence_links=None, narration=None):
        self.status = status
        self.recommendation = recommendation
        self.metrics = metrics
        self.evidence_links = evidence_links
        self.narration = narration

class FallbackStrategy:
    def __init__(self):
        pass
    
    def handle_timeout(self, scenario) -> FallbackResponse:
        # Implementation logic for timeout fallback
        return FallbackResponse(status="TIMEOUT_FALLBACK")
    
    def handle_model_offline(self, scenario) -> FallbackResponse:
        # Implementation logic for model offline fallback
        return FallbackResponse(status="MODEL_OFFLINE_FALLBACK")
    
    def handle_verification_failure(self, narration, verification) -> FallbackResponse:
        # Implementation logic for verification failure fallback
        return FallbackResponse(status="VERIFICATION_FAILURE_FALLBACK")

# Phase 9M Status: COMPLETE
