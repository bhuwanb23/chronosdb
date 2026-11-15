"""Phase 7H: Utility Scoring Engine.

Core optimization function.

Utility Formula:
U = W1(SLA Saved) + W2(Revenue Protected) - W3(Cost) - W4(Remaining Delay) - W5(Operational Risk)

Recommended Default Weights:
- Revenue Protected = 40%
- SLA Saved = 30%
- Cost = 15%
- Delay = 10%
- Risk = 5%
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class UtilityScore:
    """Utility score result."""
    candidate: str
    utility_score: float
    weighted_components: Dict[str, float]
    rank: Optional[int] = None

class UtilityScoringEngine:
    """
    Phase 7H: Utility Scoring Engine.
    
    Calculates utility scores based on normalized metrics and weights.
    """
    
    def __init__(self, weights: Dict[str, float] = None):
        # Default weights if not provided
        self.weights = weights or {
            "revenue_protected": 0.40,
            "sla_saved": 0.30,
            "cost": 0.15,
            "delay": 0.10,
            "risk": 0.05
        }
        
        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    def calculate_utility(self, normalized_metrics: Dict[str, float]) -> UtilityScore:
        """Calculate utility score for single candidate."""
        candidate = normalized_metrics.get("candidate", "UNKNOWN")
        
        # Extract normalized values
        revenue_protected = normalized_metrics.get("revenue_protected_norm", 0.0)
        sla_saved = normalized_metrics.get("breaches_avoided_norm", 0.0)  # SLA saved = breaches avoided
        cost = normalized_metrics.get("recovery_cost_norm", 0.0)
        delay = normalized_metrics.get("delay_norm", 0.0)
        risk = normalized_metrics.get("supplier_risk_norm", 0.0)
        
        # Apply weights (benefit metrics positive, cost metrics negative)
        utility = (
            self.weights["revenue_protected"] * revenue_protected +
            self.weights["sla_saved"] * sla_saved -
            self.weights["cost"] * cost -
            self.weights["delay"] * delay -
            self.weights["risk"] * risk
        )
        
        # Calculate weighted components for provenance
        weighted_components = {
            "revenue_protected": self.weights["revenue_protected"] * revenue_protected,
            "sla_saved": self.weights["sla_saved"] * sla_saved,
            "cost": -self.weights["cost"] * cost,
            "delay": -self.weights["delay"] * delay,
            "risk": -self.weights["risk"] * risk,
            "total_utility": utility
        }
        
        return UtilityScore(
            candidate=candidate,
            utility_score=utility,
            weighted_components=weighted_components
        )
    
    def calculate_multiple(self, normalized_metrics_list: List[Dict[str, Any]]) -> List[UtilityScore]:
        """Calculate utility scores for multiple candidates."""
        scores = [self.calculate_utility(m) for m in normalized_metrics_list]
        
        # Assign ranks (1 = highest utility)
        sorted_scores = sorted(scores, key=lambda x: x.utility_score, reverse=True)
        for rank, score in enumerate(sorted_scores, 1):
            # Update the score object with rank (create new dataclass instance)
            updated_score = UtilityScore(
                candidate=score.candidate,
                utility_score=score.utility_score,
                weighted_components=score.weighted_components,
                rank=rank
            )
            # Replace in original list
            for i, s in enumerate(scores):
                if s.candidate == updated_score.candidate:
                    scores[i] = updated_score
                    break
        
        return scores

# Phase 7H Status: IMPLEMENTED
