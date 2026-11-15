"""Validate Phase 7 end to end against the live engine and frozen golden data."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from src.backend.chronosdb.optimization.benchmark import BenchmarkEvaluator
from src.backend.chronosdb.optimization.constraints import ConstraintRegistry
from src.backend.chronosdb.optimization.contracts import ConstraintCategory
from src.backend.chronosdb.optimization.engine import OptimizationEngine
from src.backend.chronosdb.optimization.golden import (
    GoldenScenario,
    default_golden_path,
)
from src.backend.chronosdb.optimization.handoff import HandoffEngine
from src.backend.chronosdb.optimization.ledger import OptimizationLedger
from src.backend.chronosdb.optimization.performance import PerformanceEvaluator


ARTIFACTS = ROOT / "artifacts" / "phase-7"


def _dump(name: str, payload: object) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object = "") -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    registry = ConstraintRegistry.load(ROOT / "config" / "constraints" / "registry.yaml")
    categories = {item.category for item in registry.constraint_set.constraints}
    check(
        "constraint_registry_categories",
        categories == set(ConstraintCategory),
        sorted(item.value for item in categories),
    )

    golden = GoldenScenario.load(default_golden_path(ROOT))
    golden_engine = OptimizationEngine(root=ROOT, objective=golden.objective)
    golden_result = golden.run(golden_engine)
    check(
        "golden_selected_candidate",
        golden_result.recommendation.candidate_id == "HYBRID",
        golden_result.recommendation.candidate_id,
    )
    check(
        "golden_cost",
        next(
            item.recovery_cost
            for item in golden_result.candidates
            if item.candidate_id == "HYBRID"
        )
        == 132000.0,
    )
    benchmark = BenchmarkEvaluator(golden.expected).evaluate(golden_result)
    check("golden_benchmark", benchmark["passed"], benchmark)

    second_engine = OptimizationEngine(root=ROOT, objective=golden.objective)
    second = golden.run(second_engine)
    check(
        "golden_reproducible_hash",
        second.result_hash == golden_result.result_hash,
        second.result_hash,
    )

    live_engine = OptimizationEngine(root=ROOT)
    live_result = live_engine.run()
    statuses = {item.candidate_id: item.status.value for item in live_result.feasibility}
    check(
        "live_selected_candidate",
        live_result.recommendation.candidate_id == "EXPEDITE",
        live_result.recommendation.candidate_id,
    )
    check(
        "live_hybrid_infeasible_under_real_cost",
        statuses.get("HYBRID") == "INFEASIBLE",
        statuses.get("HYBRID"),
    )
    check(
        "live_candidate_count",
        len(live_result.candidates) == 6,
        len(live_result.candidates),
    )
    check(
        "live_phase6_provenance",
        bool(live_result.provenance.rule_versions.get("phase6")),
        live_result.provenance.rule_versions,
    )
    handoff = HandoffEngine().prepare(
        live_result, live_result.optimization_run_id, live_engine.last_audit_reference
    )
    handoff_ok, handoff_errors = HandoffEngine().validate(handoff)
    check("phase8_handoff_contract", handoff_ok, handoff_errors)

    ledger_path = ARTIFACTS / "optimization-ledger.jsonl"
    if ledger_path.exists():
        ledger_path.unlink()
    ledger = OptimizationLedger(ledger_path)
    ledger.append(
        live_result,
        run_id=live_result.optimization_run_id,
        baseline_state_hash=live_result.baseline_state_hash,
    )
    rows = ledger.read_all()
    record_types = [row.get("record_type") for row in rows]
    check(
        "ledger_record_types",
        record_types
        == [
            "OPTIMIZATION_RUN",
            "INPUT",
            "CANDIDATE_SCORE",
            "CONSTRAINT_RESULT",
            "PARETO_RESULT",
            "RECOMMENDATION",
            "SENSITIVITY_RESULT",
        ],
        record_types,
    )
    check(
        "ledger_deterministic_run_id",
        bool(rows)
        and all(
            row["run_id"] == live_result.optimization_run_id
            and row["created_at"] == "deterministic"
            and len(row["record_hash"]) == 64
            for row in rows
        ),
    )

    performance = PerformanceEvaluator(budget_seconds=0.5).measure(
        lambda: golden.run(OptimizationEngine(root=ROOT, objective=golden.objective))
    )
    check(
        "optimization_performance_budget",
        performance["within_budget"],
        performance["elapsed_seconds"],
    )

    report = {
        "phase": 7,
        "status": "PASS" if all(item["passed"] for item in checks) else "FAIL",
        "checks": checks,
        "limitations": [
            "Live Phase 6 hybrid costs INR 852400 and is infeasible under the INR 200000 budget; the live recommendation is EXPEDITE. The specification's HYBRID expectation belongs to the frozen synthetic golden fixture, not the live scenario.",
            "Docker and Db2 are unavailable on this machine, so the JSONL ledger is verified but Db2 optimization-run persistence is not.",
            "No independent real-world optimization benchmark exists; accuracy is measured against the frozen fixture and Phase 6 consistency.",
        ],
    }
    _dump("phase7-validation-report.json", report)
    _dump("phase7-golden-result.json", golden_result.to_dict())
    _dump("phase7-live-result.json", live_result.to_dict())
    _dump("phase7-benchmark.json", benchmark)
    _dump("phase7-phase8-handoff.json", handoff)

    for item in checks:
        suffix = f" ({item['detail']})" if item["detail"] not in ("", None) else ""
        print(f"{'PASS' if item['passed'] else 'FAIL'} {item['check']}{suffix}")
    print(f"Phase 7 validation: {report['status']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
