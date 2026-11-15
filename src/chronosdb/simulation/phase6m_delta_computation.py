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
    
    required = {"revenue_risk", "breaches", "delay_hours"}
    if not required.issubset(baseline_metrics) or not required.issubset(scenario_metrics):
        missing = (required - baseline_metrics.keys()) | (required - scenario_metrics.keys())
        raise ValueError(f"missing delta metrics: {sorted(missing)}")

    baseline_revenue_risk = baseline_metrics["revenue_risk"]
    baseline_breaches = baseline_metrics["breaches"]
    baseline_delay = baseline_metrics["delay_hours"]
    scenario_revenue_risk = scenario_metrics["revenue_risk"]
    scenario_breaches = scenario_metrics["breaches"]
    scenario_delay = scenario_metrics["delay_hours"]
    
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
