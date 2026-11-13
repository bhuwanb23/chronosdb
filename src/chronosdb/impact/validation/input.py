from __future__ import annotations

from ..contracts.errors import ContractError
from ..contracts.requests import ImpactRequest


def validate_request(request: ImpactRequest, supported_dataset_version: str = "1.0.0") -> None:
    if not request.rule_set_version.startswith("impact-rules-"):
        raise ContractError("unsupported rule-set version")
    if supported_dataset_version != "1.0.0":
        raise ContractError("unsupported dataset version")
