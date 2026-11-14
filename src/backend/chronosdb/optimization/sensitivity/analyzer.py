"""Phase 7L: Sensitivity Analysis.

Question: Would recommendation change if priorities changed?

Test Variations:
- Cost Weight ±20%
- SLA Weight ±20%
- Revenue Weight ±20%
- Delay Weight ±20%

Output:
{
  "stable": true,
  "winner_changes": 0
}
OR
{
  "stable": false,
  "switches_to": "TRANSFER"
}
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class SensitivityResult:
    """Sensitivity analysis result."""
    stable: bool
    winner_changes: int
    switches_to: Optional[str] = None
    weight_variations: List[Dict[str, Any]] = None
    analysis_summary: Dict[str, Any] = None

class SensitivityAnalysis:
    """
    Phase 7L: Sensitivity Analysis.
    
    Tests recommendation stability under weight variations.
    """
    
    def __init__(self, recommendation_selector):
        self.recommendation_selector = recommendation_selector
    
    def analyze_sensitivity(self, simulation_results: List[Dict[str, Any]], base_weights: Dict[str, float]) -> SensitivityResult:
        """
        Analyze sensitivity to weight variations.
        
        Variations: ±20% for each weight category.
        """
        base_recommendation = self.recommendation_selector.select_recommendation(
            simulation_results, base_weights
        )
        
        variations = []
        winner_changes = 0
        stable = True
        
        # Test variations for each weight category
        weight_categories = ["revenue_protected", "sla_saved", "cost", "delay", "risk"]
        
        for category in weight_categories:
            # +20% variation
            varied_weights_plus = base_weights.copy()
            varied_weights_plus[category] = min(1.0, base_weights[category] * 1.2)
            
            # Normalize weights to sum to 1.0
            total_plus = sum(varied_weights_plus.values())
            varied_weights_plus = {k: v / total_plus for k, v in varied_weights_plus.items()}
            
            rec_plus = self.recommendation_selector.select_recommendation(
                simulation_results, varied_weights_plus
            )
            
            variations.append({
                "category": category,
                "variation": "+20%",
                "weights": varied_weights_plus,
                "recommended_candidate": rec_plus.recommended_candidate,
                "score": rec_plus.score,
                "changed": rec_plus.recommended_candidate != base_recommendation.recommended_candidate
            })
            
            if rec_plus.recommended_candidate != base_recommendation.recommended_candidate:
                winner_changes += 1
                stable = False
            
            # -20% variation
            varied_weights_minus = base_weights.copy()
            varied_weights_minus[category] = max(0.01, base_weights[category] * 0.8)
            
            # Normalize weights to sum to 1.0
            total_minus = sum(varied_weights_minus.values())
            varied_weights_minus = {k: v / total_minus for k, v in varied_weights_minus.items()}
            
            rec_minus = self.recommendation_selector.select_recommendation(
                simulation_results, varied_weights_minus
            )
            
            variations.append({
                "category": category,
                "variation": "-20%",
                "weights": varied_weights_minus,
                "recommended_candidate": rec_minus.recommended_candidate,
                "score": rec_minus.score,
                "changed": rec_minus.recommended_candidate != base_recommendation.recommended_candidate
            })
            
            if rec_minus.recommended_candidate != base_recommendation.recommended_candidate:
                winner_changes += 1
                stable = False
        
        return SensitivityResult(
            stable=stable,
            winner_changes=winner_changes,
            switches_to=None if stable else variations[-1]["recommended_candidate"],
            weight_variations=variations,
            analysis_summary={
                "base_recommendation": base_recommendation.recommended_candidate,
                "base_score": base_recommendation.score,
                "total_variations": len(variations),
                "stable_count": sum(1 for v in variations if not v["changed"]),
                "changed_count": winner_changes
            }
        )

# Phase 7L Status: IMPLEMENTED
