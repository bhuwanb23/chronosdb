"""Canonical Phase 7 optimization engine."""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .constraints import ConstraintRegistry
from .contracts import (
    SCORING_POLICY_VERSION,
    TIE_BREAK_POLICY,
    CandidateMetrics,
    DecisionProvenance,
    FeasibilityStatus,
    NoFeasibleCandidatesError,
    OptimizationObjective,
    OptimizationResult,
    OptimizationValidationError,
    ParetoResult,
    ParetoStatus,
    UtilityScore,
    canonical_hash,
)
from .feasibility import FeasibilityValidationEngine
from .handoff import HandoffEngine
from .ledger import OptimizationLedger
from .normalization import NormalizationEngine
from .observability import OptimizationObservability
from .pareto import ParetoEngine
from .phase6 import Phase6CandidateBuilder
from .provenance import ProvenanceTracker
from .recommendation import RecommendationSelector
from .review import ReviewGate
from .sensitivity import SensitivityAnalyzer
from .utility import UtilityScoringEngine


@dataclass
class OptimizationEngine:
    root: Path
    constraint_registry_path: Path | None = None
    objective: OptimizationObjective = field(default_factory=OptimizationObjective.balanced)
    overrides: Mapping[str, Any] | None = None
    observability_path: Path | None = None
    ledger_path: Path | None = None
    engine_version: str = "phase7-optimization-v1"

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        if self.constraint_registry_path is None:
            self.constraint_registry_path = (
                self.root / "config" / "constraints" / "registry.yaml"
            )
        self.observability = OptimizationObservability(path=self.observability_path)
        self._registry = ConstraintRegistry.load(self.constraint_registry_path)
        self._constraint_set = self._registry.with_overrides(self.overrides)
        self._last_audit_reference: str | None = None
        self._last_handoff: dict[str, Any] | None = None
        self._phase6_engine_cache: Any | None = None

    def warm(self) -> None:
        """Load the frozen Phase 6 baseline once for request-time reuse."""
        self._phase6_engine().baseline()

    def run(
        self,
        overlays_path: Path | None = None,
        run_id: str | None = None,
        ledger: OptimizationLedger | None = None,
        scenario_id: str | None = None,
    ) -> OptimizationResult:
        started = time.perf_counter()
        self.observability.clear()
        self.observability.emit("optimization_started", scenario="phase6-live")
        phase6_engine = self._phase6_engine()
        overlay_sets = (
            Phase6CandidateBuilder.default_overlay_sets(self.root)
            if overlays_path is None
            else Phase6CandidateBuilder.load_overlays(Path(overlays_path))
        )
        handoff = Phase6CandidateBuilder().build(phase6_engine, overlay_sets)
        self.observability.emit(
            "phase6_candidates_loaded",
            candidate_ids=[item.candidate_id for item in handoff.candidates],
        )
        return self._optimize_candidates(
            handoff.candidates,
            scenario_id=scenario_id or handoff.scenario_id,
            baseline_state_hash=handoff.baseline_state_hash,
            rule_set_version=handoff.rule_set_version,
            run_id=run_id,
            ledger=ledger,
            started=started,
        )

    def optimize_candidates(
        self,
        candidates: Sequence[CandidateMetrics],
        *,
        scenario_id: str,
        baseline_state_hash: str,
        rule_set_version: str,
        run_id: str | None = None,
        ledger: OptimizationLedger | None = None,
    ) -> OptimizationResult:
        started = time.perf_counter()
        self.observability.clear()
        self.observability.emit("optimization_started", scenario=scenario_id)
        return self._optimize_candidates(
            tuple(candidates),
            scenario_id=scenario_id,
            baseline_state_hash=baseline_state_hash,
            rule_set_version=rule_set_version,
            run_id=run_id,
            ledger=ledger,
            started=started,
        )

    def _optimize_candidates(
        self,
        candidates: Sequence[CandidateMetrics],
        *,
        scenario_id: str,
        baseline_state_hash: str,
        rule_set_version: str,
        run_id: str | None,
        ledger: OptimizationLedger | None,
        started: float,
    ) -> OptimizationResult:
        if not candidates:
            raise OptimizationValidationError("optimization requires candidates")
        seen: set[str] = set()
        for candidate in candidates:
            if candidate.candidate_id in seen:
                raise OptimizationValidationError(
                    f"duplicate candidate ID: {candidate.candidate_id}"
                )
            seen.add(candidate.candidate_id)

        feasibility_engine = FeasibilityValidationEngine(self._constraint_set)
        feasibility_results = feasibility_engine.evaluate_many(candidates)
        self.observability.emit(
            "feasibility_completed",
            statuses={item.candidate_id: item.status.value for item in feasibility_results},
        )
        feasible_ids = {
            item.candidate_id
            for item in feasibility_results
            if item.status
            in (FeasibilityStatus.FEASIBLE, FeasibilityStatus.CONDITIONALLY_FEASIBLE)
        }
        if not feasible_ids:
            raise NoFeasibleCandidatesError("no candidate satisfies the hard constraints")
        feasible = [item for item in candidates if item.candidate_id in feasible_ids]
        feasible_results = [
            item for item in feasibility_results if item.candidate_id in feasible_ids
        ]

        normalization_engine = NormalizationEngine()
        normalized = normalization_engine.normalize(feasible)
        utility_engine = UtilityScoringEngine(self.objective.weights)
        feasible_utilities = utility_engine.score_many(
            feasible, normalized, self.objective.weights
        )
        feasible_utility_map = {item.candidate_id: item for item in feasible_utilities}
        utilities: list[UtilityScore] = [
            feasible_utility_map.get(
                candidate.candidate_id,
                UtilityScore(
                    candidate_id=candidate.candidate_id,
                    utility_score=0.0,
                    weighted_components={},
                    rank=None,
                ),
            )
            for candidate in candidates
        ]
        self.observability.emit(
            "scoring_completed",
            utilities={item.candidate_id: item.utility_score for item in utilities},
        )

        feasible_pareto = ParetoEngine().compute(feasible)
        pareto_map = {item.candidate_id: item for item in feasible_pareto}
        pareto_results = tuple(
            pareto_map.get(
                candidate.candidate_id,
                ParetoResult(
                    candidate_id=candidate.candidate_id,
                    status=ParetoStatus.NOT_EVALUATED,
                    dominated_by=(),
                    dominates=(),
                ),
            )
            for candidate in candidates
        )
        recommendation = RecommendationSelector().select(
            candidates, feasibility_results, utilities, pareto_results, self.objective
        )
        sensitivity = SensitivityAnalyzer(self.objective.weights).analyze(
            feasible,
            feasible_results,
            normalized,
            feasible_pareto,
            feasible_utilities,
            recommendation.candidate_id,
        )
        self.observability.emit(
            "recommendation_completed",
            selected=recommendation.candidate_id,
            stable=sensitivity.stable,
        )

        candidate_map = {item.candidate_id: item for item in candidates}
        feasibility_map = {item.candidate_id: item for item in feasibility_results}
        pareto_map = {item.candidate_id: item for item in pareto_results}
        selected_candidate = candidate_map[recommendation.candidate_id]
        selected_feasibility = feasibility_map[recommendation.candidate_id]
        selected_pareto = pareto_map[recommendation.candidate_id]
        selected_constraint_results = self._constraint_set.evaluate(selected_candidate)

        review = ReviewGate().evaluate_context(
            feasibility=feasibility_results,
            selected_candidate=recommendation.candidate_id,
            selected_feasibility=selected_feasibility,
            warnings=(),
            simulation_status="COMPLETED",
            ranking=recommendation.provenance.get("ranking", []),
            utilities=utilities,
            pareto=pareto_results,
        )
        if not review["passed"]:
            raise OptimizationValidationError(
                "; ".join(review["failures"])
            )

        provenance_package = ProvenanceTracker().build(
            scenario_id,
            [item.candidate_id for item in candidates],
            [item.simulation_hash for item in candidates],
            self._constraint_set.version,
            rule_set_version,
            self.objective,
            recommendation,
            sensitivity,
        )
        audit_reference = provenance_package["audit_reference"]
        decision_provenance = DecisionProvenance(
            decision_id=provenance_package["ledger_hash"][:32],
            selected_candidate=recommendation.candidate_id,
            utility_score=recommendation.score,
            weighted_components=dict(recommendation.weighted_components),
            weights_used=self.objective.weights.to_dict(),
            objective=self.objective.objective.value,
            feasibility_status=recommendation.feasibility_status,
            feasibility_reason=selected_feasibility.reason,
            pareto_status=recommendation.pareto_status,
            dominated_by=selected_pareto.dominated_by,
            dominates=selected_pareto.dominates,
            candidate_ids=tuple(item.candidate_id for item in candidates),
            metric_values={
                "revenue_protected": selected_candidate.revenue_protected,
                "breaches_avoided": selected_candidate.breaches_avoided,
                "delay_reduction_hours": selected_candidate.delay_reduction_hours,
                "recovery_cost": selected_candidate.recovery_cost,
                "supplier_risk": selected_candidate.supplier_risk,
            },
            constraint_results=tuple(
                item.to_dict() for item in selected_constraint_results
            ),
            rule_versions={"phase6": rule_set_version, "phase7": self.engine_version},
            simulation_hashes={
                item.candidate_id: item.simulation_hash for item in candidates
            },
            scoring_policy_version=SCORING_POLICY_VERSION,
            tie_break_policy=TIE_BREAK_POLICY,
            explanation=recommendation.rationale,
        )

        result_hash = canonical_hash(
            {
                "scenario_id": scenario_id,
                "candidate_ids": [item.candidate_id for item in candidates],
                "simulation_hashes": [item.simulation_hash for item in candidates],
                "constraint_version": self._constraint_set.version,
                "objective": self.objective.to_dict(),
                "recommendation": recommendation.candidate_id,
                "sensitivity": sensitivity.to_dict(),
                "provenance": provenance_package["ledger_hash"],
            }
        )
        runtime_ms = (time.perf_counter() - started) * 1000
        result = OptimizationResult(
            optimization_run_id=run_id or f"opt-{result_hash[:16]}",
            scenario_id=scenario_id,
            objective=self.objective,
            candidates=tuple(candidates),
            feasibility=tuple(feasibility_results),
            normalized=tuple(normalized),
            utilities=tuple(utilities),
            pareto=tuple(pareto_results),
            recommendation=recommendation,
            sensitivity=sensitivity,
            provenance=decision_provenance,
            constraints_version=self._constraint_set.version,
            constraint_set=self._constraint_set.to_dict(),
            observability=self.observability.summary(),
            runtime_ms=runtime_ms,
            result_hash=result_hash,
            engine_version=self.engine_version,
            baseline_state_hash=baseline_state_hash,
            review=review,
        )

        ledger_to_use = ledger
        if ledger_to_use is None and self.ledger_path is not None:
            ledger_to_use = OptimizationLedger(self.ledger_path)
        if ledger_to_use is not None:
            ledger_to_use.append(
                result,
                run_id=result.optimization_run_id,
                baseline_state_hash=baseline_state_hash,
            )
            self.observability.emit("ledger_appended", path=str(ledger_to_use.path))

        self._last_audit_reference = audit_reference
        self._last_handoff = HandoffEngine().prepare(
            result, result.optimization_run_id, audit_reference
        )
        return result

    def _phase6_engine(self):
        if self._phase6_engine_cache is None:
            try:
                from chronosdb.simulation.counterfactual import Phase6Engine
            except Exception:  # pragma: no cover
                from src.chronosdb.simulation.counterfactual import Phase6Engine
            self._phase6_engine_cache = Phase6Engine(self.root)
        return self._phase6_engine_cache

    @property
    def last_audit_reference(self) -> str | None:
        return self._last_audit_reference

    @property
    def last_handoff(self) -> dict[str, Any] | None:
        return self._last_handoff
