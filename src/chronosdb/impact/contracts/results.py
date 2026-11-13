from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from .enums import DataQualityStatus, ImpactStatus


def _canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "value") and not isinstance(value, (str, int, float, bool)):
        return _canonical(value.value)
    return value


def canonical_hash(payload: Any) -> str:
    encoded = json.dumps(
        _canonical(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class StateIdentity:
    dataset_version: str
    state_version: str
    state_hash: str
    as_of_time: str


@dataclass
class ImpactResult:
    impact_run_id: str
    scenario_id: str
    status: ImpactStatus
    data_quality_status: DataQualityStatus
    rule_set_version: str
    input_state_hash: str
    affected_purchase_orders: list[dict[str, Any]] = field(default_factory=list)
    affected_components: list[str] = field(default_factory=list)
    inventory_timelines: list[dict[str, Any]] = field(default_factory=list)
    shortages: list[dict[str, Any]] = field(default_factory=list)
    affected_production_orders: list[dict[str, Any]] = field(default_factory=list)
    affected_customer_orders: list[dict[str, Any]] = field(default_factory=list)
    headline_metrics: dict[str, Any] = field(default_factory=dict)
    causal_traces: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    result_hash: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ImpactResult:
        return cls(
            impact_run_id=payload["impact_run_id"],
            scenario_id=payload["scenario_id"],
            status=ImpactStatus(payload["status"]),
            data_quality_status=DataQualityStatus(payload["data_quality_status"]),
            rule_set_version=payload["rule_set_version"],
            input_state_hash=payload["input_state_hash"],
            affected_purchase_orders=list(payload.get("affected_purchase_orders", [])),
            affected_components=list(payload.get("affected_components", [])),
            inventory_timelines=list(payload.get("inventory_timelines", [])),
            shortages=list(payload.get("shortages", [])),
            affected_production_orders=list(payload.get("affected_production_orders", [])),
            affected_customer_orders=list(payload.get("affected_customer_orders", [])),
            headline_metrics=dict(payload.get("headline_metrics", {})),
            causal_traces=list(payload.get("causal_traces", [])),
            warnings=list(payload.get("warnings", [])),
            errors=list(payload.get("errors", [])),
            provenance=dict(payload.get("provenance", {})),
            result_hash=payload.get("result_hash", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "impact_run_id": self.impact_run_id,
            "scenario_id": self.scenario_id,
            "status": self.status.value,
            "data_quality_status": self.data_quality_status.value,
            "rule_set_version": self.rule_set_version,
            "input_state_hash": self.input_state_hash,
            "affected_purchase_orders": self.affected_purchase_orders,
            "affected_components": self.affected_components,
            "inventory_timelines": self.inventory_timelines,
            "shortages": self.shortages,
            "affected_production_orders": self.affected_production_orders,
            "affected_customer_orders": self.affected_customer_orders,
            "headline_metrics": self.headline_metrics,
            "causal_traces": self.causal_traces,
            "warnings": self.warnings,
            "errors": self.errors,
            "provenance": self.provenance,
        }
        payload["result_hash"] = self.result_hash or canonical_hash(payload)
        return payload


def decimal(value: str | int | float | Decimal) -> Decimal:
    return Decimal(str(value))
