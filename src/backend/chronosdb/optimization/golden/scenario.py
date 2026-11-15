"""Phase 7O: Golden Optimization Scenario.

Locked Scenario:
Candidates: Do Nothing, Transfer, Expedite, Alternate Supplier, Hybrid
Expected Winner: Hybrid (for golden dataset)
Expected Metrics: Revenue Risk ↓, Revenue Protected ↑, Breaches ↓, Delay ↓, Cost within ₹2 lakh
Golden Requirement: Winner must exactly match frozen expected result
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class GoldenScenario:
    """Golden optimization scenario."""
    scenario_id: str
    description: str
    candidates: List[Dict[str, Any]]
    expected_winner: str
    expected_metrics: Dict[str, Any]
    expected_weights: Dict[str, float]
    expected_constraints: Dict[str, Any]
    golden_requirement: str

class GoldenOptimizationScenario:
    """
    Phase 7O: Golden Optimization Scenario.
    
    Provides standard golden scenario for benchmarking and testing.
    """
    
    def __init__(self):
        self.scenarios = self._load_scenarios()
    
    def _load_scenarios(self) -> List[GoldenScenario]:
        """Load standard golden optimization scenarios."""
        
        # Golden Scenario 1: Balanced Recovery
        scenario1 = GoldenScenario(
            scenario_id="GOLD-OPTIMIZATION-001",
            description="Golden Balanced Recovery Scenario",
            candidates=[
                {
                    "candidate": "DO_NOTHING",
                    "revenue_risk": 1600000.0,
                    "revenue_protected": 0.0,
                    "sla_breaches": 2,
                    "breaches_avoided": 0,
                    "delay": 720.0,
                    "delay_reduction": 0.0,
                    "recovery_cost": 0.0,
                    "capacity_usage": 0.0,
                    "inventory_consumed": 0.0,
                    "remaining_inventory": 1000.0,
                    "supplier_risk": 1.0,
                    "simulation_hash": "HASH-GOLD-DO-NOTHING"
                },
                {
                    "candidate": "TRANSFER",
                    "revenue_risk": 800000.0,
                    "revenue_protected": 800000.0,
                    "sla_breaches": 1,
                    "breaches_avoided": 1,
                    "delay": 480.0,
                    "delay_reduction": 240.0,
                    "recovery_cost": 50000.0,
                    "capacity_usage": 50.0,
                    "inventory_consumed": 320.0,
                    "remaining_inventory": 680.0,
                    "supplier_risk": 0.8,
                    "simulation_hash": "HASH-GOLD-TRANSFER"
                },
                {
                    "candidate": "EXPEDITE",
                    "revenue_risk": 600000.0,
                    "revenue_protected": 1000000.0,
                    "sla_breaches": 0,
                    "breaches_avoided": 2,
                    "delay": 240.0,
                    "delay_reduction": 480.0,
                    "recovery_cost": 120000.0,
                    "capacity_usage": 70.0,
                    "inventory_consumed": 400.0,
                    "remaining_inventory": 600.0,
                    "supplier_risk": 0.6,
                    "simulation_hash": "HASH-GOLD-EXPEDITE"
                },
                {
                    "candidate": "ALTERNATE_SUPPLIER",
                    "revenue_risk": 1000000.0,
                    "revenue_protected": 600000.0,
                    "sla_breaches": 1,
                    "breaches_avoided": 1,
                    "delay": 360.0,
                    "delay_reduction": 360.0,
                    "recovery_cost": 45000.0,
                    "capacity_usage": 40.0,
                    "inventory_consumed": 300.0,
                    "remaining_inventory": 700.0,
                    "supplier_risk": 0.4,
                    "simulation_hash": "HASH-GOLD-SUPPLIER"
                },
                {
                    "candidate": "RESCHEDULE",
                    "revenue_risk": 1200000.0,
                    "revenue_protected": 400000.0,
                    "sla_breaches": 1,
                    "breaches_avoided": 1,
                    "delay": 300.0,
                    "delay_reduction": 420.0,
                    "recovery_cost": 30000.0,
                    "capacity_usage": 60.0,
                    "inventory_consumed": 200.0,
                    "remaining_inventory": 800.0,
                    "supplier_risk": 0.7,
                    "simulation_hash": "HASH-GOLD-RESCHEDULE"
                },
                {
                    "candidate": "HYBRID",
                    "revenue_risk": 400000.0,
                    "revenue_protected": 1200000.0,
                    "sla_breaches": 0,
                    "breaches_avoided": 2,
                    "delay": 120.0,
                    "delay_reduction": 600.0,
                    "recovery_cost": 132000.0,
                    "capacity_usage": 80.0,
                    "inventory_consumed": 500.0,
                    "remaining_inventory": 500.0,
                    "supplier_risk": 0.3,
                    "simulation_hash": "HASH-GOLD-HYBRID"
                }
            ],
            expected_winner="HYBRID",
            expected_metrics={
                "revenue_risk_reduction": 1200000.0,
                "revenue_protected": 1200000.0,
                "breaches_avoided": 2,
                "delay_reduction": 600.0,
                "cost": 132000.0,
                "within_budget": True  # ₹1.32 lakh ≤ ₹2 lakh
            },
            expected_weights={
                "revenue_protected": 0.40,
                "sla_saved": 0.30,
                "cost": 0.15,
                "delay": 0.10,
                "risk": 0.05
            },
            expected_constraints={
                "max_recovery_cost": 200000,
                "min_safety_stock": 100,
                "supplier_approved": True,
                "transfer_lane_approved": True,
                "max_delay": 10,
                "capacity_utilization": 100
            },
            golden_requirement="Winner must exactly match frozen expected result (HYBRID)"
        )
        
        return [scenario1]
    
    def get_scenario(self, scenario_id: str) -> GoldenScenario:
        """Get specific golden scenario."""
        for scenario in self.scenarios:
            if scenario.scenario_id == scenario_id:
                return scenario
        raise ValueError(f"Golden scenario {scenario_id} not found")
    
    def list_scenarios(self) -> List[GoldenScenario]:
        """List all golden scenarios."""
        return self.scenarios

# Phase 7O Status: IMPLEMENTED
