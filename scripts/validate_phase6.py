"""Validate Phase 6 against the real Phase 5-backed counterfactual engine."""

from __future__ import annotations

import json
import sys
import time
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chronosdb.simulation.counterfactual import (  # noqa: E402
    Overlay,
    Phase6Engine,
    ScenarioLedger,
    SimulationValidationError,
    load_golden_overlays,
)


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _records_snapshot(engine: Phase6Engine) -> str:
    return json.dumps(
        {name: [dict(row) for row in rows] for name, rows in engine.state.records.items()},
        sort_keys=True,
        separators=(",", ":"),
    )


def _event_types(result: Any) -> list[str]:
    return sorted({event["event_type"] for event in result.events})


def _adversarial_cases(owner: Phase6Engine) -> list[tuple[str, tuple[Overlay, ...]]]:
    return [
        (
            "negative_transfer_quantity",
            (
                Overlay(
                    "ADV-001",
                    "TRANSFER_INVENTORY",
                    {
                        "component_id": "CMP-MCU-42",
                        "quantity": "-1",
                        "from_warehouse": "WH-CHENNAI",
                        "to_warehouse": "WH-PUNE",
                    },
                ),
            ),
        ),
        (
            "transfer_exceeds_stock",
            (
                Overlay(
                    "ADV-002",
                    "TRANSFER_INVENTORY",
                    {
                        "component_id": "CMP-MCU-42",
                        "quantity": "999999",
                        "from_warehouse": "WH-CHENNAI",
                        "to_warehouse": "WH-PUNE",
                    },
                ),
            ),
        ),
        (
            "transfer_violates_safety_stock",
            (
                Overlay(
                    "ADV-002B",
                    "TRANSFER_INVENTORY",
                    {
                        "component_id": "CMP-MCU-42",
                        "quantity": "581",
                        "from_warehouse": "WH-CHENNAI",
                        "to_warehouse": "WH-PUNE",
                    },
                ),
            ),
        ),
        (
            "unknown_alternate_supplier",
            (
                Overlay(
                    "ADV-003",
                    "ALTERNATE_SUPPLIER",
                    {
                        "supplier_id": "SUP-UNKNOWN-999",
                        "component_id": "CMP-MCU-42",
                        "available_quantity": "10",
                    },
                ),
            ),
        ),
        (
            "expedite_impossible_po",
            (
                Overlay(
                    "ADV-004",
                    "EXPEDITE_PO",
                    {
                        "purchase_order_id": "PO-IMPOSSIBLE-999",
                        "lead_time_reduction_days": 5,
                    },
                ),
            ),
        ),
        (
            "invalid_priority",
            (
                Overlay(
                    "ADV-005",
                    "RESCHEDULE_PRODUCTION",
                    {"production_order_id": "MO-0882", "priority": "URGENT"},
                ),
            ),
        ),
        (
            "duplicate_intervention",
            (
                Overlay(
                    "ADV-006",
                    "TRANSFER_INVENTORY",
                    {
                        "component_id": "CMP-MCU-42",
                        "quantity": "10",
                        "from_warehouse": "WH-CHENNAI",
                        "to_warehouse": "WH-PUNE",
                    },
                ),
                Overlay(
                    "ADV-006",
                    "TRANSFER_INVENTORY",
                    {
                        "component_id": "CMP-MCU-42",
                        "quantity": "10",
                        "from_warehouse": "WH-CHENNAI",
                        "to_warehouse": "WH-PUNE",
                    },
                ),
            ),
        ),
        (
            "conflicting_intervention",
            (
                Overlay(
                    "ADV-007",
                    "EXPEDITE_PO",
                    {"purchase_order_id": "PO-2208", "lead_time_reduction_days": 3},
                ),
                Overlay(
                    "ADV-008",
                    "EXPEDITE_PO",
                    {"purchase_order_id": "PO-2208", "lead_time_reduction_days": 4},
                ),
            ),
        ),
        (
            "broken_overlay",
            (Overlay("ADV-009", "UNKNOWN_ACTION", {}),),
        ),
        (
            "expired_agreement",
            (
                Overlay(
                    "ADV-010",
                    "ALTERNATE_SUPPLIER",
                    {
                        "supplier_id": "SUP-0104",
                        "component_id": "CMP-P4-0002",
                        "available_quantity": "10",
                    },
                ),
            ),
        ),
    ]


