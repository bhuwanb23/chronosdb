"""Phase 6Q: Golden Intervention Scenarios.

Required locked scenarios:
GI-001 Inventory Transfer
GI-002 Purchase Expedition
GI-003 Alternate Supplier
GI-004 Reschedule Production
GI-005 Hybrid Recovery

Each scenario defines expected shortages, delays, SLA breaches, revenue.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class GoldenInterventionScenario:
    """Golden intervention scenario."""
    scenario_id: str
    name: str
    intervention_type: str
    expected_shortages: int
    expected_delays_hours: float
    expected_sla_breaches: int
    expected_revenue_at_risk: float
    expected_revenue_protected: float
    expected_intervention_cost: float
    aliases: List[str] = field(default_factory=list)


class GoldenInterventionScenarios:
    """Phase 6Q: Golden Intervention Scenarios.

    Provides locked golden scenarios for intervention validation.
    """

    def __init__(self):
        self.scenarios = self._load_scenarios()
        self._index = {s.scenario_id: s for s in self.scenarios}
        for s in self.scenarios:
            for alias in s.aliases:
                self._index[alias] = s

    def _load_scenarios(self) -> List[GoldenInterventionScenario]:
        scenarios = [
            GoldenInterventionScenario(
                scenario_id="GOLD-TRANSFER-001",
                name="GI-001 Inventory Transfer",
                intervention_type="INT-TRANSFER",
                expected_shortages=1,
                expected_delays_hours=120.0,
                expected_sla_breaches=1,
                expected_revenue_at_risk=800000.0,
                expected_revenue_protected=800000.0,
                expected_intervention_cost=0.0,
                aliases=["GI-001", "GOLD-TRANSFER", "TRANSFER"],
            ),
            GoldenInterventionScenario(
                scenario_id="GOLD-EXPEDITION-001",
                name="GI-002 Purchase Expedition",
                intervention_type="INT-EXPEDITE",
                expected_shortages=0,
                expected_delays_hours=240.0,
                expected_sla_breaches=0,
                expected_revenue_at_risk=600000.0,
                expected_revenue_protected=1000000.0,
                expected_intervention_cost=8700.0,
                aliases=["GI-002", "GOLD-EXPEDITION", "EXPEDITION"],
            ),
            GoldenInterventionScenario(
                scenario_id="GOLD-SUPPLIER-001",
                name="GI-003 Alternate Supplier",
                intervention_type="INT-SUPPLIER",
                expected_shortages=1,
                expected_delays_hours=360.0,
                expected_sla_breaches=1,
                expected_revenue_at_risk=1000000.0,
                expected_revenue_protected=600000.0,
                expected_intervention_cost=45000.0,
                aliases=["GI-003", "GOLD-SUPPLIER", "SUPPLIER"],
            ),
            GoldenInterventionScenario(
                scenario_id="GOLD-RESCHEDULE-001",
                name="GI-004 Reschedule Production",
                intervention_type="INT-RESCHEDULE",
                expected_shortages=1,
                expected_delays_hours=300.0,
                expected_sla_breaches=1,
                expected_revenue_at_risk=1200000.0,
                expected_revenue_protected=400000.0,
                expected_intervention_cost=12000.0,
                aliases=["GI-004", "GOLD-RESCHEDULE", "RESCHEDULE"],
            ),
            GoldenInterventionScenario(
                scenario_id="GOLD-HYBRID-001",
                name="GI-005 Hybrid Recovery",
                intervention_type="INT-HYBRID",
                expected_shortages=0,
                expected_delays_hours=120.0,
                expected_sla_breaches=0,
                expected_revenue_at_risk=400000.0,
                expected_revenue_protected=1200000.0,
                expected_intervention_cost=132000.0,
                aliases=["GI-005", "GOLD-HYBRID", "HYBRID"],
            ),
        ]
        return scenarios

    def list_scenarios(self) -> List[GoldenInterventionScenario]:
        return self.scenarios

    def get_scenario(self, scenario_id: str) -> GoldenInterventionScenario:
        if scenario_id in self._index:
            return self._index[scenario_id]
        # Fallback: search by suffix/contains
        for s in self.scenarios:
            if scenario_id in s.scenario_id or scenario_id in s.aliases:
                return s
        raise ValueError(f"Golden scenario {scenario_id} not found")

# Phase 6Q Status: IMPLEMENTED