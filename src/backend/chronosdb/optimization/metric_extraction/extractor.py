"""Phase 7F: Metric Extraction Layer.

Extract optimization metrics from Phase 6 simulation results.

Required Metrics:
- Revenue Risk / Revenue Protected
- SLA Breaches / Breaches Avoided
- Delay / Delay Reduction
- Recovery Cost
- Capacity Usage
- Inventory Consumed / Remaining
- Supplier Risk
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class ExtractedMetrics:
    """Extracted optimization metrics."""
    candidate: str
    revenue_risk: float
    revenue_protected: float
    sla_breaches: int
    breaches_avoided: int
    delay: float
    delay_reduction: float
    recovery_cost: float
    capacity_usage: float
    inventory_consumed: float
    remaining_inventory: float
    supplier_risk: float
    simulation_hash: str

class MetricExtractionLayer:
    """
    Phase 7F: Metric Extraction Layer.
    
    Extracts optimization metrics from Phase 6 simulation results.
    """
    
    def __init__(self):
        pass
    
    def extract_from_simulation(self, simulation_result: Dict[str, Any]) -> ExtractedMetrics:
        """Extract metrics from Phase 6 simulation result."""
        candidate = simulation_result.get("candidate", "UNKNOWN")
        simulation_hash = simulation_result.get("simulation_hash", "UNKNOWN")
        
        # Extract metrics from Phase 6 output
        revenue_risk = simulation_result.get("revenue_risk", 0.0)
        revenue_protected = simulation_result.get("revenue_protected", 0.0)
        sla_breaches = simulation_result.get("sla_breaches", 0)
        breaches_avoided = simulation_result.get("breaches_avoided", 0)
        delay = simulation_result.get("delay", 0.0)
        delay_reduction = simulation_result.get("delay_reduction", 0.0)
        recovery_cost = simulation_result.get("cost", 0.0)
        capacity_usage = simulation_result.get("capacity_usage", 0.0)
        inventory_consumed = simulation_result.get("inventory_consumed", 0.0)
        remaining_inventory = simulation_result.get("remaining_inventory", 0.0)
        supplier_risk = simulation_result.get("supplier_risk", 0.0)
        
        return ExtractedMetrics(
            candidate=candidate,
            revenue_risk=revenue_risk,
            revenue_protected=revenue_protected,
            sla_breaches=sla_breaches,
            breaches_avoided=breaches_avoided,
            delay=delay,
            delay_reduction=delay_reduction,
            recovery_cost=recovery_cost,
            capacity_usage=capacity_usage,
            inventory_consumed=inventory_consumed,
            remaining_inventory=remaining_inventory,
            supplier_risk=supplier_risk,
            simulation_hash=simulation_hash
        )
    
    def extract_multiple(self, simulation_results: List[Dict[str, Any]]) -> List[ExtractedMetrics]:
        """Extract metrics from multiple simulation results."""
        return [self.extract_from_simulation(result) for result in simulation_results]

# Phase 7F Status: IMPLEMENTED
