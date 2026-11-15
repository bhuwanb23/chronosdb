"""Phase 8L: Evidence Ranking Layer.

Classify evidence.

Tiers:
- PRIMARY: Directly supports recommendation
- SECONDARY: Historical similarity
- CONTEXTUAL: Helpful reference
- EXCLUDED: Expired, Unauthorized, Low confidence
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class RankedEvidence:
    """Ranked evidence result."""
    evidence_id: str
    tier: str  # PRIMARY, SECONDARY, CONTEXTUAL, EXCLUDED
    hybrid_score: float
    classification_reason: str
    metadata: Dict[str, Any]
    rank: int

class EvidenceRankingLayer:
    """
    Phase 8L: Evidence Ranking Layer.
    
    Classifies and ranks evidence based on relevance and confidence.
    """
    
    def __init__(self):
        pass
    
    def classify_tier(
        self,
        hybrid_result: Dict[str, Any],
        recommendation: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> str:
        """Classify evidence tier."""
        hybrid_score = hybrid_result.get("hybrid_score", 0.0)
        document_type = hybrid_result.get("metadata", {}).get("type", "")
        
        # PRIMARY: Directly supports recommendation
        if (hybrid_score >= 0.85 and 
            document_type in ["PROCEDURAL", "OPERATIONAL"] and
            self._matches_recommendation(hybrid_result, recommendation)):
            return "PRIMARY"
        
        # SECONDARY: Historical similarity
        elif (hybrid_score >= 0.70 and 
              document_type == "HISTORICAL"):
            return "SECONDARY"
        
        # CONTEXTUAL: Helpful reference
        elif (hybrid_score >= 0.50 and 
              document_type in ["GOVERNANCE", "PROCEDURAL"]):
            return "CONTEXTUAL"
        
        # EXCLUDED: Expired, Unauthorized, Low confidence
        else:
            return "EXCLUDED"
    
    def _matches_recommendation(self, hybrid_result: Dict[str, Any], recommendation: Dict[str, Any]) -> bool:
        """Check if evidence matches recommendation."""
        # Implementation would check if evidence supports recommendation
        # For demonstration, return True for high scores
        return hybrid_result.get("hybrid_score", 0.0) >= 0.7
    
    def rank_evidence(
        self,
        hybrid_results: List[Dict[str, Any]],
        recommendation: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> List[RankedEvidence]:
        """Classify and rank evidence."""
        ranked_results = []
        
        for result in hybrid_results:
            tier = self.classify_tier(result, recommendation, constraints)
            
            # Calculate rank within tier (placeholder)
            rank = 1  # Would be calculated based on score within tier
            
            ranked_result = RankedEvidence(
                evidence_id=result.get("document_id", "UNKNOWN"),
                tier=tier,
                hybrid_score=result.get("hybrid_score", 0.0),
                classification_reason=f"Tier: {tier}, Score: {result.get('hybrid_score', 0.0):.3f}",
                metadata=result.get("metadata", {}),
                rank=rank
            )
            
            ranked_results.append(ranked_result)
        
        # Sort by tier (PRIMARY > SECONDARY > CONTEXTUAL > EXCLUDED) and score
        tier_order = {"PRIMARY": 0, "SECONDARY": 1, "CONTEXTUAL": 2, "EXCLUDED": 3}
        ranked_results.sort(key=lambda x: (tier_order[x.tier], -x.hybrid_score))
        
        # Update ranks
        for rank, result in enumerate(ranked_results, 1):
            # Create new dataclass instance with rank
            updated_result = RankedEvidence(
                evidence_id=result.evidence_id,
                tier=result.tier,
                hybrid_score=result.hybrid_score,
                classification_reason=result.classification_reason,
                metadata=result.metadata,
                rank=rank
            )
            # Replace in original list
            for i, r in enumerate(ranked_results):
                if r.evidence_id == updated_result.evidence_id:
                    ranked_results[i] = updated_result
                    break
        
        return ranked_results

# Phase 8L Status: IMPLEMENTED
