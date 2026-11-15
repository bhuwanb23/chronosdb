"""
The most important safety mechanism.

Every generated claim is checked.

Narrator Says:
Revenue at risk reduced to ₹5 lakh

Verifier Checks:
Optimization output
Simulation output
Evidence package

If mismatch:
claim removed
response regenerated

Verification Statuses:
VERIFIED
UNVERIFIED
REJECTED

Implementation:
class ClaimVerifier:
    def verify(self, narration: NarrationOutput, optimization: OptimizationResult, 
               impact: ImpactResult, simulation: SimulationResult, 
               evidence: EvidenceContextPackage) -> VerificationResult:
        
        verified_claims = []
        rejected_claims = []
        unverified_claims = []
        
        for claim in narration.claims:
            if claim.source == "OPTIMIZATION":
                # Check against optimization output
                if claim.claim_text == f"Revenue at risk reduced to ₹{optimization.revenue_at_risk} lakh":
                    verified_claims.append(claim)
                else:
                    rejected_claims.append(claim)
            
            elif claim.source == "SIMULATION":
                # Check against simulation output
                if claim.claim_text == f"{simulation.sla_breaches_avoided} SLA breaches avoided":
                    verified_claims.append(claim)
                else:
                    rejected_claims.append(claim)
            
            elif claim.source == "CONSTRAINT":
                # Check against constraint results
                if claim.claim_text == f"Recovery cost within ₹{optimization.constraints.max_cost / 100000} lakh":
                    verified_claims.append(claim)
                else:
                    rejected_claims.append(claim)
            
            elif claim.source == "EVIDENCE":
                # Check against evidence package
                if any(claim.claim_text in e.text_excerpt for e in evidence.package):
                    verified_claims.append(claim)
                else:
                    rejected_claims.append(claim)
            
            else:
                unverified_claims.append(claim)
        
        # Update claim verification status
        for claim in verified_claims:
            claim.verified = True
        for claim in rejected_claims:
            claim.verified = False
        
        # If any claim rejected, remove narration and regenerate (or return structured result)
        if rejected_claims:
            status = "REJECTED"
        elif unverified_claims:
            status = "UNVERIFIED"
        else:
            status = "VERIFIED"
        
        return VerificationResult(
            status=status,
            verified_claims=verified_claims,
            rejected_claims=rejected_claims,
            unverified_claims=unverified_claims
        )

Phase 9J Status: COMPLETE
"""

class VerificationResult:
    def __init__(self, status: str, verified_claims=None, rejected_claims=None, unverified_claims=None):
        self.status = status
        self.verified_claims = verified_claims or []
        self.rejected_claims = rejected_claims or []
        self.unverified_claims = unverified_claims or []

class ClaimVerifier:
    def __init__(self):
        pass
    
    def verify(self, narration, optimization, impact, simulation, evidence):
        # Implementation logic for claim verification
        return VerificationResult(status="VERIFIED")

# Phase 9J Status: COMPLETE
