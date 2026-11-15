"""Phase 6Q: Golden Intervention Scenarios.

Required locked scenarios:
GI-001 Inventory Transfer
GI-002 Purchase Expedition
GI-003 Alternate Supplier
GI-004 Reschedule Production
GI-005 Hybrid Recovery

Each scenario defines expected shortages, delays, SLA breaches, revenue.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


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
        root = Path(__file__).resolve().parents[3]
        expected = json.loads(
            (root / "data" / "golden" / "phase6-expected.json").read_text(
                encoding="utf-8"
            )
        )
        metadata = {
            "transfer": (
                "GOLD-TRANSFER-001",
                "GI-001 Inventory Transfer",
                "INT-TRANSFER",
                ["GI-001", "GOLD-TRANSFER", "TRANSFER"],
            ),
            "expedition": (
                "GOLD-EXPEDITION-001",
                "GI-002 Purchase Expedition",
                "INT-EXPEDITE",
                ["GI-002", "GOLD-EXPEDITION", "EXPEDITION"],
            ),
            "alternate_supplier": (
                "GOLD-SUPPLIER-001",
                "GI-003 Alternate Supplier",
                "INT-SUPPLIER",
                ["GI-003", "GOLD-SUPPLIER", "SUPPLIER"],
            ),
            "reschedule": (
                "GOLD-RESCHEDULE-001",
                "GI-004 Reschedule Production",
                "INT-RESCHEDULE",
                ["GI-004", "GOLD-RESCHEDULE", "RESCHEDULE"],
            ),
            "hybrid": (
                "GOLD-HYBRID-001",
                "GI-005 Hybrid Recovery",
                "INT-HYBRID",
                ["GI-005", "GOLD-HYBRID", "HYBRID"],
            ),
        }
        return [
            GoldenInterventionScenario(
                scenario_id=metadata[name][0],
                name=metadata[name][1],
                intervention_type=metadata[name][2],
                expected_shortages=int(values["expected_shortages"]),
                expected_delays_hours=float(values["scenario_delay_hours"]),
                expected_sla_breaches=2 - int(values["breaches_avoided"]),
                expected_revenue_at_risk=float(values["scenario_revenue_risk"]),
                expected_revenue_protected=float(values["revenue_protected"]),
                expected_intervention_cost=float(values["intervention_cost"]),
                aliases=metadata[name][3],
            )
            for name, values in expected.items()
        ]

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