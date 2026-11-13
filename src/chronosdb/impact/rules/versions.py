from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    version: str
    name: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    units: str
    formula: str
    rounding: str
    failure_conditions: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> RuleDefinition:
        return cls(
            rule_id=payload["rule_id"],
            version=str(payload["version"]),
            name=payload["name"],
            inputs=tuple(payload["inputs"]),
            outputs=tuple(payload["outputs"]),
            units=payload["units"],
            formula=payload["formula"],
            rounding=payload["rounding"],
            failure_conditions=tuple(payload["failure_conditions"]),
        )


@dataclass(frozen=True)
class RuleSet:
    version: str
    domain_model_version: str
    dataset_compatibility: tuple[str, ...]
    rules: tuple[RuleDefinition, ...]

    def get(self, rule_id: str) -> RuleDefinition:
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        raise KeyError(rule_id)
