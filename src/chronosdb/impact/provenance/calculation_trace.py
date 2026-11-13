from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class CalculationTrace:
    step_id: str
    calculation_name: str
    rule_id: str
    rule_version: str
    input_record_ids: tuple[str, ...]
    output_fields: tuple[str, ...]
    value: Any
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "calculation_name": self.calculation_name,
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "input_record_ids": list(self.input_record_ids),
            "output_fields": list(self.output_fields),
            "value": self.value,
            "timestamp": _iso(self.timestamp),
        }


def metric_provenance(
    metric_id: str,
    metric_name: str,
    value: Any,
    unit: str,
    rule_id: str,
    rule_version: str,
    input_record_ids: Iterable[str],
    calculation_step_ids: Iterable[str],
    scenario_id: str,
    impact_run_id: str,
    state_hash: str,
    timestamp: datetime,
    data_quality_status: str,
) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
        "rule_id": rule_id,
        "rule_version": rule_version,
        "input_record_ids": sorted(set(input_record_ids)),
        "calculation_step_ids": sorted(set(calculation_step_ids)),
        "scenario_id": scenario_id,
        "impact_run_id": impact_run_id,
        "state_hash": state_hash,
        "timestamp": _iso(timestamp),
        "data_quality_status": data_quality_status,
    }
