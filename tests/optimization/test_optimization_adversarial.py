"""Phase 7 end-to-end and adversarial tests.

Every test exercises the real implementation. No placeholder passes remain.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from src.backend.chronosdb.optimization.benchmark import BenchmarkEvaluator
from src.backend.chronosdb.optimization.constraints import ConstraintRegistry
from src.backend.chronosdb.optimization.contracts import (
    CandidateMetrics,
    FeasibilityStatus,
    NoFeasibleCandidatesError,
    OptimizationObjective,
    OptimizationValidationError,
    WeightVector,
)
from src.backend.chronosdb.optimization.engine import OptimizationEngine
from src.backend.chronosdb.optimization.feasibility import FeasibilityValidationEngine
from src.backend.chronosdb.optimization.golden import (
    GoldenScenario,
    default_golden_path,
)
from src.backend.chronosdb.optimization.handoff import HandoffEngine
from src.backend.chronosdb.optimization.ledger import OptimizationLedger
from src.backend.chronosdb.optimization.normalization import NormalizationEngine
from src.backend.chronosdb.optimization.pareto import ParetoEngine
from src.backend.chronosdb.optimization.performance import PerformanceEvaluator

ROOT = Path(__file__).resolve().parents[2]
HASH = hashlib.sha256(b"phase7-test-baseline").hexdigest()


def candidate(
    candidate_id: str,
    *,
    revenue_protected: float = 100.0,
    breaches_avoided: int = 0,
    delay_hours: float = 0.0,
    delay_reduction_hours: float = 0.0,
    recovery_cost: float = 100.0,
    supplier_risk: float = 0.0,
    inventory_consumed: float = 0.0,
    remaining_inventory: float = 100.0,
    capacity_utilization_pct: float = 0.0,
    metadata: dict | None = None,
) -> CandidateMetrics:
    return CandidateMetrics(
        candidate_id=candidate_id,
        label=candidate_id,
        revenue_risk=1_600_000.0 - revenue_protected,
        revenue_protected=revenue_protected,
        sla_breaches=0,
        breaches_avoided=breaches_avoided,
        delay_hours=delay_hours,
        delay_reduction_hours=delay_reduction_hours,
        recovery_cost=recovery_cost,
        capacity_utilization_pct=capacity_utilization_pct,
        inventory_consumed=inventory_consumed,
        remaining_inventory=remaining_inventory,
        supplier_risk=supplier_risk,
        simulation_hash=hashlib.sha256(candidate_id.encode()).hexdigest(),
        rule_set_version="phase7-test-v1",
        baseline_result_hash=HASH,
        source="FIXTURE",
        feasibility_metadata=metadata
        or {
            "uses_supplier": False,
            "uses_transfer_lane": False,
            "uses_capacity": False,
            "uses_regulatory": False,
            "supplier_approved": False,
            "transfer_lane_approved": False,
            "regulatory_compliance": False,
        },
    )


def golden() -> GoldenScenario:
    return GoldenScenario.load(default_golden_path(ROOT))


def golden_engine(scenario: GoldenScenario | None = None) -> OptimizationEngine:
    scenario = scenario or golden()
    return OptimizationEngine(root=ROOT, objective=scenario.objective)


def test_golden_scenario_selects_hybrid_and_is_reproducible() -> None:
    scenario = golden()
    first = scenario.run(golden_engine(scenario))
    second = scenario.run(golden_engine(scenario))
    assert first.recommendation.candidate_id == "HYBRID"
    assert first.recommendation.score == 0.889
    assert first.result_hash == second.result_hash
    assert [
        (item.candidate_id, item.status.value) for item in first.feasibility
    ] == [
        ("DO_NOTHING", "INFEASIBLE"),
        ("TRANSFER", "FEASIBLE"),
        ("EXPEDITE", "FEASIBLE"),
        ("ALTERNATE_SUPPLIER", "FEASIBLE"),
        ("RESCHEDULE", "INFEASIBLE"),
        ("HYBRID", "FEASIBLE"),
    ]
    assert first.provenance.tie_break_policy
    assert first.provenance.simulation_hashes


def test_golden_benchmark_passes_all_required_metrics() -> None:
    scenario = golden()
    result = scenario.run(golden_engine(scenario))
    report = BenchmarkEvaluator(scenario.expected).evaluate(result)
    assert report["passed"], report
    assert report["feasibility_accuracy"] == 1.0
    assert report["utility_fidelity"] == 1.0
    assert report["constraint_accuracy"] == 1.0
    assert report["pareto_accuracy"] == 1.0
    assert report["recommendation_accuracy"] == 1.0


def test_live_phase6_end_to_end_recommends_expedite() -> None:
    result = OptimizationEngine(root=ROOT).run()
    assert result.recommendation.candidate_id == "EXPEDITE"
    statuses = {item.candidate_id: item.status for item in result.feasibility}
    assert statuses["EXPEDITE"] is FeasibilityStatus.FEASIBLE
    assert statuses["TRANSFER"] is FeasibilityStatus.FEASIBLE
    assert statuses["HYBRID"] is FeasibilityStatus.INFEASIBLE
    assert statuses["ALTERNATE_SUPPLIER"] is FeasibilityStatus.INFEASIBLE
    assert len(result.candidates) == 6
    expedite = next(item for item in result.candidates if item.candidate_id == "EXPEDITE")
    assert expedite.recovery_cost == 3650.0
    assert expedite.revenue_protected == 1_600_000.0
    assert expedite.breaches_avoided == 2
    assert result.provenance.rule_versions["phase6"]


def test_phase6_handoff_is_valid() -> None:
    engine = OptimizationEngine(root=ROOT)
    result = engine.run()
    valid, errors = HandoffEngine().validate(engine.last_handoff)
    assert valid, errors
    assert engine.last_audit_reference.startswith("audit:")
    assert len(result.baseline_state_hash) == 64


def test_phase6_handoff_for_golden_metrics_is_not_applicable() -> None:
    # Golden metrics are declared FIXTURE, not PHASE6, and must never be silently
    # presented as a live simulation result.
    scenario = golden()
    assert all(item.source == "FIXTURE" for item in scenario.candidates)


def test_impossible_budget_rejects_candidate() -> None:
    engine = FeasibilityValidationEngine(
        ConstraintRegistry.load(ROOT / "config" / "constraints" / "registry.yaml").constraint_set
    )
    result = engine.evaluate(candidate("TOO_EXPENSIVE", recovery_cost=1_000_000.0))
    assert result.status is FeasibilityStatus.INFEASIBLE
    assert "max_recovery_cost" in result.hard_violations


def test_conflicting_constraints_produce_no_feasible_candidate() -> None:
    scenario = golden()
    engine = OptimizationEngine(
        root=ROOT,
        objective=scenario.objective,
        overrides={"max_recovery_cost": 1.0, "max_delay_hours": 0.0},
    )
    with pytest.raises(NoFeasibleCandidatesError):
        scenario.run(engine)


def test_negative_weights_are_rejected() -> None:
    with pytest.raises(OptimizationValidationError):
        WeightVector(-0.40, 0.30, 0.15, 0.10, 0.05)


def test_weights_above_one_and_bad_sum_are_rejected() -> None:
    with pytest.raises(OptimizationValidationError):
        WeightVector(0.60, 0.50, 0.20, 0.10, 0.10)
    with pytest.raises(OptimizationValidationError):
        WeightVector(1.20, 0.10, 0.10, 0.10, 0.10)


def test_missing_revenue_metric_raises_typed_error() -> None:
    with pytest.raises(OptimizationValidationError):
        CandidateMetrics.from_dict(
            {
                "candidate_id": "MISSING_REVENUE",
                "label": "Missing Revenue",
                "simulation_hash": hashlib.sha256(b"x").hexdigest(),
                "rule_set_version": "v1",
                "baseline_result_hash": HASH,
            }
        )


def test_duplicate_candidate_id_is_rejected() -> None:
    scenario = golden()
    engine = golden_engine(scenario)
    duplicate = scenario.candidates[0]
    with pytest.raises(OptimizationValidationError):
        engine.optimize_candidates(
            (duplicate, duplicate),
            scenario_id=scenario.scenario_id,
            baseline_state_hash=scenario.baseline_state_hash,
            rule_set_version=scenario.rule_set_version,
        )


def test_single_feasible_candidate_is_selected() -> None:
    scenario = golden()
    only = candidate("ONLY", recovery_cost=1000.0, delay_hours=0.0)
    result = golden_engine(scenario).optimize_candidates(
        (only,),
        scenario_id=scenario.scenario_id,
        baseline_state_hash=scenario.baseline_state_hash,
        rule_set_version=scenario.rule_set_version,
    )
    assert result.recommendation.candidate_id == "ONLY"
    assert result.normalized[0].revenue_protected == 0.0


def test_identical_candidates_tie_break_by_candidate_id() -> None:
    scenario = golden()
    left = candidate("ALPHA", revenue_protected=500.0)
    right = candidate("BETA", revenue_protected=500.0)
    result = golden_engine(scenario).optimize_candidates(
        (right, left),
        scenario_id=scenario.scenario_id,
        baseline_state_hash=scenario.baseline_state_hash,
        rule_set_version=scenario.rule_set_version,
    )
    assert result.recommendation.candidate_id == "ALPHA"
    assert result.recommendation.rank == 1


def test_soft_constraint_makes_candidate_conditional_not_infeasible() -> None:
    scenario = golden()
    risky = candidate("RISKY", supplier_risk=0.40)
    result = golden_engine(scenario).optimize_candidates(
        (risky,),
        scenario_id=scenario.scenario_id,
        baseline_state_hash=scenario.baseline_state_hash,
        rule_set_version=scenario.rule_set_version,
    )
    assert result.feasibility[0].status is FeasibilityStatus.CONDITIONALLY_FEASIBLE
    assert "max_supplier_risk" in result.feasibility[0].soft_violations


def test_normalization_is_over_candidate_set_not_cartesian_product() -> None:
    items = (
        candidate("A", recovery_cost=10.0, revenue_protected=10.0),
        candidate("B", recovery_cost=20.0, revenue_protected=20.0),
        candidate("C", recovery_cost=30.0, revenue_protected=30.0),
    )
    normalized = NormalizationEngine().normalize(items)
    assert len(normalized) == 3
    by_id = {item.candidate_id: item for item in normalized}
    assert by_id["A"].recovery_cost == 1.0
    assert by_id["C"].recovery_cost == 0.0
    assert by_id["A"].revenue_protected == 0.0
    assert by_id["C"].revenue_protected == 1.0
    assert len({item.candidate_id for item in normalized}) == 3


def test_pareto_dominance_and_frontier() -> None:
    strong = candidate("STRONG", revenue_protected=800.0, recovery_cost=10.0)
    weak = candidate("WEAK", revenue_protected=400.0, recovery_cost=20.0)
    results = ParetoEngine().compute((strong, weak))
    by_id = {item.candidate_id: item for item in results}
    assert by_id["STRONG"].status.value == "PARETO_OPTIMAL"
    assert by_id["WEAK"].status.value == "DOMINATED"
    assert by_id["WEAK"].dominated_by == ("STRONG",)


def test_sensitivity_varies_supplied_weights() -> None:
    scenario = golden()
    result = scenario.run(golden_engine(scenario))
    assert len(result.sensitivity.variations) == 8
    assert result.sensitivity.stable is True
    assert result.sensitivity.switches_to == ()
    for variation in result.sensitivity.variations:
        assert variation.weights != result.objective.weights.to_dict()
        assert variation.recommended_candidate == "HYBRID"


def test_ledger_is_deterministic_and_project_relative(tmp_path: Path) -> None:
    scenario = golden()
    path = tmp_path / "ledger.jsonl"
    ledger = OptimizationLedger(path)
    result = scenario.run(golden_engine(scenario), ledger=ledger)
    rows = ledger.read_all()
    assert len(rows) == 7
    assert [row["record_type"] for row in rows] == [
        "OPTIMIZATION_RUN",
        "INPUT",
        "CANDIDATE_SCORE",
        "CONSTRAINT_RESULT",
        "PARETO_RESULT",
        "RECOMMENDATION",
        "SENSITIVITY_RESULT",
    ]
    assert all(row["created_at"] == "deterministic" for row in rows)
    assert all(row["run_id"] == result.optimization_run_id for row in rows)
    assert all(row["result_hash"] == result.result_hash for row in rows)
    assert all(len(row["record_hash"]) == 64 for row in rows)
    assert "/home/user" not in path.read_text(encoding="utf-8")


def test_provenance_has_no_wall_clock_or_uuid() -> None:
    scenario = golden()
    result = scenario.run(golden_engine(scenario))
    payload = json.dumps(result.provenance.to_dict(), sort_keys=True)
    assert "uuid" not in payload.lower()
    assert "2026-" not in payload
    assert result.provenance.selected_candidate == "HYBRID"
    assert result.provenance.objective == "BALANCED_RECOVERY"


def test_optimization_performance_budget() -> None:
    scenario = golden()
    engine = golden_engine(scenario)
    report = PerformanceEvaluator(budget_seconds=0.5).measure(
        lambda: scenario.run(engine)
    )
    assert report["within_budget"], report["elapsed_seconds"]
    assert engine.observability.summary()["event_count"] >= 1
    assert engine.last_handoff is not None
    assert engine.last_handoff["selected_candidate_id"] == "HYBRID"
