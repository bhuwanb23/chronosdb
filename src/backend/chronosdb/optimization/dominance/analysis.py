"""Phase 7J: Dominance Analysis.

Candidate A dominates B if:
- A ≥ B on all objectives
- AND A > B on at least one objective

Useful for UI and explanation.
"""

from typing import List, Dict, Any

class DominanceAnalysis:
    """
    Phase 7J: Dominance Analysis.
    
    Analyzes dominance relationships between candidates.
    """
    
    def __init__(self):
        pass
    
    def analyze_dominance(self, normalized_metrics_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze dominance relationships.
        
        Returns:
        {
            "dominance_matrix": [...],
            "dominated_candidates": [...],
            "dominating_candidates": [...],
            "analysis_summary": {...}
        }
        """
        dominance_matrix = []
        dominated_candidates = set()
        dominating_candidates = set()
        
        for i, candidate_a in enumerate(normalized_metrics_list):
            candidate_a_id = candidate_a.get("candidate", f"CANDIDATE_{i}")
            row = {"candidate": candidate_a_id, "dominates": [], "dominated_by": []}
            
            for j, candidate_b in enumerate(normalized_metrics_list):
                if i == j:
                    continue
                
                candidate_b_id = candidate_b.get("candidate", f"CANDIDATE_{j}")
                
                # Check if A dominates B
                if self._is_dominant(candidate_a, candidate_b):
                    row["dominates"].append(candidate_b_id)
                    dominating_candidates.add(candidate_a_id)
                
                # Check if B dominates A
                if self._is_dominant(candidate_b, candidate_a):
                    row["dominated_by"].append(candidate_b_id)
                    dominated_candidates.add(candidate_a_id)
            
            dominance_matrix.append(row)
        
        return {
            "dominance_matrix": dominance_matrix,
            "dominated_candidates": list(dominated_candidates),
            "dominating_candidates": list(dominating_candidates),
            "analysis_summary": {
                "total_candidates": len(normalized_metrics_list),
                "pareto_optimal_count": len(normalized_metrics_list) - len(dominated_candidates),
                "dominated_count": len(dominated_candidates)
            }
        }
    
    def _is_dominant(self, candidate_a: Dict[str, float], candidate_b: Dict[str, float]) -> bool:
        """Check if candidate A dominates candidate B."""
        # Benefit metrics (higher is better)
        benefit_keys = ["revenue_protected_norm", "breaches_avoided_norm", "delay_reduction_norm", "remaining_inventory_norm"]
        
        # Cost metrics (lower is better)
        cost_keys = ["revenue_risk_norm", "sla_breaches_norm", "delay_norm", "recovery_cost_norm", "capacity_usage_norm", "inventory_consumed_norm", "supplier_risk_norm"]
        
        a_dominates_b = True
        a_strictly_better = False
        
        # Check benefit metrics
        for key in benefit_keys:
            a_val = candidate_a.get(key, 0.0)
            b_val = candidate_b.get(key, 0.0)
            if a_val < b_val:
                a_dominates_b = False
                break
            elif a_val > b_val:
                a_strictly_better = True
        
        if not a_dominates_b:
            return False
        
        # Check cost metrics
        for key in cost_keys:
            a_val = candidate_a.get(key, 0.0)
            b_val = candidate_b.get(key, 0.0)
            if a_val > b_val:  # Higher cost is worse
                a_dominates_b = False
                break
            elif a_val < b_val:
                a_strictly_better = True
        
        return a_dominates_b and a_strictly_better

# Phase 7J Status: IMPLEMENTED
