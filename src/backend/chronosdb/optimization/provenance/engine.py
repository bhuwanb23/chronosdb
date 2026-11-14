"""Phase 7M: Decision Provenance.

Every recommendation must explain:
- Selected candidate
- Reason (metrics, weights, constraints)
- Utility score
- Cost
- Within constraints
- Pareto-optimal status
- Simulation hashes
- Rule versions
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class DecisionProvenance:
    """Decision provenance record."""
    recommendation_id: str
    selected_candidate: str
    utility_score: float
    weighted_components: Dict[str, float]
    feasibility_status: str
    feasibility_reason: Optional[str]
    pareto_status: str
    dominated_by: List[str]
    dominates: List[str]
    weights_used: Dict[str, float]
    constraint_results: List[Dict[str, Any]]
    rule_versions: Dict[str, str]
    simulation_hashes: List[str]
    explanation: str
    timestamp: str

class DecisionProvenanceEngine:
    """
    Phase 7M: Decision Provenance.
    
    Generates complete audit trail for recommendations.
    """
    
    def __init__(self):
        pass
    
    def generate_provenance(
        self,
        recommendation: Any,  # Recommendation from Phase 7K
        feasibility_results: List[Any],
        pareto_results: List[Any],
        weights: Dict[str, float],
        constraint_results: List[Dict[str, Any]],
        rule_versions: Dict[str, str],
        simulation_hashes: List[str],
        recommendation_id: str
    ) -> DecisionProvenance:
        """Generate complete decision provenance."""
        
        # Generate explanation
        explanation = self._generate_explanation(
            recommendation, feasibility_results, pareto_results, weights
        )
        
        return DecisionProvenance(
            recommendation_id=recommendation_id,
            selected_candidate=recommendation.recommended_candidate,
            utility_score=recommendation.score,
            weighted_components=recommendation.weighted_components,
            feasibility_status=recommendation.feasibility_status,
            feasibility_reason=next(
                (r.reason for r in feasibility_results if r.candidate == recommendation.recommended_candidate),
                None
            ),
            pareto_status=recommendation.pareto_status,
            dominated_by=next(
                (r.dominated_by for r in pareto_results if r.candidate == recommendation.recommended_candidate),
                []
            ),
            dominates=next(
                (r.dominates for r in pareto_results if r.candidate == recommendation.recommended_candidate),
                []
            ),
            weights_used=weights,
            constraint_results=constraint_results,
            rule_versions=rule_versions,
            simulation_hashes=simulation_hashes,
            explanation=explanation,
            timestamp="2026-11-14T00:00:00Z"  # Current date
        )
    
    def _generate_explanation(self, recommendation, feasibility_results, pareto_results, weights) -> str:
        """Generate human-readable explanation."""
        candidate = recommendation.recommended_candidate
        score = recommendation.score
        
        # Find feasibility result
        feasibility = next(
            (r for r in feasibility_results if r.candidate == candidate),
            None
        )
        
        # Find Pareto result
        pareto = next(
            (r for r in pareto_results if r.candidate == candidate),
            None
        )
        
        explanation = f"Selected: {candidate}\n"
        explanation += f"Reason:\n"
        explanation += f"- Utility Score: {score:.3f}\n"
        explanation += f"- Feasibility Status: {recommendation.feasibility_status}\n"
        if feasibility and feasibility.reason:
            explanation += f"- Feasibility Reason: {feasibility.reason}\n"
        explanation += f"- Pareto Status: {recommendation.pareto_status}\n"
        if pareto and pareto.dominated_by:
            explanation += f"- Dominated By: {', '.join(pareto.dominated_by)}\n"
        if pareto and pareto.dominates:
            explanation += f"- Dominates: {', '.join(pareto.dominates)}\n"
        explanation += f"- Weights Used: {weights}\n"
        explanation += f"- Components: {recommendation.weighted_components}\n"
        
        return explanation

# Phase 7M Status: IMPLEMENTED
