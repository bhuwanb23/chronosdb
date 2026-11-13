from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..contracts.errors import ContractError
from .versions import RuleDefinition, RuleSet


def load_rule_set(path: Path) -> RuleSet:
    payload: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
    rules = tuple(RuleDefinition.from_dict(rule) for rule in payload["rules"])
    if not payload["rule_set_version"].startswith("impact-rules-"):
        raise ContractError("invalid impact rule-set version")
    identifiers = [rule.rule_id for rule in rules]
    if len(identifiers) != len(set(identifiers)):
        raise ContractError("duplicate rule identifiers")
    if any(not rule.inputs or not rule.outputs for rule in rules):
        raise ContractError("every rule needs typed inputs and outputs")
    return RuleSet(
        version=payload["rule_set_version"],
        domain_model_version=payload["domain_model_version"],
        dataset_compatibility=tuple(payload["dataset_compatibility"]),
        rules=rules,
    )
