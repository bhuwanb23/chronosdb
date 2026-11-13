from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .errors import ContractError


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ContractError(f"invalid ISO timestamp: {value}") from error
    if parsed.tzinfo is None:
        raise ContractError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(UTC)


@dataclass(frozen=True)
class SimulationHorizon:
    as_of_time: datetime
    simulation_end_time: datetime

    def __post_init__(self) -> None:
        if self.simulation_end_time <= self.as_of_time:
            raise ContractError("simulation_end_time must be after as_of_time")

    @property
    def days(self) -> int:
        return (self.simulation_end_time - self.as_of_time).days


@dataclass(frozen=True)
class ImpactRequest:
    scenario_id: str
    disruption_event_id: str
    horizon: SimulationHorizon
    rule_set_version: str
    allocation_policy: str
    scheduling_policy: str

    @classmethod
    def from_dict(cls, payload: dict[str, str]) -> ImpactRequest:
        as_of = parse_time(payload["as_of_time"])
        end = parse_time(payload["simulation_end_time"])
        if not payload.get("scenario_id") or not payload.get("disruption_event_id"):
            raise ContractError("scenario_id and disruption_event_id are required")
        return cls(
            scenario_id=payload["scenario_id"],
            disruption_event_id=payload["disruption_event_id"],
            horizon=SimulationHorizon(as_of, end),
            rule_set_version=payload["rule_set_version"],
            allocation_policy=payload["allocation_policy"],
            scheduling_policy=payload["scheduling_policy"],
        )
