"""Phase 7 contracts for deterministic intervention optimization.

The contract is deliberately independent of HTTP, LLMs, wall-clock time, and
database ordering. Every value that can change a recommendation is explicit.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping


OPTIMIZATION_ENGINE_VERSION = "chronosdb-optimization-engine-v1.0.0"
SCORING_POLICY_VERSION = "balanced-utility-v1.0.0"
RISK_POLICY_VERSION = "operational-risk-v1.0.0"
TIE_BREAK_POLICY = (
    "utility desc, revenue_protected desc, breaches_avoided desc, "
    "delay_reduction desc, recovery_cost asc, supplier_risk asc, candidate_id asc"
)


class OptimizationError(ValueError):
    """Base class for typed optimization failures."""


class OptimizationValidationError(OptimizationError):
    """One or more inputs violate the optimization contract."""


class DuplicateCandidateError(OptimizationValidationError):
    """The candidate set contains duplicate candidate identifiers."""


class NoFeasibleCandidatesError(OptimizationError):
    """No candidate satisfies the hard constraint set."""


class HandoffValidationError(OptimizationError):
    """A Phase 6 or Phase 8 handoff is incomplete or inconsistent."""


class ObjectiveName(StrEnum):
    MINIMIZE_REVENUE_RISK = "MINIMIZE_REVENUE_RISK"
    MINIMIZE_SLA_BREACHES = "MINIMIZE_SLA_BREACHES"
    MINIMIZE_DELAY = "MINIMIZE_DELAY"
    MINIMIZE_COST = "MINIMIZE_COST"
    MAXIMIZE_SERVICE_LEVEL = "MAXIMIZE_SERVICE_LEVEL"
    BALANCED_RECOVERY = "BALANCED_RECOVERY"


class FeasibilityStatus(StrEnum):
    FEASIBLE = "FEASIBLE"
    CONDITIONALLY_FEASIBLE = "CONDITIONALLY_FEASIBLE"
    INFEASIBLE = "INFEASIBLE"


class ParetoStatus(StrEnum):
    PARETO_OPTIMAL = "PARETO_OPTIMAL"
    DOMINATED = "DOMINATED"
    NOT_EVALUATED = "NOT_EVALUATED"


class ConstraintCategory(StrEnum):
    COST = "COST"
    INVENTORY = "INVENTORY"
    SUPPLIER = "SUPPLIER"
    WAREHOUSE = "WAREHOUSE"
    CAPACITY = "CAPACITY"
    DELAY = "DELAY"
    REGULATORY = "REGULATORY"


class ConstraintSeverity(StrEnum):
    HARD = "HARD"
    SOFT = "SOFT"


def canonical_hash(payload: Any) -> str:
    """Stable SHA-256 for audit hashes."""

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _finite(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise OptimizationValidationError(f"{field_name} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise OptimizationValidationError(f"{field_name} must be finite")
    return numeric


def _as_number(value: Any, field_name: str, default: float | None = None) -> float:
    if value is None:
        if default is None:
            raise OptimizationValidationError(f"missing required metric: {field_name}")
        return default
    return _finite(value, field_name)


@dataclass(frozen=True)
class WeightVector:
    """Five business weights. They must sum to exactly 1.0 (within float epsilon)."""

    revenue: float
    sla: float
    cost: float
    delay: float
    risk: float

    def __post_init__(self) -> None:
        values = {
            "revenue": _finite(self.revenue, "weights.revenue"),
            "sla": _finite(self.sla, "weights.sla"),
            "cost": _finite(self.cost, "weights.cost"),
            "delay": _finite(self.delay, "weights.delay"),
            "risk": _finite(self.risk, "weights.risk"),
        }
        for name, value in values.items():
            if value < 0.0 or value > 1.0:
                raise OptimizationValidationError(
                    f"weights.{name} must be between 0.0 and 1.0"
                )
        total = sum(values.values())
        if abs(total - 1.0) > 1e-9:
            raise OptimizationValidationError(
                f"weights must sum to 1.0, got {total:.12f}"
            )

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "WeightVector":
        aliases = {
            "revenue": ("revenue", "revenue_protected"),
            "sla": ("sla", "sla_saved", "sla_breaches"),
            "cost": ("cost", "recovery_cost"),
            "delay": ("delay", "remaining_delay"),
            "risk": ("risk", "supplier_risk", "operational_risk"),
        }
        resolved: dict[str, Any] = {}
        for target, names in aliases.items():
            for name in names:
                if name in payload:
                    resolved[target] = payload[name]
                    break
            else:
                raise OptimizationValidationError(f"missing weight: {target}")
        return cls(**resolved)

    def to_dict(self) -> dict[str, float]:
        return {
            "revenue": self.revenue,
            "sla": self.sla,
            "cost": self.cost,
            "delay": self.delay,
            "risk": self.risk,
        }

    def vary(self, target: str, factor: float) -> "WeightVector":
        """Change one weight and redistribute the remainder proportionally.

        The result still sums to 1.0, which is required by the contract. This
        makes sensitivity analysis a *priority* change, not an invalid weight set.
        """

        if target not in self.to_dict():
            raise OptimizationValidationError(f"unknown sensitivity weight: {target}")
        values = self.to_dict()
        original = values[target]
        changed = max(0.0, min(1.0, original * factor))
        others = {name: value for name, value in values.items() if name != target}
        remaining = 1.0 - changed
        other_total = sum(others.values())
        if other_total <= 1e-15:
            share = remaining / len(others)
            values = {name: share for name in others}
        else:
            values = {
                name: value / other_total * remaining for name, value in others.items()
            }
        values[target] = changed
        # Absorb tiny floating-point drift into the largest remaining weight.
        drift = 1.0 - sum(values.values())
        if abs(drift) > 1e-12:
            largest = max((name for name in values if name != target), key=values.get)
            values[largest] += drift
        return WeightVector(**values)


OBJECTIVE_WEIGHTS: dict[ObjectiveName, WeightVector] = {
    ObjectiveName.MINIMIZE_REVENUE_RISK: WeightVector(0.65, 0.20, 0.05, 0.05, 0.05),
    ObjectiveName.MINIMIZE_SLA_BREACHES: WeightVector(0.15, 0.65, 0.10, 0.05, 0.05),
    ObjectiveName.MINIMIZE_DELAY: WeightVector(0.15, 0.15, 0.05, 0.60, 0.05),
    ObjectiveName.MINIMIZE_COST: WeightVector(0.10, 0.10, 0.65, 0.10, 0.05),
    ObjectiveName.MAXIMIZE_SERVICE_LEVEL: WeightVector(0.45, 0.45, 0.03, 0.05, 0.02),
    ObjectiveName.BALANCED_RECOVERY: WeightVector(0.40, 0.30, 0.15, 0.10, 0.05),
}


@dataclass(frozen=True)
class OptimizationObjective:
    objective: ObjectiveName
    weights: WeightVector

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "OptimizationObjective":
        raw_name = payload.get("objective")
        if not raw_name:
            raise OptimizationValidationError("objective is required")
        try:
            name = ObjectiveName(str(raw_name))
        except ValueError as exc:
            allowed = ", ".join(item.value for item in ObjectiveName)
            raise OptimizationValidationError(
                f"unsupported objective {raw_name!r}; expected one of {allowed}"
            ) from exc
        raw_weights = payload.get("weights")
        weights = (
            WeightVector.from_mapping(raw_weights)
            if raw_weights is not None
            else OBJECTIVE_WEIGHTS[name]
        )
        return cls(name, weights)

    @classmethod
    def balanced(cls) -> "OptimizationObjective":
        return cls(
            ObjectiveName.BALANCED_RECOVERY,
            OBJECTIVE_WEIGHTS[ObjectiveName.BALANCED_RECOVERY],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective": self.objective.value,
            "weights": self.weights.to_dict(),
        }


@dataclass(frozen=True)
class CandidateMetrics:
    """All metrics required for deterministic optimization."""

    candidate_id: str
    label: str
    revenue_risk: float
    revenue_protected: float
    sla_breaches: int
    breaches_avoided: int
    delay_hours: float
    delay_reduction_hours: float
    recovery_cost: float
    capacity_utilization_pct: float
    inventory_consumed: float
    remaining_inventory: float
    supplier_risk: float
    simulation_hash: str
    rule_set_version: str
    baseline_result_hash: str
    source: str = "UNKNOWN"
    warnings: tuple[str, ...] = ()
    feasibility_metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_id", str(self.candidate_id).strip().upper())
        object.__setattr__(self, "label", str(self.label).strip())
        object.__setattr__(self, "source", str(self.source).strip().upper())
        object.__setattr__(self, "warnings", tuple(str(item) for item in self.warnings))
        object.__setattr__(
            self,
            "feasibility_metadata",
            dict(self.feasibility_metadata),
        )
        if not self.candidate_id:
            raise OptimizationValidationError("candidate_id is required")
        if not self.label:
            raise OptimizationValidationError("candidate label is required")
        for name in (
            "revenue_risk",
            "revenue_protected",
            "delay_hours",
            "delay_reduction_hours",
            "recovery_cost",
            "capacity_utilization_pct",
            "inventory_consumed",
            "remaining_inventory",
            "supplier_risk",
        ):
            _finite(getattr(self, name), name)
        if self.sla_breaches < 0 or self.breaches_avoided < 0:
            raise OptimizationValidationError(
                "SLA breach counts cannot be negative"
            )
        if self.revenue_risk < 0 or self.recovery_cost < 0:
            raise OptimizationValidationError(
                "revenue risk and recovery cost cannot be negative"
            )
        if self.delay_hours < 0 or self.delay_reduction_hours < 0:
            # Delay reduction can legitimately be negative when a plan worsens
            # delay. Delay itself cannot be negative.
            if self.delay_hours < 0:
                raise OptimizationValidationError("delay_hours cannot be negative")
        if self.supplier_risk < 0.0 or self.supplier_risk > 1.0:
            raise OptimizationValidationError("supplier_risk must be within [0, 1]")
        if self.capacity_utilization_pct < 0:
            raise OptimizationValidationError("capacity utilization cannot be negative")
        if self.remaining_inventory < 0:
            raise OptimizationValidationError("remaining inventory cannot be negative")
        if len(self.simulation_hash) != 64:
            raise OptimizationValidationError(
                "simulation_hash must be a 64-character SHA-256 hex digest"
            )
        try:
            int(self.simulation_hash, 16)
        except ValueError as exc:
            raise OptimizationValidationError(
                "simulation_hash must be hexadecimal"
            ) from exc
        if not self.rule_set_version:
            raise OptimizationValidationError("rule_set_version is required")
        if len(self.baseline_result_hash) != 64:
            raise OptimizationValidationError(
                "baseline_result_hash must be a 64-character SHA-256 hex digest"
            )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CandidateMetrics":
        candidate_id = payload.get("candidate_id", payload.get("candidate"))
        if candidate_id is None:
            raise OptimizationValidationError("candidate_id is required")
        delay = payload.get("delay_hours", payload.get("delay"))
        delay_reduction = payload.get(
            "delay_reduction_hours", payload.get("delay_reduction")
        )
        capacity = payload.get(
            "capacity_utilization_pct",
            payload.get("capacity_utilization", payload.get("capacity_usage", 0.0)),
        )
        return cls(
            candidate_id=str(candidate_id),
            label=str(payload.get("label", candidate_id)),
            revenue_risk=_as_number(payload.get("revenue_risk"), "revenue_risk"),
            revenue_protected=_as_number(
                payload.get("revenue_protected"), "revenue_protected"
            ),
            sla_breaches=int(
                _as_number(payload.get("sla_breaches"), "sla_breaches")
            ),
            breaches_avoided=int(
                _as_number(payload.get("breaches_avoided"), "breaches_avoided")
            ),
            delay_hours=_as_number(delay, "delay_hours"),
            delay_reduction_hours=_as_number(
                delay_reduction, "delay_reduction_hours"
            ),
            recovery_cost=_as_number(
                payload.get("recovery_cost", payload.get("cost")), "recovery_cost"
            ),
            capacity_utilization_pct=_as_number(
                capacity, "capacity_utilization_pct", 0.0
            ),
            inventory_consumed=_as_number(
                payload.get("inventory_consumed"), "inventory_consumed", 0.0
            ),
            remaining_inventory=_as_number(
                payload.get("remaining_inventory"), "remaining_inventory", 0.0
            ),
            supplier_risk=_as_number(
                payload.get("supplier_risk", payload.get("operational_risk")),
                "supplier_risk",
                0.0,
            ),
            simulation_hash=str(payload.get("simulation_hash", "")),
            rule_set_version=str(payload.get("rule_set_version", "")),
            baseline_result_hash=str(payload.get("baseline_result_hash", "")),
            source=str(payload.get("source", "FIXTURE")),
            warnings=tuple(payload.get("warnings", ())),
            feasibility_metadata=dict(payload.get("feasibility_metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate": self.candidate_id,
            "label": self.label,
            "source": self.source,
            "revenue_risk": self.revenue_risk,
            "revenue_protected": self.revenue_protected,
            "sla_breaches": self.sla_breaches,
            "breaches_avoided": self.breaches_avoided,
            "delay_hours": self.delay_hours,
            "delay": self.delay_hours,
            "delay_reduction_hours": self.delay_reduction_hours,
            "delay_reduction": self.delay_reduction_hours,
            "recovery_cost": self.recovery_cost,
            "cost": self.recovery_cost,
            "capacity_utilization_pct": self.capacity_utilization_pct,
            "inventory_consumed": self.inventory_consumed,
            "remaining_inventory": self.remaining_inventory,
            "supplier_risk": self.supplier_risk,
            "simulation_hash": self.simulation_hash,
            "rule_set_version": self.rule_set_version,
            "baseline_result_hash": self.baseline_result_hash,
            "warnings": list(self.warnings),
            "feasibility_metadata": dict(sorted(self.feasibility_metadata.items())),
        }


@dataclass(frozen=True)
class ConstraintResult:
    constraint_id: str
    name: str
    category: str
    operator: str
    threshold: Any
    actual: Any
    passed: bool
    severity: str
    applicable: bool = True
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "constraint_id": self.constraint_id,
            "name": self.name,
            "category": self.category,
            "operator": self.operator,
            "threshold": self.threshold,
            "actual": self.actual,
            "passed": self.passed,
            "severity": self.severity,
            "applicable": self.applicable,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class FeasibilityResult:
    candidate_id: str
    status: FeasibilityStatus
    constraint_results: tuple[ConstraintResult, ...]
    reason: str = ""
    hard_violations: tuple[str, ...] = ()
    soft_violations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate": self.candidate_id,
            "status": self.status.value,
            "reason": self.reason,
            "hard_violations": list(self.hard_violations),
            "soft_violations": list(self.soft_violations),
            "constraint_results": [item.to_dict() for item in self.constraint_results],
        }


@dataclass(frozen=True)
class NormalizedMetrics:
    candidate_id: str
    revenue_protected: float
    breaches_avoided: float
    delay_reduction: float
    recovery_cost: float
    supplier_risk: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "revenue_protected_norm": self.revenue_protected,
            "breaches_avoided_norm": self.breaches_avoided,
            "delay_reduction_norm": self.delay_reduction,
            "recovery_cost_norm": self.recovery_cost,
            "supplier_risk_norm": self.supplier_risk,
        }


@dataclass(frozen=True)
class UtilityScore:
    candidate_id: str
    utility_score: float
    weighted_components: Mapping[str, float]
    rank: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate": self.candidate_id,
            "utility_score": self.utility_score,
            "score": self.utility_score,
            "rank": self.rank,
            "weighted_components": dict(self.weighted_components),
        }


@dataclass(frozen=True)
class ParetoResult:
    candidate_id: str
    status: ParetoStatus
    dominated_by: tuple[str, ...] = ()
    dominates: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate": self.candidate_id,
            "status": self.status.value,
            "pareto_status": self.status.value,
            "dominated_by": list(self.dominated_by),
            "dominates": list(self.dominates),
        }


@dataclass(frozen=True)
class SensitivityVariation:
    category: str
    variation: str
    weights: Mapping[str, float]
    recommended_candidate: str
    score: float
    changed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "variation": self.variation,
            "weights": dict(self.weights),
            "recommended_candidate": self.recommended_candidate,
            "score": self.score,
            "changed": self.changed,
        }


@dataclass(frozen=True)
class SensitivityResult:
    stable: bool
    winner_changes: int
    base_winner: str
    switches_to: tuple[str, ...]
    variations: tuple[SensitivityVariation, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stable": self.stable,
            "winner_changes": self.winner_changes,
            "base_winner": self.base_winner,
            "switches_to": list(self.switches_to),
            "variations": [item.to_dict() for item in self.variations],
            "total_variations": len(self.variations),
            "stable_count": sum(1 for item in self.variations if not item.changed),
        }


@dataclass(frozen=True)
class Recommendation:
    candidate_id: str
    label: str
    score: float
    rank: int
    pareto_status: str
    feasibility_status: str
    weighted_components: Mapping[str, float]
    rationale: str
    provenance: Mapping[str, Any]

    @property
    def recommended_candidate(self) -> str:
        return self.candidate_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommended_candidate": self.candidate_id,
            "candidate_id": self.candidate_id,
            "label": self.label,
            "score": self.score,
            "utility_score": self.score,
            "rank": self.rank,
            "pareto_status": self.pareto_status,
            "feasibility_status": self.feasibility_status,
            "weighted_components": dict(self.weighted_components),
            "rationale": self.rationale,
            "provenance": dict(self.provenance),
        }


@dataclass(frozen=True)
class DecisionProvenance:
    decision_id: str
    selected_candidate: str
    utility_score: float
    weighted_components: Mapping[str, float]
    weights_used: Mapping[str, float]
    objective: str
    feasibility_status: str
    feasibility_reason: str
    pareto_status: str
    dominated_by: tuple[str, ...]
    dominates: tuple[str, ...]
    candidate_ids: tuple[str, ...]
    metric_values: Mapping[str, Any]
    constraint_results: tuple[Mapping[str, Any], ...]
    rule_versions: Mapping[str, str]
    simulation_hashes: Mapping[str, str]
    scoring_policy_version: str
    tie_break_policy: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "selected_candidate": self.selected_candidate,
            "utility_score": self.utility_score,
            "weighted_components": dict(self.weighted_components),
            "weights_used": dict(self.weights_used),
            "objective": self.objective,
            "feasibility_status": self.feasibility_status,
            "feasibility_reason": self.feasibility_reason,
            "pareto_status": self.pareto_status,
            "dominated_by": list(self.dominated_by),
            "dominates": list(self.dominates),
            "candidate_ids": list(self.candidate_ids),
            "metric_values": dict(self.metric_values),
            "constraint_results": [dict(item) for item in self.constraint_results],
            "rule_versions": dict(self.rule_versions),
            "simulation_hashes": dict(self.simulation_hashes),
            "scoring_policy_version": self.scoring_policy_version,
            "tie_break_policy": self.tie_break_policy,
            "explanation": self.explanation,
        }


@dataclass(frozen=True)
class OptimizationResult:
    optimization_run_id: str
    scenario_id: str
    objective: OptimizationObjective
    candidates: tuple[CandidateMetrics, ...]
    feasibility: tuple[FeasibilityResult, ...]
    normalized: tuple[NormalizedMetrics, ...]
    utilities: tuple[UtilityScore, ...]
    pareto: tuple[ParetoResult, ...]
    recommendation: Recommendation
    sensitivity: SensitivityResult
    provenance: DecisionProvenance
    constraints_version: str
    constraint_set: Mapping[str, Any]
    observability: Mapping[str, Any]
    runtime_ms: float
    result_hash: str
    engine_version: str = OPTIMIZATION_ENGINE_VERSION
    baseline_state_hash: str = ""
    review: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "optimization_run_id": self.optimization_run_id,
            "optimization_id": self.optimization_run_id,
            "scenario_id": self.scenario_id,
            "engine_version": self.engine_version,
            "objective": self.objective.objective.value,
            "weights": self.objective.weights.to_dict(),
            "constraints_version": self.constraints_version,
            "constraints": dict(self.constraint_set),
            "candidates": [item.to_dict() for item in self.candidates],
            "feasibility_results": [item.to_dict() for item in self.feasibility],
            "normalized_metrics": [item.to_dict() for item in self.normalized],
            "utility_scores": [item.to_dict() for item in self.utilities],
            "pareto_results": [item.to_dict() for item in self.pareto],
            "pareto_frontier": [
                item.candidate_id
                for item in self.pareto
                if item.status is ParetoStatus.PARETO_OPTIMAL
            ],
            "recommendation": self.recommendation.to_dict(),
            "recommended_candidate": self.recommendation.candidate_id,
            "utility_score": self.recommendation.score,
            "sensitivity": self.sensitivity.to_dict(),
            "provenance": self.provenance.to_dict(),
            "observability": dict(self.observability),
            "runtime_ms": self.runtime_ms,
            "result_hash": self.result_hash,
            "baseline_state_hash": self.baseline_state_hash,
            "review": dict(self.review),
        }
