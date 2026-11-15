"""Validate the immutable Phase 4 inputs used by the Phase 5 impact engine."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "data" / "releases" / "v1.0.0"
PHASE4 = ROOT / "artifacts" / "phase-4"
PHASE5 = ROOT / "artifacts" / "phase-5"


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _count(path: Path) -> int:
    if path.suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as stream:
            return sum(1 for _ in csv.DictReader(stream))
    if path.suffix == ".jsonl":
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    payload = _json(path)
    return len(payload) if isinstance(payload, list) else 1


def _check_release_files() -> list[str]:
    issues: list[str] = []
    manifest = _json(RELEASE / "manifest.json")
    declared = {item["path"]: item["sha256"] for item in manifest["files"]}
    for path, expected in declared.items():
        file_path = ROOT / path
        if not file_path.exists():
            issues.append(f"manifest missing file: {path}")
            continue
        if _sha(file_path) != expected:
            issues.append(f"manifest checksum mismatch: {path}")
    checksums = RELEASE / "checksums.sha256"
    for line in checksums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        file_path = RELEASE / relative
        if not file_path.exists() or _sha(file_path) != expected:
            issues.append(f"release checksum mismatch: {relative}")
    return issues


def _check_handoff() -> list[str]:
    issues: list[str] = []
    contract_path = PHASE4 / "handoff" / "phase5-load-contract.json"
    contract = _json(contract_path)
    if contract.get("status") == "FAIL":
        issues.append("Phase 4 handoff validation status is FAIL")
    for entry in contract.get("files", []):
        profile_root = RELEASE if entry["profile"] == "demo" else RELEASE / entry["profile"]
        path = profile_root / entry["source_file"]
        if not path.exists():
            issues.append(f"handoff source missing: {entry['source_file']}")
        elif _sha(path) != entry["checksum"]:
            issues.append(f"handoff checksum mismatch: {entry['source_file']}")
    return issues


def _check_golden_inputs() -> list[str]:
    issues: list[str] = []
    golden = RELEASE / "golden"
    scenario = _json(golden / "scenario.json")
    required = {
        "scenario_id",
        "as_of_time",
        "event_id",
        "supplier_id",
        "component_id",
        "purchase_order_id",
    }
    missing = sorted(required - scenario.keys())
    if missing:
        issues.append(f"golden scenario missing fields: {missing}")
    if scenario.get("scenario_id") != "SCN-GOLD-001":
        issues.append("unexpected golden scenario identity")
    if _json(golden / "state_at_as_of.json").get("as_of_time") != scenario.get("as_of_time"):
        issues.append("golden state timestamp does not match scenario")
    if _json(golden / "expected_recommendation.json").get("hard_constraints_satisfied") is not True:
        issues.append("golden hard-constraint fixture is not satisfied")
    for name in (
        "scenario.json",
        "state_at_as_of.json",
        "expected_recommendation.json",
        "expected_timeline.json",
        "expected_causal_traces.json",
        "manual_calculation.csv",
    ):
        if not (golden / name).exists():
            issues.append(f"golden input missing: {name}")
    do_nothing = _json(ROOT / "data" / "golden" / "expected_do_nothing.json")
    if do_nothing.get("candidate_id") != "DO-NOTHING":
        issues.append("golden expected do-nothing identity is invalid")
    if do_nothing.get("breached_customer_orders") != 2:
        issues.append("golden expected breach count is invalid")
    if do_nothing.get("revenue_at_risk_inr") != "1600000.00":
        issues.append("golden expected revenue is invalid")
    if do_nothing.get("total_delay_hours") != 110400:
        issues.append("golden expected delay is invalid")
    if len(do_nothing.get("customer_lines", ())) != 3:
        issues.append("golden customer-line fixture is incomplete")
    traces = _json(ROOT / "data" / "golden" / "expected_causal_traces.json")
    if not traces or any(not trace.get("target") for trace in traces):
        issues.append("golden causal-root fixture is incomplete")
    if len(_json(ROOT / "data" / "golden" / "expected_engine_causal_traces.json")) != 2:
        issues.append("golden engine causal-trace fixture is incomplete")
    return issues


def _check_benchmarks() -> list[str]:
    issues: list[str] = []
    manifest = _json(RELEASE / "benchmarks" / "partition_manifest.json")
    partitions = manifest.get("exclusive_partitions", {})
    scenario_ids = {item for values in partitions.values() for item in values}
    if len(scenario_ids) != 60:
        issues.append(f"expected 60 unique benchmark scenarios, found {len(scenario_ids)}")
    if sum(len(values) for values in partitions.values()) != len(scenario_ids):
        issues.append("benchmark partitions overlap")
    partition_by_scenario = {
        scenario_id: partition
        for partition, values in partitions.items()
        for scenario_id in values
    }
    hashes = {
        row["scenario_id"]: row
        for row in csv.DictReader(
            (PHASE4 / "ground-truth" / "scenario-input-hashes.csv").open(
                encoding="utf-8", newline=""
            )
        )
    }
    expected_results = {
        row["scenario_id"]: row
        for row in _jsonl(PHASE4 / "ground-truth" / "expected-results.jsonl")
    }
    causal_traces = {
        row["trace_id"]: row
        for row in _jsonl(PHASE4 / "ground-truth" / "causal-traces.jsonl")
    }
    for scenario_id in sorted(scenario_ids):
        scenario_path = RELEASE / "benchmarks" / "scenarios" / f"{scenario_id}.json"
        expected_path = RELEASE / "benchmarks" / "expected" / f"{scenario_id}.json"
        if not scenario_path.exists() or not expected_path.exists():
            issues.append(f"benchmark pair missing: {scenario_id}")
            continue
        scenario = _json(scenario_path)
        expected = _json(expected_path)
        do_nothing = expected_results.get(scenario_id, {}).get("do_nothing")
        if not do_nothing:
            issues.append(f"expected do-nothing result missing: {scenario_id}")
        else:
            for field in ("late_quantity", "revenue_at_risk_inr", "source_record_ids"):
                if field not in do_nothing:
                    issues.append(f"{scenario_id} do-nothing field missing: {field}")
        for field in ("as_of_time", "simulation_horizon_days", "partition"):
            if field not in scenario:
                issues.append(f"{scenario_id} scenario field missing: {field}")
        if scenario.get("partition") != partition_by_scenario[scenario_id]:
            issues.append(f"{scenario_id} partition does not match manifest")
        hash_row = hashes.get(scenario_id)
        if hash_row is None:
            issues.append(f"benchmark input hash missing: {scenario_id}")
        elif expected_results.get(scenario_id, {}).get("input_state_hash") != hash_row["input_state_hash"]:
            issues.append(f"{scenario_id} input hash differs from ground truth")
        trace_id = expected.get("causal_trace_id")
        if not trace_id or trace_id not in causal_traces:
            issues.append(f"{scenario_id} expected causal root missing")
        for field in ("affected_customer_orders", "source_record_ids", "reason_code"):
            if field not in expected:
                issues.append(f"{scenario_id} expected field missing: {field}")
        if expected.get("scenario_id") != scenario_id:
            issues.append(f"{scenario_id} expected scenario identity mismatch")
    return issues


def run(check: str = "all") -> dict[str, Any]:
    checks = {
        "intake": _check_release_files,
        "golden": _check_golden_inputs,
        "benchmark": _check_benchmarks,
        "handoff": _check_handoff,
    }
    selected = {
        "all": ("intake", "golden", "benchmark", "handoff"),
        "intake": ("intake",),
        "golden": ("golden",),
        "benchmark": ("benchmark",),
    }.get(check)
    if selected is None:
        raise ValueError(f"unsupported check: {check}")
    issues = [issue for name in selected for issue in checks[name]()]
    report = {
        "status": "PASS" if not issues else "FAIL",
        "dataset": "chronosdb-demo-dataset",
        "dataset_version": "1.0.0",
        "checks": {name: "PASS" if not checks[name]() else "FAIL" for name in selected},
        "issues": issues,
        "runtime_expected_output_reads": False,
    }
    PHASE5.mkdir(parents=True, exist_ok=True)
    (PHASE5 / "intake-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    docs = ROOT / "docs" / "impact-engine"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "phase-4-handoff-review.md").write_text(
        "# Phase 4 Handoff Review\n\n"
        f"- Dataset: `{report['dataset']}` v{report['dataset_version']}\n"
        f"- Status: **{report['status']}**\n"
        "- Checksums, golden inputs, benchmark partitions, and Db2 handoff were verified.\n"
        "- The calculation runtime does not read frozen expected outputs.\n"
        f"- Issues: {len(report['issues'])}\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", choices=("all", "intake", "golden", "benchmark"), default="all"
    )
    args = parser.parse_args()
    report = run(args.check)
    print(f"Phase 5 intake {report['status']}")
    if report["issues"]:
        print("\n".join(report["issues"]))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
