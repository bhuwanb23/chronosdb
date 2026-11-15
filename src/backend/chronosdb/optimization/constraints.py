"""Versioned Phase 7 constraint registry and deterministic evaluators."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

import yaml

from .contracts import (
    CandidateMetrics,
    ConstraintCategory,
    ConstraintResult,
    ConstraintSeverity,
    OptimizationValidationError,
    _finite,
)


ALLOWED_OPERATORS = {"<=", ">=", "==", "<", ">"}


@dataclass(frozen=True)
class Constraint:
    constraint_id: str
    name: str
    category: ConstraintCategory
    operator: str
    value: Any
    unit: str
    severity: ConstraintSeverity
    description: str = ""

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Constraint":
        required = (
            "constraint_id",
            "name",
            "category",
            "operator",
            "value",
            "unit",
            "severity",
        )
        missing = [key for key in required if key not in payload]
        if missing:
            raise OptimizationValidationError(
                f"constraint missing fields: {', '.join(missing)}"
            )
        try:
            category = ConstraintCategory(str(payload["category"]).upper())
        except ValueError as exc:
            raise OptimizationValidationError(
                f"unsupported constraint category: {payload['category']}"
            ) from exc
        try:
            severity = ConstraintSeverity(str(payload["severity"]).upper())
        except ValueError as exc:
            raise OptimizationValidationError(
                f"unsupported constraint severity: {payload['severity']}"
            ) from exc
        operator = str(payload["operator"])
        if operator not in ALLOWED_OPERATORS:
            raise OptimizationValidationError(
                f"unsupported constraint operator: {operator}"
            )
        value = payload["value"]
        if isinstance(value, bool):
            pass
        elif isinstance(value, (int, float)):
            value = _finite(value, f"constraint {payload['constraint_id']} value")
        return cls(
            constraint_id=str(payload["constraint_id"]),
            name=str(payload["name"]),
            category=category,
            operator=operator,
            value=value,
            unit=str(payload["unit"]),
            severity=severity,
            description=str(payload.get("description", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "constraint_id": self.constraint_id,
            "name": self.name,
            "category": self.category.value,
            "operator": self.operator,
            "value": self.value,
            "unit": self.unit,
            "severity": self.severity.value,
            "description": self.description,
        }


def _metadata(candidate: CandidateMetrics) -> Mapping[str, Any]:
    return candidate.feasibility_metadata


def _actual_value(candidate: CandidateMetrics, name: str) -> tuple[Any, bool]:
    """Return (actual value, applicable).

    Applicability is explicit so a do-nothing plan is not failed for lacking a
    supplier or transfer lane. This prevents hidden assumptions in the model.
    """

    metadata = _metadata(candidate)
    if name == "max_recovery_cost":
        return candidate.recovery_cost, True
    if name == "min_remaining_inventory":
        return candidate.remaining_inventory, True
    if name == "max_capacity_utilization":
        return candidate.capacity_utilization_pct, bool(
            metadata.get("uses_capacity", False)
        )
    if name == "max_delay_hours":
        return candidate.delay_hours, True
    if name == "max_supplier_risk":
        return candidate.supplier_risk, True
    if name == "max_inventory_commitment":
        return candidate.inventory_consumed, True
    if name == "supplier_approved":
        return bool(metadata.get("supplier_approved", False)), bool(
            metadata.get("uses_supplier", False)
        )
    if name == "transfer_lane_approved":
        return bool(metadata.get("transfer_lane_approved", False)), bool(
            metadata.get("uses_transfer_lane", False)
        )
    if name == "regulatory_compliance":
        return bool(metadata.get("regulatory_compliance", False)), bool(
            metadata.get("uses_regulatory", False)
        )
    raise OptimizationValidationError(f"constraint has no evaluator: {name}")


def _compare(actual: Any, operator: str, threshold: Any) -> bool:
    try:
        left = actual
        right = threshold
        if isinstance(actual, bool) or isinstance(threshold, bool):
            if operator not in {"==", "!="}:
                if operator == "<=":
                    return int(bool(actual)) <= int(bool(threshold))
                if operator == ">=":
                    return int(bool(actual)) >= int(bool(threshold))
                raise OptimizationValidationError(
                    f"operator {operator} is invalid for boolean values"
                )
            return bool(actual) == bool(threshold)
        left = float(actual)
        right = float(threshold)
    except (TypeError, ValueError) as exc:
        raise OptimizationValidationError("constraint values must be comparable") from exc
    if operator == "<=":
        return left <= right
    if operator == ">=":
        return left >= right
    if operator == "<":
        return left < right
    if operator == ">":
        return left > right
    if operator == "==":
        return math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-9)
    raise OptimizationValidationError(f"unsupported operator: {operator}")


@dataclass(frozen=True)
class ConstraintSet:
    version: str
    constraints: tuple[Constraint, ...]
    source: str = "registry"

    def __post_init__(self) -> None:
        if not self.version:
            raise OptimizationValidationError("constraint version is required")
        if not self.constraints:
            raise OptimizationValidationError("constraint set cannot be empty")
        ids = [item.constraint_id for item in self.constraints]
        if len(ids) != len(set(ids)):
            raise OptimizationValidationError("duplicate constraint_id")
        names = [item.name for item in self.constraints]
        if len(names) != len(set(names)):
            raise OptimizationValidationError("duplicate constraint name")

    def evaluate(self, candidate: CandidateMetrics) -> tuple[ConstraintResult, ...]:
        results: list[ConstraintResult] = []
        for constraint in self.constraints:
            actual, applicable = _actual_value(candidate, constraint.name)
            if not applicable:
                results.append(
                    ConstraintResult(
                        constraint_id=constraint.constraint_id,
                        name=constraint.name,
                        category=constraint.category.value,
                        operator=constraint.operator,
                        threshold=constraint.value,
                        actual=actual,
                        passed=True,
                        severity=constraint.severity.value,
                        applicable=False,
                        reason=f"{constraint.name} is not used by this plan",
                    )
                )
                continue
            passed = _compare(actual, constraint.operator, constraint.value)
            reason = (
                f"{constraint.name} satisfied"
                if passed
                else (
                    f"{constraint.name} violated: {actual} {constraint.operator} "
                    f"{constraint.value} {constraint.unit}"
                )
            )
            results.append(
                ConstraintResult(
                    constraint_id=constraint.constraint_id,
                    name=constraint.name,
                    category=constraint.category.value,
                    operator=constraint.operator,
                    threshold=constraint.value,
                    actual=actual,
                    passed=passed,
                    severity=constraint.severity.value,
                    applicable=True,
                    reason=reason,
                )
            )
        return tuple(results)

    def with_overrides(self, overrides: Mapping[str, Any] | None) -> "ConstraintSet":
        if not overrides:
            return self
        by_name = {item.name: item for item in self.constraints}
        aliases = {
            "max_cost": "max_recovery_cost",
            "max_recovery_cost": "max_recovery_cost",
            "max_delay": "max_delay_hours",
            "max_delay_days": "max_delay_hours",
            "max_delay_hours": "max_delay_hours",
            "max_capacity_utilization": "max_capacity_utilization",
            "min_safety_stock": "min_remaining_inventory",
            "min_remaining_inventory": "min_remaining_inventory",
            "max_supplier_risk": "max_supplier_risk",
            "max_inventory_consumption": "max_inventory_commitment",
            "max_inventory_commitment": "max_inventory_commitment",
        }
        updated = dict(by_name)
        for key, raw_value in overrides.items():
            name = aliases.get(str(key), str(key))
            constraint = by_name.get(name)
            if constraint is None:
                raise OptimizationValidationError(f"unknown constraint override: {key}")
            value = raw_value
            if name == "max_delay_hours" and key in {"max_delay", "max_delay_days"}:
                value = _finite(raw_value, key) * 24.0
            elif name == "max_delay_hours":
                value = _finite(raw_value, key)
            elif isinstance(raw_value, bool):
                value = raw_value
            else:
                value = _finite(raw_value, key)
            updated[name] = replace(constraint, value=value)
        return ConstraintSet(
            version=self.version,
            constraints=tuple(updated.values()),
            source=f"{self.source}+overrides",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "source": self.source,
            "constraints": [item.to_dict() for item in self.constraints],
        }

    def thresholds(self) -> dict[str, Any]:
        return {item.name: item.value for item in self.constraints}


class ConstraintRegistry:
    """Load and version constraint definitions."""

    def __init__(self, constraint_set: ConstraintSet) -> None:
        self.constraint_set = constraint_set

    @classmethod
    def load(cls, path: Path) -> "ConstraintRegistry":
        if not path.exists():
            raise OptimizationValidationError(f"constraint registry not found: {path}")
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            raise OptimizationValidationError("constraint registry must be a mapping")
        version = payload.get("version")
        raw_constraints = payload.get("constraints")
        if not version or not isinstance(raw_constraints, list):
            raise OptimizationValidationError(
                "constraint registry requires version and constraints[]"
            )
        constraints = tuple(Constraint.from_dict(item) for item in raw_constraints)
        return cls(
            ConstraintSet(
                version=str(version),
                constraints=constraints,
                source=str(path),
            )
        )

    @property
    def version(self) -> str:
        return self.constraint_set.version

    def evaluate(self, candidate: CandidateMetrics) -> tuple[ConstraintResult, ...]:
        return self.constraint_set.evaluate(candidate)

    def with_overrides(self, overrides: Mapping[str, Any] | None) -> ConstraintSet:
        return self.constraint_set.with_overrides(overrides)
