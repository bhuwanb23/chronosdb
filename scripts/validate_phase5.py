#!/usr/bin/env python3
"""Phase 5 end-to-end validation.

This is the release gate for the deterministic do-nothing impact engine. It
checks frozen inputs, runs the golden scenario, evaluates the benchmark
manifest, regenerates the handoff package, and verifies the required Phase 5
repository structure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from benchmarks.impact.compare_ground_truth import compare  # noqa: E402
from chronosdb.impact.contracts.results import canonical_hash  # noqa: E402
from scripts import impact_intake  # noqa: E402
from scripts import run_impact_benchmarks, run_phase5_golden  # noqa: E402

REQUIRED_FILES = [
    "config/rules/impact-rules-v1.0.0.yaml",
    "schemas/impact-request.schema.json",
    "schemas/impact-result.schema.json",
    "schemas/causal-trace.schema.json",
    "docs/impact-engine/phase-4-handoff-review.md",
    "docs/impact-engine/engine-contract.md",
    "docs/impact-engine/input-contract.md",
    "docs/impact-engine/output-contract.md",
    "docs/impact-engine/rule-catalogue.md",
    "docs/impact-engine/state-reconstruction.md",
    "docs/impact-engine/disruption-resolution.md",
    "docs/impact-engine/inbound-supply-projection.md",
    "docs/impact-engine/inventory-timeline.md",
    "docs/impact-engine/material-allocation.md",
    "docs/impact-engine/shortage-calculation.md",
    "docs/impact-engine/production-scheduling.md",
    "docs/impact-engine/customer-fulfilment.md",
    "docs/impact-engine/sla-and-financial-impact.md",
    "docs/impact-engine/causality-and-provenance.md",
    "docs/impact-engine/data-quality-and-partial-results.md",
    "docs/impact-engine/determinism-contract.md",
    "docs/impact-engine/execution-ledger.md",
    "docs/impact-engine/observability.md",
    "docs/impact-engine/review-signoff.md",
    "docs/impact-engine/phase-5-traceability-matrix.csv",
    "docs/impact-engine/phase-5-completion-report.md",
    "benchmarks/impact/run_impact_benchmark.py",
    "benchmarks/impact/compare_ground_truth.py",
    "benchmarks/impact/benchmark_config.yaml",
    "artifacts/phase-5/golden-impact-result.json",
    "artifacts/phase-5/golden-comparison-report.md",
    "artifacts/phase-5/impact-benchmark-results.json",
    "artifacts/phase-5/impact-benchmark-report.md",
    "artifacts/phase-5-handoff/impact-engine-contract.json",
    "artifacts/phase-5-handoff/rule-set-manifest.json",
    "artifacts/phase-5-handoff/golden-impact-result.json",
    "artifacts/phase-5-handoff/determinism-report.json",
    "artifacts/phase-5-handoff/performance-report.json",
    "artifacts/phase-5-handoff/error-catalogue.json",
    "artifacts/phase-5-handoff/causal-trace-schema.json",
    "artifacts/phase-5-handoff/phase-5-completion-report.md",
]

REQUIRED_TEST_DIRECTORIES = [
    "tests/impact/unit",
    "tests/impact/property",
    "tests/impact/integration",
    "tests/impact/temporal",
    "tests/impact/golden",
    "tests/impact/benchmark",
    "tests/impact/adversarial",
]

REQUIRED_RULE_IDS = {
    "STATE-001",
    "STATE-002",
    "SUP-001",
    "SUP-004",
    "SUP-005",
    "SUP-006",
    "INV-003",
    "INV-004",
    "ALLOC-001",
    "PROD-003",
    "FUL-001",
    "SLA-001",
    "FIN-004",
    "CAU-001",
    "DQ-001",
}

PROHIBITED_ENGINE_STRINGS = (
    "expected_do_nothing",
    "artifacts/phase-5",
    "artifacts/phase-4",
    "data/golden",
    "openai",
    "anthropic",
    "llm",
)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _digest_release() -> str:
    digest = hashlib.sha256()
    release = ROOT / "data" / "releases" / "v1.0.0"
    for directory in (
        "master",
        "operations",
        "inventory",
        "production",
        "demand",
        "disruptions",
    ):
        for path in sorted((release / directory).glob("*.csv")):
            digest.update(path.relative_to(release).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _check_structure() -> list[str]:
    issues = [f"missing file: {path}" for path in REQUIRED_FILES if not (ROOT / path).exists()]
    issues += [
        f"missing test directory: {path}"
        for path in REQUIRED_TEST_DIRECTORIES
        if not (ROOT / path).is_dir()
    ]
    return issues


def _check_rule_registry() -> list[str]:
    text = (ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml").read_text(
        encoding="utf-8"
    )
    missing = sorted(rule for rule in REQUIRED_RULE_IDS if f"rule_id: {rule}" not in text)
    return [f"rule registry missing: {rule}" for rule in missing]


def _check_no_runtime_expected_reads() -> list[str]:
    issues: list[str] = []
    for path in (ROOT / "src" / "chronosdb" / "impact").rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for token in PROHIBITED_ENGINE_STRINGS:
            if token in text:
                issues.append(f"prohibited runtime token in {path.relative_to(ROOT)}: {token}")
    return issues


def _check_traceability() -> list[str]:
    path = ROOT / "docs" / "impact-engine" / "phase-5-traceability-matrix.csv"
    if not path.exists():
        return ["traceability matrix is missing"]
    rows = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) < 10:
        return ["traceability matrix has fewer than 10 rows"]
    header = rows[0].split(",")
    required = {"phase2_rule_id", "engine_module", "rule_id", "golden_evidence", "status"}
    missing = sorted(required - set(header))
    return [f"traceability matrix missing column: {name}" for name in missing]


def _check_golden_artifact() -> list[str]:
    result = _json(ROOT / "artifacts" / "phase-5" / "golden-impact-result.json")
    expected_hash = canonical_hash(
        {key: value for key, value in result.items() if key != "result_hash"}
    )
    issues = []
    if result.get("result_hash") != expected_hash:
        issues.append("golden result hash is not canonical")
    metrics = result.get("headline_metrics", {})
    if metrics.get("late_quantity") != "400":
        issues.append("golden late quantity is not 400")
    if metrics.get("revenue_at_risk") != {"amount": "1600000.00", "currency": "INR"}:
        issues.append("golden revenue at risk is not 1,600,000 INR")
    if len(result.get("provenance", {}).get("metric_provenance", {})) < 10:
        issues.append("headline metric provenance is incomplete")
    if len(result.get("causal_traces", [])) != 2:
        issues.append("golden causal trace count is not 2")
    return issues


def _check_benchmark_artifact() -> list[str]:
    artifact = _json(ROOT / "artifacts" / "phase-5" / "impact-benchmark-results.json")
    issues = []
    if artifact.get("benchmark_scenario_count") != 60:
        issues.append("benchmark artifact does not cover 60 scenarios")
    if sum(artifact.get("partitions", {}).values()) != 60:
        issues.append("benchmark partition counts do not sum to 60")
    if not artifact.get("golden", {}).get("targets_met"):
        issues.append("golden benchmark targets are not met")
    return issues


def _check_handoff() -> list[str]:
    issues: list[str] = []
    report = _json(ROOT / "artifacts" / "phase-5-handoff" / "determinism-report.json")
    if report.get("status") != "PASS" or not report.get("same_result"):
        issues.append("determinism handoff report is not PASS")
    if report.get("repeated_run_count", 0) < 100:
        issues.append("determinism report covers fewer than 100 runs")
    golden = _json(ROOT / "artifacts" / "phase-5-handoff" / "golden-impact-result.json")
    current = _json(ROOT / "artifacts" / "phase-5" / "golden-impact-result.json")
    if golden.get("result_hash") != current.get("result_hash"):
        issues.append("handoff golden result is stale")
    return issues


def run(*, run_handoff: bool = True) -> dict[str, Any]:
    issues: list[str] = []
    checks: dict[str, str] = {}

    issues.extend(_check_structure())
    checks["structure"] = "PASS" if not issues else "FAIL"

    rule_issues = _check_rule_registry()
    issues.extend(rule_issues)
    checks["rule_registry"] = "PASS" if not rule_issues else "FAIL"

    runtime_issues = _check_no_runtime_expected_reads()
    issues.extend(runtime_issues)
    checks["runtime_isolation"] = "PASS" if not runtime_issues else "FAIL"

    trace_issues = _check_traceability()
    issues.extend(trace_issues)
    checks["traceability"] = "PASS" if not trace_issues else "FAIL"

    intake = impact_intake.run("all")
    if intake["status"] != "PASS":
        issues.extend(f"intake: {issue}" for issue in intake["issues"])
    checks["intake"] = intake["status"]

    before = _digest_release()
    golden = run_phase5_golden.run(ROOT)
    after = _digest_release()
    if before != after:
        issues.append("operational release files changed during calculation")
    checks["operational_immutability"] = "PASS" if before == after else "FAIL"
    checks["golden"] = "PASS"

    benchmark = run_impact_benchmarks.run(ROOT)
    checks["benchmark"] = "PASS" if benchmark["golden"]["targets_met"] else "FAIL"
    if checks["benchmark"] != "PASS":
        issues.append("golden benchmark correctness targets failed")

    comparison = compare(ROOT)
    checks["ground_truth"] = comparison["status"]
    if comparison["status"] != "PASS":
        issues.extend(f"ground truth: {name}" for name in comparison["failed"])

    if run_handoff:
        from scripts import build_phase5_handoff

        build_phase5_handoff.run(ROOT)
        checks["handoff"] = "PASS"
    else:
        checks["handoff"] = "SKIPPED"

    artifact_issues = _check_golden_artifact() + _check_benchmark_artifact()
    issues.extend(artifact_issues)
    checks["artifacts"] = "PASS" if not artifact_issues else "FAIL"

    if run_handoff:
        handoff_issues = _check_handoff()
        issues.extend(handoff_issues)
        checks["determinism"] = "PASS" if not handoff_issues else "FAIL"

    report = {
        "report_version": "1.0.0",
        "phase": 5,
        "engine": "chronosdb-impact-engine-v1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not issues else "FAIL",
        "checks": checks,
        "issues": sorted(set(issues)),
        "golden_result_hash": golden.get("result_hash"),
        "benchmark_result_hash": benchmark.get("result_hash"),
    }
    output_dir = ROOT / "artifacts" / "phase-5"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "validation-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-handoff", action="store_true")
    args = parser.parse_args()
    report = run(run_handoff=not args.skip_handoff)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