def main() -> int:
    issues: list[str] = []
    checks: dict[str, str] = {}
    engine = Phase6Engine(ROOT)
    baseline = engine.baseline()
    phase5_artifact = _read(ROOT / "artifacts" / "phase-5" / "golden-impact-result.json")

    if baseline.result_hash != phase5_artifact["result_hash"]:
        issues.append("live Phase 5 baseline hash does not match frozen Phase 5 artifact")
    if baseline.input_state_hash != phase5_artifact["input_state_hash"]:
        issues.append("live baseline state hash does not match Phase 5 artifact")
    if baseline.headline_metrics.get("revenue_at_risk") != phase5_artifact["headline_metrics"][
        "revenue_at_risk"
    ]:
        issues.append("live baseline revenue at risk does not match Phase 5 artifact")
    checks["phase5_handoff"] = "PASS" if not issues else "FAIL"

    golden_overlays = load_golden_overlays(ROOT / "data" / "golden" / "phase6-overlays.json")
    expected = _read(ROOT / "data" / "golden" / "phase6-expected.json")
    before = _records_snapshot(engine)
    ledger_path = ROOT / "artifacts" / "phase-6" / "simulation-ledger.jsonl"
    ledger_path.unlink(missing_ok=True)
    ledger = ScenarioLedger(ledger_path)
    golden_results: dict[str, Any] = {}
    for name, overlays in golden_overlays.items():
        result = engine.run(overlays, ledger=ledger)
        payload = result.to_dict()
        golden_results[name] = payload
        target = expected[name]
        if Decimal(result.delta["revenue_protected"]) != Decimal(
            target["revenue_protected"]
        ):
            issues.append(f"{name}: revenue protected mismatch")
        if result.delta["breaches_avoided"] != target["breaches_avoided"]:
            issues.append(f"{name}: breaches avoided mismatch")
        if result.delta["delay_reduction_hours"] != target["delay_reduction_hours"]:
            issues.append(f"{name}: delay reduction mismatch")
        if Decimal(result.intervention_cost) != Decimal(target["intervention_cost"]):
            issues.append(f"{name}: intervention cost mismatch")
        if result.headline_metrics["revenue_at_risk"]["amount"] != target[
            "scenario_revenue_risk"
        ]:
            issues.append(f"{name}: scenario revenue mismatch")
        if _event_types(result) != sorted(target["event_types"]):
            issues.append(f"{name}: generated event types mismatch")
        if result.baseline_state_hash != engine.state.identity.state_hash:
            issues.append(f"{name}: baseline state hash changed")
        if result.status not in {"COMPLETED", "PARTIALLY_COMPLETED"}:
            issues.append(f"{name}: simulation did not complete")
        if result.result_hash != engine.run(overlays).result_hash:
            issues.append(f"{name}: repeated result hash is not stable")

    if _records_snapshot(engine) != before:
        issues.append("baseline operational records were mutated")
    ledger_records = [
        json.loads(line)
        for line in (ROOT / "artifacts" / "phase-6" / "simulation-ledger.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    if len(ledger_records) != len(golden_overlays):
        issues.append("simulation ledger does not contain every golden run")
    if any("result_hash" not in record for record in ledger_records):
        issues.append("simulation ledger record is missing result provenance")
    checks["golden_interventions"] = "PASS" if not issues else "FAIL"
    checks["persistence"] = "PASS" if len(ledger_records) == len(golden_overlays) else "FAIL"

    adversarial = []
    for name, overlays in _adversarial_cases(engine):
        try:
            engine.run(overlays)
            adversarial.append({"case": name, "status": "FAIL", "detail": "no error"})
            issues.append(f"adversarial case did not reject: {name}")
        except SimulationValidationError as exc:
            adversarial.append({"case": name, "status": "PASS", "detail": str(exc)})
        except Exception as exc:  # noqa: BLE001
            adversarial.append(
                {"case": name, "status": "FAIL", "detail": f"untyped {type(exc).__name__}: {exc}"}
            )
            issues.append(f"adversarial case raised untyped error: {name}")
    if _records_snapshot(engine) != before:
        issues.append("adversarial validation mutated baseline records")
    checks["adversarial"] = (
        "PASS" if all(item["status"] == "PASS" for item in adversarial) else "FAIL"
    )

    transfer = golden_overlays["transfer"]
    determinism_hashes: list[str] = []
    for _ in range(100):
        determinism_hashes.append(engine.run(transfer).result_hash)
    if len(set(determinism_hashes)) != 1:
        issues.append("100-run transfer determinism produced multiple result hashes")

    benchmark_hashes: dict[str, set[str]] = {}
    for quantity in range(10, 210, 10):
        variant = (
            Overlay(
                f"BENCH-TRANSFER-{quantity:03d}",
                "TRANSFER_INVENTORY",
                {
                    "component_id": "CMP-MCU-42",
                    "quantity": str(quantity),
                    "from_warehouse": "WH-CHENNAI",
                    "to_warehouse": "WH-PUNE",
                },
            ),
        )
        benchmark_hashes[str(quantity)] = {
            engine.run(variant).result_hash for _ in range(10)
        }
    if any(len(hashes) != 1 for hashes in benchmark_hashes.values()):
        issues.append("20-scenario benchmark replay was not stable")
    if len({next(iter(hashes)) for hashes in benchmark_hashes.values()}) != 20:
        issues.append("benchmark scenarios did not produce 20 distinct outputs")
    checks["determinism"] = (
        "PASS"
        if len(set(determinism_hashes)) == 1
        and all(len(hashes) == 1 for hashes in benchmark_hashes.values())
        else "FAIL"
    )

    timings: list[float] = []
    for _ in range(5):
        started = time.perf_counter()
        engine.run(golden_overlays["hybrid"])
        timings.append((time.perf_counter() - started) * 1000)
    p95 = sorted(timings)[-1]
    if p95 > 2500:
        issues.append(f"hybrid P95 exceeds target: {p95:.1f} ms")
    checks["performance"] = "PASS" if p95 <= 2500 else "FAIL"

    generated_at = datetime.now(UTC).isoformat()
    report = {
        "phase": 6,
        "status": "PASS" if not issues else "FAIL",
        "generated_at": generated_at,
        "engine": "chronosdb-counterfactual-engine-v1.0.0",
        "baseline_result_hash": baseline.result_hash,
        "baseline_state_hash": baseline.input_state_hash,
        "checks": checks,
        "issues": issues,
    }
    _write(ROOT / "artifacts" / "phase-6" / "validation-report.json", report)
    _write(ROOT / "artifacts" / "phase-6" / "golden-results.json", golden_results)
    _write(
        ROOT / "artifacts" / "phase-6" / "determinism-report.json",
        {
            "golden_transfer": {
                "runs": 100,
                "unique_result_hashes": len(set(determinism_hashes)),
                "result_hash": determinism_hashes[0],
                "stable": len(set(determinism_hashes)) == 1,
            },
            "benchmark": {
                "scenarios": len(benchmark_hashes),
                "reruns_per_scenario": 10,
                "total_outputs": 200,
                "distinct_outputs": len(
                    {next(iter(hashes)) for hashes in benchmark_hashes.values()}
                ),
                "stable": all(len(hashes) == 1 for hashes in benchmark_hashes.values()),
            },
        },
    )
    _write(
        ROOT / "artifacts" / "phase-6" / "performance-report.json",
        {
            "runs": len(timings),
            "p95_ms": round(p95, 3),
            "target_ms": 2500,
            "samples_ms": [round(value, 3) for value in timings],
            "passes": p95 <= 2500,
        },
    )
    _write(
        ROOT / "artifacts" / "phase-6" / "adversarial-report.json",
        {"cases": adversarial, "all_passed": checks["adversarial"] == "PASS"},
    )
    _write(
        ROOT / "artifacts" / "phase-6" / "phase-7-handoff.json",
        {
            "do_nothing": {
                "revenue_risk": baseline.headline_metrics["revenue_at_risk"]["amount"],
                "breaches": baseline.headline_metrics["sla_breached_customer_order_count"],
                "delay_hours": baseline.headline_metrics["maximum_delay_hours"],
                "result_hash": baseline.result_hash,
            },
            "candidates": {
                name: {
                    "revenue_risk": result["headline_metrics"]["revenue_at_risk"]["amount"],
                    "breaches": result["headline_metrics"][
                        "sla_breached_customer_order_count"
                    ],
                    "delay_hours": result["headline_metrics"]["maximum_delay_hours"],
                    "intervention_cost": result["intervention_cost"],
                    "delta": result["delta"],
                    "result_hash": result["result_hash"],
                }
                for name, result in golden_results.items()
            },
        },
    )
    print(json.dumps(report, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
