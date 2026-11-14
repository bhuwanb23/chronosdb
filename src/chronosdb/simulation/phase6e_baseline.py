"""Phase 6E: Scenario Baseline Construction."""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class SimulationBaseline:
    """Frozen deterministic baseline for Phase 6 simulation."""
    baseline_id: str
    state_hash: str
    impact_run_id: str
    revenue_at_risk: float
    sla_breaches: int
    disruption_definition: Dict[str, Any]
    rule_set_version: str
    horizon: Dict[str, str]  # start_time, end_time

    # Accept Phase 5 parameters for compatibility with Golden Scenarios
    def __init__(self, baseline_id: str, state_hash: str, impact_run_id: str, 
                 revenue_at_risk: float, sla_breaches: int, disruption_definition: Dict[str, Any], 
                 rule_set_version: str, horizon: Dict[str, str],
                 **kwargs):
        # Extract Phase 5 parameters if provided (for backward compatibility)
        phase5_state_hash = kwargs.get('phase5_state_hash', state_hash)
        phase5_disruption = kwargs.get('phase5_disruption', disruption_definition)
        actual_rule_version = kwargs.get('rule_version', rule_set_version)
        
        object.__setattr__(self, 'baseline_id', baseline_id)
        object.__setattr__(self, 'state_hash', phase5_state_hash)
        object.__setattr__(self, 'impact_run_id', impact_run_id)
        object.__setattr__(self, 'revenue_at_risk', revenue_at_risk)
        object.__setattr__(self, 'sla_breaches', sla_breaches)
        object.__setattr__(self, 'disruption_definition', phase5_disruption)
        object.__setattr__(self, 'rule_set_version', actual_rule_version)
        object.__setattr__(self, 'horizon', horizon)

    def identity_check(self, other: 'SimulationBaseline') -> bool:
        """
        Identity Rule: Every candidate must share same state hash, disruption, horizon, rule set.
        Only overlay differs.
        """
        return (
            self.state_hash == other.state_hash and
            self.disruption_definition == other.disruption_definition and
            self.horizon == other.horizon and
            self.rule_set_version == other.rule_set_version
        )

# Keep original name for backward compatibility
ScenarioBaseline = SimulationBaseline

def construct_baseline(
    phase5_state_hash: str,
    phase5_disruption: Dict[str, Any],
    impact_run_id: str,
    revenue_at_risk: float,
    sla_breaches: int,
    rule_version: str,
    horizon: Dict[str, str]
) -> SimulationBaseline:
    """Construct baseline from Phase 5 state and disruption."""
    baseline_id = f"BASE-GOLD-{phase5_state_hash[:8]}"
    return SimulationBaseline(
        baseline_id=baseline_id,
        state_hash=phase5_state_hash,
        impact_run_id=impact_run_id,
        revenue_at_risk=revenue_at_risk,
        sla_breaches=sla_breaches,
        disruption_definition=phase5_disruption,
        rule_set_version=rule_version,
        horizon=horizon,
        phase5_state_hash=phase5_state_hash,
        phase5_disruption=phase5_disruption,
        rule_version=rule_version
    )
