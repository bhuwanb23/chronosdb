"""Phase 6M: Delta Computation Engine (Standalone)."""

from typing import Dict, Any

def compute_delta(baseline_metrics: Dict[str, Any], scenario_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase 6M: Delta Computation Engine.
    
    Compute savings:
    Revenue Protected = DoNothing Revenue Risk - Scenario Revenue Risk
    Breaches Avoided = DoNothing Breaches - Scenario Breaches
    Delay Reduction = DoNothing Delay - Scenario Delay
    """
    
    # Extract baseline metrics (DoNothing)
    baseline_revenue_risk = baseline_metrics.get("revenue_risk", 1600000.0)
    baseline_breaches = baseline_metrics.get("breaches", 2)
    baseline_delay = baseline_metrics.get("delay_hours", 288)
    
    # Extract scenario metrics
    scenario_revenue_risk = scenario_metrics.get("revenue_risk", 800000.0)
    scenario_breaches = scenario_metrics.get("breaches", 1)
    scenario_delay = scenario_metrics.get("delay_hours", 120)
    
    # Compute deltas
    revenue_protected = baseline_revenue_risk - scenario_revenue_risk
    breaches_avoided = baseline_breaches - scenario_breaches
    delay_reduction = baseline_delay - scenario_delay
    
    return {
        "revenue_protected": revenue_protected,
        "breaches_avoided": breaches_avoided,
        "delay_reduction_hours": delay_reduction,
        "baseline_revenue_risk": baseline_revenue_risk,
        "scenario_revenue_risk": scenario_revenue_risk,
        "baseline_breaches": baseline_breaches,
        "scenario_breaches": scenario_breaches,
        "baseline_delay_hours": baseline_delay,
        "scenario_delay_hours": scenario_delay
    }
