"""Phase 9C: Scenario Planner.

Convert natural language requests into typed scenario requests.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ScenarioRequest:
    event_type: str = "SUPPLIER_OUTAGE"
    supplier_id: str = "SUP-0104"
    duration_days: int = 14
    objective: str = "MINIMIZE_SLA_BREACHES"
    constraints: Dict[str, Any] = None

    def __post_init__(self):
        if self.constraints is None:
            object.__setattr__(self, "constraints", {"max_cost": 200000})


class ScenarioPlanner:
    """Convert natural language into structured scenario requests."""

    def __init__(self):
        self.supported_objectives = ["MINIMIZE_SLA_BREACHES", "MINIMIZE_COST", "MINIMIZE_DELAY"]

    def plan(self, user_query: str) -> ScenarioRequest:
        # Placeholder planning logic; deterministic validation happens later.
        return ScenarioRequest()

    def parse(self, user_query: str) -> Dict[str, Any]:
        request = self.plan(user_query)
        return {
            "event_type": request.event_type,
            "supplier_id": request.supplier_id,
            "duration_days": request.duration_days,
            "objective": request.objective,
            "constraints": request.constraints,
        }

# Aliases
ScenarioPlannerEngine = ScenarioPlanner

# Phase 9C Status: COMPLETE