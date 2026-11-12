"""Phase 4O frozen benchmark scenario generation."""

from __future__ import annotations

from typing import Any

from .release_export import write_release_csv, write_release_json
from .release_profile import ReleaseProfile, release_root
from .scenarios import SCENARIO_CATEGORIES

TEST_INDICES = {1, 2, 19, 27, 33, 37, 41, 45, 49, 52, 53, 54, 55, 56, 57, 58, 59, 60}
GOLDEN_INDICES = {3, 4, 5}
ADVERSARIAL_INDICES = {6, 7, 8}


def _partition(index: int) -> str:
    if index in TEST_INDICES:
        return "test"
    if index in GOLDEN_INDICES:
        return "golden"
    if index in ADVERSARIAL_INDICES:
        return "adversarial-only"
    remaining = [
        value
        for value in range(1, 61)
        if value not in TEST_INDICES | GOLDEN_INDICES | ADVERSARIAL_INDICES
    ]
    if remaining.index(index) < 24:
        return "development"
    if remaining.index(index) < 36:
        return "validation"
    raise ValueError(f"benchmark partition overflow: {index}")


def _difficulty(index: int) -> str:
    if index <= 15:
        return "L1_DIRECT"
    if index <= 35:
        return "L2_CONNECTED"
    if index <= 52:
        return "L3_CONSTRAINED"
    return "L4_ADVERSARIAL"


def _expected(category: str) -> tuple[str, str]:
    if category == "NO_OPERATIONAL_IMPACT":
        return "MONITOR_NO_INTERVENTION", "NO_BREACH"
    if category == "NO_FEASIBLE_INTERVENTION":
        return "NO_FEASIBLE_INTERVENTION", "NO_VALID_CANDIDATE"
    if category == "INSUFFICIENT_CRITICAL_DATA":
        return "INSUFFICIENT_DATA", "DATA_REQUIRED"
    if category == "INVENTORY_TRANSFER_CONSTRAINT":
        return "TRANSFER", "TRANSFER_CONSTRAINED"
    if category == "ALTERNATE_SUPPLIER_CONSTRAINT":
        return "ALTERNATE_SUPPLY", "ALTERNATE_CONSTRAINED"
    if category == "BUDGET_CONSTRAINED_RECOVERY":
        return "TRANSFER", "BUDGET_COMPLIANT"
    if category == "TIE_OR_PARETO_EQUIVALENT":
        return "PARETO_SET", "MULTIPLE_VALID_OPTIMA"
    if category == "PURCHASE_ORDER_DISRUPTION":
        return "EXPEDITE", "PO_SCOPED"
    if category == "PARTIAL_SUPPLIER_OUTAGE":
        return "RESCHEDULE", "PARTIAL_CAPACITY_AVAILABLE"
    if category == "SELECTED_COMPONENT_OUTAGE":
        return "EXPEDITE", "COMPONENT_PATH_AVAILABLE"
    return "HYBRID", "MINIMIZE_SLA_BREACHES"


def build_benchmarks(profile: ReleaseProfile) -> dict[str, Any]:
    """Create the exact 60-case catalogue and immutable expected outcomes."""
    scenarios: list[dict[str, Any]] = []
    expected: list[dict[str, Any]] = []
    difficulty_labels: list[dict[str, Any]] = []
    number = 0
    for category, count in SCENARIO_CATEGORIES:
        for _ in range(count):
            number += 1
            scenario_id = f"SCN-BENCH-{number:04d}"
            partition = _partition(number)
            difficulty = _difficulty(number)
            recommendation, reason = _expected(category)
            scenario = {
                "scenario_id": scenario_id,
                "category": category,
                "partition": partition,
                "difficulty": difficulty,
                "as_of_time": "2026-11-11T02:30:00Z",
                "simulation_horizon_days": 30,
                "objective_mode": "MINIMIZE_SLA_BREACHES",
                "expected_outcome_file": f"expected/{scenario_id}.json",
                "test_specific_branch": "false",
                "reference_supplier_id": "SUP-0104",
                "reference_component_id": "CMP-MCU-42",
                "reference_purchase_order_id": "PO-2208",
                "reference_customer_order_id": (
                    "CO-0701",
                    "CO-0704",
                    "CO-0711",
                )[number % 3],
                "evidence_query_id": (
                    "RET-GOLD-NOTICE"
                    if number % 2
                    else "RET-GOLD-TRANSFER"
                ),
                "requires_temporal_reconstruction": number in {
                    19,
                    27,
                    33,
                    37,
                    41,
                    45,
                    49,
                    52,
                    55,
                },
                "has_misleading_evidence": number in {1, 2, 19, 27, 33, 37, 41},
                "partial_fulfillment": number in {19, 27, 33, 37, 41, 45},
            }
            outcome = {
                "scenario_id": scenario_id,
                "feasibility_status": (
                    "INFEASIBLE"
                    if recommendation in {"NO_FEASIBLE_INTERVENTION", "INSUFFICIENT_DATA"}
                    else "FEASIBLE"
                ),
                "recommended_intervention": recommendation,
                "reason_code": reason,
                "sla_breach_count": 0 if recommendation == "MONITOR_NO_INTERVENTION" else None,
                "causal_trace_id": f"TRACE-{scenario_id}",
                "affected_customer_orders": [scenario["reference_customer_order_id"]],
                "evidence_references": [scenario["evidence_query_id"]],
                "requires_temporal_reconstruction": scenario[
                    "requires_temporal_reconstruction"
                ],
                "has_misleading_evidence": scenario["has_misleading_evidence"],
                "partial_fulfillment": scenario["partial_fulfillment"],
            }
            scenarios.append(scenario)
            expected.append(outcome)
            difficulty_labels.append(
                {
                    "scenario_id": scenario_id,
                    "difficulty": difficulty,
                    "partition": partition,
                }
            )
    catalogue = [
        {
            "scenario_id": row["scenario_id"],
            "category": row["category"],
            "partition": row["partition"],
            "difficulty": row["difficulty"],
            "expected_outcome_file": row["expected_outcome_file"],
        }
        for row in scenarios
    ]
    partition_manifest = {
        "version": profile.version,
        "exclusive_partitions": {
            name: [row["scenario_id"] for row in scenarios if row["partition"] == name]
            for name in ("development", "validation", "test", "golden", "adversarial-only")
        },
        "relationships": {
            "golden": "exclusive benchmark partition",
            "adversarial-only": "exclusive benchmark partition",
            "no_partition_overlap": True,
        },
    }
    release_notes = (
        "# Phase 4O benchmark release\n\n"
        "This 60-scenario catalogue is frozen for release v1.0.0. "
        "Expected outcomes are authoritative dataset ground truth; implementation "
        "changes must not rewrite them. A discovered dataset defect requires a "
        "version increase.\n"
    )
    output = release_root(profile) / "benchmarks"
    for row in scenarios:
        write_release_json(output / "scenarios" / f"{row['scenario_id']}.json", row)
    for row in expected:
        write_release_json(output / "expected" / f"{row['scenario_id']}.json", row)
    write_release_json(output / "partition_manifest.json", partition_manifest)
    write_release_csv(output / "scenario_catalogue.csv", catalogue)
    write_release_csv(output / "difficulty_labels.csv", difficulty_labels)
    (output / "benchmark_release_notes.md").write_text(
        release_notes,
        encoding="utf-8",
    )
    return {
        "scenarios": scenarios,
        "expected": expected,
        "difficulty_labels": difficulty_labels,
        "partition_manifest": partition_manifest,
    }
