"""Phase 7I: Pareto Frontier Engine.

One of the major differentiators.
Avoid assuming there is always one winner.

Output:
- PARETO_OPTIMAL
- DOMINATED
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class ParetoResult:
    """Pareto frontier result."""
    candidate: str
    status: str  # PARETO_OPTIMAL, DOMINATED
    dominated_by: Optional[List[str]] = None
    dominates: Optional[List[str]] = None

class ParetoFrontierEngine:
    """
    Phase 7I: Pareto Frontier Engine.
    
    Identifies Pareto-optimal candidates and dominated candidates.
    """
    
    def __init__(self):
        pass
    
    def is_dominant(self, candidate_a: Dict[str, float], candidate_b: Dict[str, float]) -> bool:
        """
        Check if candidate A dominates candidate B.
        
        A dominates B if:
        - A ≥ B on all objectives
        - AND A > B on at least one objective
        """
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
    
    def calculate_pareto_frontier(self, normalized_metrics_list: List[Dict[str, Any]]) -> List[ParetoResult]:
        """Calculate Pareto frontier for multiple candidates."""
        results = []
        
        for i, candidate_a in enumerate(normalized_metrics_list):
            candidate_id = candidate_a.get("candidate", f"CANDIDATE_{i}")
            dominated_by = []
            dominates = []
            
            for j, candidate_b in enumerate(normalized_metrics_list):
                if i == j:
                    continue
                
                # Check if A dominates B
                if self.is_dominant(candidate_a, candidate_b):
                    dominates.append(candidate_b.get("candidate", f"CANDIDATE_{j}"))
                
                # Check if B dominates A
                if self.is_dominant(candidate_b, candidate_a):
                    dominated_by.append(candidate_b.get("candidate", f"CANDIDATE_{j}"))
            
            status = "DOMINATED" if dominated_by else "PARETO_OPTIMAL"
            
            results.append(ParetoResult(
                candidate=candidate_id,
                status=status,
                dominated_by=dominated_by if dominated_by else None,
                dominates=dominates if dominates else None
            ))
        
        return results
    
    def get_pareto_frontier(self, normalized_metrics_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get only Pareto-optimal candidates."""
        results = self.calculate_pareto_frontier(normalized_metrics_list)
        pareto_optimal = []
        
        for result, metrics in zip(results, normalized_metrics_list):
            if result.status == "PARETO_OPTIMAL":
                pareto_optimal.append(metrics)
        
        return pareto_optimal

# Phase 7I Status: IMPLEMENTED
