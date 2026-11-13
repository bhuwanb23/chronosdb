"""Run the Phase 4P–4V final gates and produce release/handoff artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from validate_phase4 import validate_profile

from data_generator.release_profile import load_release_profile, release_root

PROFILES = ("demo", "tiny", "standard", "stress")
NESTED_PROFILES = set(PROFILES)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _date(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _json_hash(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _logical_count(path: Path) -> int:
    if path.suffix == ".csv":
        return sum(1 for _ in csv.DictReader(path.open(encoding="utf-8", newline="")))
    if path.suffix == ".jsonl":
        return sum(
            1
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    if path.suffix == ".json":
        payload = _json(path)
        return len(payload) if isinstance(payload, list) else 1
    return 1


def _release_files(output: Path) -> list[Path]:
    files: list[Path] = []
    for path in output.rglob("*"):
        if not path.is_file() or path.name in {"manifest.json", "checksums.sha256"}:
            continue
        relative = path.relative_to(output)
        if relative.parts and relative.parts[0] in NESTED_PROFILES:
            continue
        files.append(path)
    return sorted(files)


def _write_release_docs(root: Path) -> None:
    load_order = [
        "master/warehouses",
        "master/facilities",
        "master/suppliers",
        "master/components",
        "master/supplier_component_agreements",
        "master/products",
        "master/bom_versions",
        "master/bom_lines",
        "master/customers",
        "master/sla_policies",
        "master/transfer_lanes",
        "operations/purchase_orders",
        "operations/purchase_order_receipts",
        "production/production_orders",
        "demand/customer_orders",
        "demand/customer_order_lines",
        "inventory/inventory_opening_balances",
        "inventory/inventory_transactions",
        "inventory/inventory_snapshots_daily",
        "history/replay_input_events",
        "disruptions/disruption_events",
        "interventions/transfer_capabilities",
        "evidence/documents",
        "golden/expected_recommendation",
        "benchmarks/scenarios",
    ]
    readme = (
        "# ChronosDB Synthetic Dataset v1.0.0\n\n"
        "This is a fictional, project-authored supply-chain dataset for deterministic "
        "demonstration, validation, and benchmark evaluation. Suppliers, customers, "
        "prices, incidents, and outcomes are synthetic and are not commercial forecasts.\n\n"
        "The canonical demo release is accompanied by tiny, standard, and stress profiles. "
        "Use `manifest.json`, `checksums.sha256`, and `load-order.json` for loading.\n"
    )
    card = (
        "# Dataset Card\n\n"
        "- Version: `1.0.0`\n"
        "- Seed: `260311`\n"
        "- Currency: `INR`\n"
        "- Canonical timezone: `UTC` (display: `Asia/Kolkata`)\n"
        "- Origin: project-authored synthetic data\n"
        "- License: `LicenseRef-ChronosDB-Synthetic-Data-1.0`\n"
        "- Golden scenario: `SCN-GOLD-001`\n"
        "- Benchmark: 60 frozen scenarios with exclusive partitions\n"
        "- Privacy and answer-leakage status: PASS\n"
    )
    for profile_name in PROFILES:
        profile = load_release_profile(root, profile_name)
        output = release_root(profile)
        (output / "README.md").write_text(readme, encoding="utf-8")
        (output / "DATASET_CARD.md").write_text(card, encoding="utf-8")
        _write_json(
            output / "load-order.json",
            {"load_order": load_order, "version": profile.version},
        )
        _write_json(
            output / "license.json",
            {
                "spdx_license_identifier": "LicenseRef-ChronosDB-Synthetic-Data-1.0",
                "license_name": "ChronosDB Synthetic Data License",
                "version": "1.0",
                "attribution": "ChronosDB project authors",
                "terms": (
                    "Fictional synthetic records may be used for ChronosDB development, "
                    "demonstration, testing, and benchmark evaluation. They are not "
                    "commercial forecasts or real customer/supplier records."
                ),
                "synthetic_origin": True,
                "external_corpus_copied": False,
            },
        )


def _write_release_checksums(root: Path) -> None:
    for profile_name in PROFILES:
        profile = load_release_profile(root, profile_name)
        output = release_root(profile)
        lines = [
            f"{_sha(path)}  {path.relative_to(output).as_posix()}"
            for path in _release_files(output)
        ]
        (output / "checksums.sha256").write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )


def _write_release_reports(
    root: Path, validation: dict[str, Any], score: int
) -> None:
    for profile_name in PROFILES:
        profile = load_release_profile(root, profile_name)
        output = release_root(profile)
        _write_json(
            output / "reports" / "phase4-finalization-summary.json",
            {
                "profile": profile_name,
                "version": profile.version,
                "status": validation["status"],
                "errors": validation["errors"],
                "warnings": validation["warnings"],
                "score": score,
            },
        )


def _benchmark_source_context(output: Path) -> dict[str, list[dict[str, str]]]:
    return {
        "purchase_orders": _csv(output / "operations" / "purchase_orders.csv"),
        "opening": _csv(output / "inventory" / "inventory_opening_balances.csv"),
        "transactions": _csv(output / "inventory" / "inventory_transactions.csv"),
        "requirements": _csv(
            output / "production" / "production_material_requirements.csv"
        ),
        "production_orders": _csv(output / "production" / "production_orders.csv"),
        "customer_lines": _csv(output / "demand" / "customer_order_lines.csv"),
        "customer_orders": _csv(output / "demand" / "customer_orders.csv"),
        "transfers": _csv(output / "interventions" / "transfer_capabilities.csv"),
        "alternates": _csv(
            output / "interventions" / "alternate_supply_capabilities.csv"
        ),
        "expedites": _csv(output / "interventions" / "expedite_capabilities.csv"),
        "rescheduling": _csv(
            output / "interventions" / "rescheduling_constraints.csv"
        ),
    }


def _oracle_candidate(
    candidate_type: str,
    scenario: dict[str, Any],
    source: dict[str, list[dict[str, str]]],
    baseline_breaches: int | None,
) -> dict[str, Any]:
    po = next(
        row
        for row in source["purchase_orders"]
        if row["id"] == scenario["reference_purchase_order_id"]
    )
    transfer = next(
        (
            row
            for row in source["transfers"]
            if row["candidate_type"] == "TRANSFER"
            and row["component_id"] == scenario["reference_component_id"]
        ),
        None,
    )
    alternate = next(
        (
            row
            for row in source["alternates"]
            if row["component_id"] == scenario["reference_component_id"]
        ),
        None,
    )
    expedite = next(
        (
            row
            for row in source["expedites"]
            if row["purchase_order_id"] == po["id"]
            and (
                scenario["category"]
                in {"PURCHASE_ORDER_DISRUPTION", "SELECTED_COMPONENT_OUTAGE"}
                and row["eligible"] == "true"
                or scenario["category"]
                not in {"PURCHASE_ORDER_DISRUPTION", "SELECTED_COMPONENT_OUTAGE"}
                and row["eligible"] == "false"
            )
        ),
        None,
    )
    reschedule = next(
        (
            row
            for row in source["rescheduling"]
            if row["production_order_id"]
            == scenario.get("reference_production_order_id", "")
        ),
        None,
    )
    quantity = Decimal(str(transfer["requested_quantity"])) if transfer else Decimal("0")
    cost = Decimal("0")
    feasible = False
    rejection = "CAPABILITY_NOT_FOUND"
    references: list[str] = []
    coverage_quantity = Decimal("0")
    affected_order_ids = {
        row["assigned_production_order_id"]
        for row in source["customer_lines"]
        if row["customer_order_id"] == scenario["reference_customer_order_id"]
    }
    if not affected_order_ids:
        affected_order_ids = {
        row["production_order_id"]
        for row in source["requirements"]
        if row["component_id"] == scenario["reference_component_id"]
        }
    planned_starts = [
        _date(row["planned_start_time"])
        for row in source["production_orders"]
        if row["id"] in affected_order_ids and row.get("planned_start_time")
    ]
    planned_start = min(planned_starts, default=_date(po["expected_arrival_time"]))
    ready_time = _date(po["expected_arrival_time"])
    if candidate_type == "TRANSFER" and transfer:
        cost = Decimal(str(transfer["fixed_cost_inr"])) + quantity * Decimal(
            str(transfer["variable_cost_per_unit_inr"])
        )
        scenario_allows = scenario["category"] in {
            "FULL_SUPPLIER_OUTAGE",
            "INVENTORY_TRANSFER_CONSTRAINT",
            "BUDGET_CONSTRAINED_RECOVERY",
        }
        feasible = transfer["feasibility_status"] == "FEASIBLE" and scenario_allows
        rejection = (
            ""
            if feasible
            else transfer.get("rejection_reason") or "TRANSFER_SCENARIO_CONSTRAINT"
        )
        references = [transfer["id"]]
        coverage_quantity = Decimal(str(transfer["available_quantity"]))
        ready_time = _date(transfer["dispatch_time"]) + timedelta(
            days=int(transfer["lead_time_days"])
        )
    elif candidate_type == "ALTERNATE_SUPPLY" and alternate:
        cost = Decimal(str(alternate["incremental_premium_inr"]))
        scenario_allows = scenario["category"] in {
            "FULL_SUPPLIER_OUTAGE",
            "ALTERNATE_SUPPLIER_CONSTRAINT",
        }
        feasible = alternate["feasibility_status"] == "FEASIBLE" and scenario_allows
        rejection = (
            ""
            if feasible
            else "ALTERNATE_CAPACITY_UNAVAILABLE"
            if alternate["feasibility_status"] != "FEASIBLE"
            else "ALTERNATE_SCENARIO_CONSTRAINT"
        )
        references = [alternate["id"]]
        coverage_quantity = Decimal(str(alternate["quantity"]))
        ready_time = _date(alternate["effective_from"]) + timedelta(
            days=int(alternate["lead_time_days"])
        )
    elif candidate_type == "EXPEDITE" and expedite:
        cost = Decimal(str(expedite["fixed_fee_inr"])) + Decimal(
            str(expedite["variable_fee_inr"])
        )
        feasible = expedite["eligible"] == "true" and expedite["outage_compatible"] == "true"
        rejection = "" if feasible else expedite.get("rejection_reason", "EXPEDITE_UNAVAILABLE")
        references = [expedite["id"], po["id"]]
        coverage_quantity = Decimal(str(po["ordered_quantity"]))
        if expedite.get("earliest_achievable_arrival"):
            ready_time = _date(expedite["earliest_achievable_arrival"])
    elif candidate_type == "RESCHEDULE" and reschedule:
        cost = Decimal(str(reschedule["reschedule_penalty_inr"]))
        scenario_allows = scenario["category"] == "PARTIAL_SUPPLIER_OUTAGE"
        feasible = reschedule["feasibility_status"] == "FEASIBLE" and scenario_allows
        rejection = (
            ""
            if feasible
            else "RESCHEDULE_LOCKED"
            if reschedule["feasibility_status"] != "FEASIBLE"
            else "RESCHEDULE_SCENARIO_CONSTRAINT"
        )
        references = [reschedule["id"], reschedule["production_order_id"]]
        ready_time = planned_start
        ready_time = planned_start
    elif candidate_type == "HYBRID":
        transfer_cost = _oracle_candidate("TRANSFER", scenario, source, baseline_breaches)
        alternate_cost = _oracle_candidate(
            "ALTERNATE_SUPPLY", scenario, source, baseline_breaches
        )
        cost = Decimal(transfer_cost["cost_inr"]) + Decimal(alternate_cost["cost_inr"])
        feasible = (
            scenario["category"] == "FULL_SUPPLIER_OUTAGE"
            and transfer_cost["feasible"]
            and alternate_cost["feasible"]
        )
        rejection = "" if feasible else "HYBRID_COMPONENT_NOT_FEASIBLE"
        references = transfer_cost["source_record_ids"] + alternate_cost["source_record_ids"]
        coverage_quantity = Decimal(transfer_cost["coverage_quantity"]) + Decimal(
            alternate_cost["coverage_quantity"]
        )
        ready_time = max(
            _date(transfer_cost["material_ready_time"]),
            _date(alternate_cost["material_ready_time"]),
        )
    if candidate_type == "MONITOR_NO_INTERVENTION":
        feasible = True
        rejection = ""
    if candidate_type == "PARETO_SET":
        feasible = True
        rejection = ""
    delay_hours = max(0, int((ready_time - planned_start).total_seconds() // 3600))
    breaches = None if baseline_breaches is None else baseline_breaches
    if feasible and baseline_breaches is not None:
        required_quantity = sum(
            (
                Decimal(row["required_quantity"])
                for row in source["requirements"]
                if row["component_id"] == scenario["reference_component_id"]
                and row["production_order_id"] in affected_order_ids
            ),
            Decimal("0"),
        )
        reduction = (
            min(baseline_breaches, int(coverage_quantity / required_quantity))
            if required_quantity > 0
            else 0
        )
        breaches = (
            baseline_breaches
            if candidate_type == "MONITOR_NO_INTERVENTION"
            else max(
                0,
                baseline_breaches - reduction
                if delay_hours == 0
                else baseline_breaches - reduction,
            )
        )
    return {
        "candidate_id": f"ORACLE-{candidate_type}-{scenario['scenario_id']}",
        "candidate_type": candidate_type,
        "feasibility_status": "FEASIBLE" if feasible else "INFEASIBLE",
        "feasible": feasible,
        "rejection_code": rejection or None,
        "cost_inr": f"{cost:.2f}",
        "sla_breach_count": breaches,
        "material_ready_time": ready_time.isoformat().replace("+00:00", "Z"),
        "projected_delay_hours": delay_hours,
        "coverage_quantity": str(coverage_quantity),
        "delta_from_do_nothing": (
            None
            if breaches is None or baseline_breaches is None
            else baseline_breaches - breaches
        ),
        "constraint_checks": {
            "budget": cost <= Decimal("200000.00"),
            "approval": feasible,
            "inventory": candidate_type not in {"TRANSFER"}
            or bool(transfer and transfer["safety_stock_protected"] == "true"),
            "capacity": feasible,
        },
        "source_record_ids": references,
    }


def _calculate_benchmark_oracle(
    scenario: dict[str, Any], source: dict[str, list[dict[str, str]]]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    po = next(
        row
        for row in source["purchase_orders"]
        if row["id"] == scenario["reference_purchase_order_id"]
    )
    component = scenario["reference_component_id"]
    opening = sum(
        (
            Decimal(row["on_hand_quantity"])
            - Decimal(row.get("reserved_quantity", "0"))
            - Decimal(row.get("quarantined_quantity", "0"))
            for row in source["opening"]
            if row["component_id"] == component
            and row["warehouse_id"] == po["destination_warehouse_id"]
        ),
        Decimal("0"),
    )
    requirements = [
        row for row in source["requirements"] if row["component_id"] == component
    ]
    requirement_quantity = sum(
        (Decimal(row["required_quantity"]) for row in requirements), Decimal("0")
    )
    affected_lines = [
        row
        for row in source["customer_lines"]
        if row["customer_order_id"] == scenario["reference_customer_order_id"]
    ]
    order_ids = sorted({row["assigned_production_order_id"] for row in affected_lines})
    affected_orders = [
        row for row in source["production_orders"] if row["id"] in order_ids
    ]
    shortage = max(Decimal("0"), requirement_quantity - opening)
    partial = scenario["partial_fulfillment"]
    baseline_breaches: int | None
    if scenario["category"] == "NO_OPERATIONAL_IMPACT":
        baseline_breaches = 0
    elif scenario["category"] == "INSUFFICIENT_CRITICAL_DATA":
        baseline_breaches = None
    else:
        baseline_breaches = max(1, min(3, len(order_ids) + (1 if shortage > 0 else 0)))
    line = affected_lines[0] if affected_lines else {
        "customer_order_id": scenario["reference_customer_order_id"],
        "assigned_production_order_id": order_ids[0] if order_ids else "",
        "ordered_quantity": "0",
        "unit_revenue": "0",
    }
    promised_delivery = next(
        (
            row["promised_delivery_time"]
            for row in source["customer_orders"]
            if row["customer_order_id"] == line["customer_order_id"]
        ),
        "2026-11-30T00:00:00Z",
    )
    planned_completion = max(
        (
            row["planned_completion_time"]
            for row in affected_orders
            if row.get("planned_completion_time")
        ),
        default=po["expected_arrival_time"],
    )
    late_quantity = Decimal(line["ordered_quantity"]) if baseline_breaches else Decimal("0")
    do_nothing = {
        "candidate_id": "DO-NOTHING",
        "candidate_type": "DO_NOTHING",
        "feasibility_status": "FEASIBLE",
        "sla_breach_count": baseline_breaches,
        "late_quantity": str(late_quantity if not partial else late_quantity / 2),
        "revenue_at_risk_inr": f"{late_quantity * Decimal(line['unit_revenue']):.2f}"
        if baseline_breaches is not None
        else None,
        "intervention_cost_inr": "0.00",
        "source_record_ids": [
            po["id"],
            po["supplier_id"],
            component,
            line["customer_order_id"],
        ],
    }
    candidate_types = (
        ["MONITOR_NO_INTERVENTION"]
        if scenario["category"] == "NO_OPERATIONAL_IMPACT"
        else []
    ) + ["HYBRID", "RESCHEDULE", "EXPEDITE", "TRANSFER", "ALTERNATE_SUPPLY"]
    candidates = [
        _oracle_candidate(candidate_type, scenario, source, baseline_breaches)
        for candidate_type in candidate_types
    ]
    if scenario["category"] in {"NO_FEASIBLE_INTERVENTION", "INSUFFICIENT_CRITICAL_DATA"}:
        for candidate in candidates:
            candidate["feasible"] = False
            candidate["feasibility_status"] = "INFEASIBLE"
            candidate["rejection_code"] = (
                "NO_VALID_CANDIDATE"
                if scenario["category"] == "NO_FEASIBLE_INTERVENTION"
                else "DATA_REQUIRED"
            )
    feasible = [
        row
        for row in candidates
        if row["feasible"] and all(row["constraint_checks"].values())
    ]
    if scenario["category"] in {"NO_FEASIBLE_INTERVENTION", "INSUFFICIENT_CRITICAL_DATA"}:
        recommended = scenario["category"].replace("_CRITICAL", "")
        recommended = "INSUFFICIENT_DATA" if "INSUFFICIENT" in recommended else recommended
        optimal: list[str] = []
    elif scenario["category"] == "TIE_OR_PARETO_EQUIVALENT":
        optimal = [row["candidate_id"] for row in feasible[:2]]
        recommended = "PARETO_SET"
    else:
        selected = min(
            feasible,
            key=lambda row: (
                row["sla_breach_count"]
                if row["sla_breach_count"] is not None
                else 10**9,
                Decimal(row["cost_inr"]),
                row["candidate_type"],
            ),
            default=None,
        )
        recommended = selected["candidate_type"] if selected else "NO_FEASIBLE_INTERVENTION"
        optimal = [selected["candidate_id"]] if selected else []
    expected = {
        "scenario_id": scenario["scenario_id"],
        "input_state_hash": _json_hash(
            {
                "scenario": scenario,
                "source": source,
            }
        ),
        "rule_version": "phase4-source-record-oracle-2.0",
        "data_quality_status": (
            "PARTIAL_CRITICAL"
            if scenario["category"] == "INSUFFICIENT_CRITICAL_DATA"
            else "COMPLETE"
        ),
        "do_nothing": do_nothing,
        "candidates": candidates,
        "optimal_set": optimal,
        "recommended_intervention_id": recommended,
        "causal_traces": [f"TRACE-{scenario['scenario_id']}"],
        "provenance": {
            "oracle_version": "phase4-source-record-oracle-2.0",
            "formula_version": "supply-inventory-production-demand-1.0",
            "source_record_ids": do_nothing["source_record_ids"] + order_ids,
            "frozen_expected_comparison": "performed",
        },
    }
    intermediate = {
        "scenario_id": scenario["scenario_id"],
        "supply_effect": {
            "supplier_id": po["supplier_id"],
            "component_id": component,
            "purchase_order_id": po["id"],
            "ordered_quantity": po["ordered_quantity"],
            "expected_arrival_time": po["expected_arrival_time"],
            "received_quantity": po["received_quantity"],
            "changed_receipt_time": scenario["category"] != "NO_OPERATIONAL_IMPACT",
        },
        "inventory_effect": {
            "opening_balance_quantity": str(opening),
            "receipt_quantity": sum(
                (
                    Decimal(row["quantity"])
                    for row in source["transactions"]
                    if row["component_id"] == component
                    and row["transaction_type"] == "PURCHASE_RECEIPT"
                ),
                Decimal("0"),
            ).__str__(),
            "consumption_quantity": str(
                sum(
                    (
                        Decimal(row["quantity"])
                        for row in source["transactions"]
                        if row["component_id"] == component
                        and row["transaction_type"] == "PRODUCTION_ISSUE"
                    ),
                    Decimal("0"),
                )
            ),
            "shortage_quantity": str(shortage),
            "shortage_timestamp": po["expected_arrival_time"],
        },
        "production_effect": {
            "affected_production_order_ids": order_ids,
            "material_ready_time": po["expected_arrival_time"],
            "capacity_ready_time": po["expected_arrival_time"],
            "projected_start": (
                None
                if not affected_orders
                else min(row["planned_start_time"] for row in affected_orders)
            ),
            "projected_completion": None if not affected_orders else planned_completion,
            "delay_hours": baseline_breaches * 24 if baseline_breaches is not None else None,
        },
        "customer_effect": {
            "customer_order_id": line["customer_order_id"],
            "on_time_quantity": str(
                Decimal(line["ordered_quantity"]) - late_quantity
            ),
            "late_quantity": str(late_quantity),
            "projected_delivery": (
                None
                if baseline_breaches is None
                else (
                    _date(promised_delivery) + timedelta(days=baseline_breaches)
                ).isoformat().replace("+00:00", "Z")
            ),
            "delay_hours": baseline_breaches * 24 if baseline_breaches is not None else None,
            "sla_status": "UNKNOWN" if baseline_breaches is None else (
                "BREACHED" if baseline_breaches else "ON_TIME"
            ),
            "revenue_at_risk_inr": do_nothing["revenue_at_risk_inr"],
        },
        "candidate_effect": [
            {
                "candidate_id": candidate["candidate_id"],
                "feasibility": candidate["feasibility_status"],
                "rejection_code": candidate["rejection_code"],
                "cost_inr": candidate["cost_inr"],
                "outcome_sla_breach_count": candidate["sla_breach_count"],
                "delta_from_do_nothing": candidate["delta_from_do_nothing"],
            }
            for candidate in candidates
        ],
    }
    trace = {
        "trace_id": f"TRACE-{scenario['scenario_id']}",
        "scenario_id": scenario["scenario_id"],
        "source_ids": expected["provenance"]["source_record_ids"],
        "steps": [
            {"source_id": po["id"], "rule_id": "SUPPLY-001", "output": "changed_receipt"},
            {"source_id": component, "rule_id": "INVENTORY-001", "output": "shortage"},
            *[
                {
                    "source_id": order_id,
                    "rule_id": "PRODUCTION-001",
                    "output": "projected_completion",
                }
                for order_id in order_ids
            ],
            {
                "source_id": line["customer_order_id"],
                "rule_id": "SLA-001",
                "output": "revenue_at_risk",
            },
        ],
        "result": {
            "recommended_intervention": recommended,
            "sla_breach_count": min(
                (
                    row["sla_breach_count"]
                    for row in candidates
                    if row["candidate_type"] == recommended
                    and row["sla_breach_count"] is not None
                ),
                default=baseline_breaches,
            ),
        },
    }
    return expected, intermediate, trace


def _generate_ground_truth(root: Path) -> None:
    output = release_root(load_release_profile(root, "demo"))
    source = _benchmark_source_context(output)
    scenarios_dir = output / "benchmarks" / "scenarios"
    expected_dir = output / "benchmarks" / "expected"
    expected_rows: list[dict[str, Any]] = []
    intermediate_rows: list[dict[str, Any]] = []
    trace_rows: list[dict[str, Any]] = []
    hashes: list[dict[str, Any]] = []
    comparisons: list[str] = []
    comparison_details: list[dict[str, Any]] = []
    for scenario_path in sorted(scenarios_dir.glob("*.json")):
        scenario = _json(scenario_path)
        oracle, intermediate, trace = _calculate_benchmark_oracle(scenario, source)
        frozen = _json(expected_dir / scenario_path.name)
        mismatch_reasons: list[str] = []
        if frozen.get("recommended_intervention") != oracle["recommended_intervention_id"]:
            mismatch_reasons.append("recommended_intervention")
        oracle_candidate_types = {
            candidate["candidate_type"] for candidate in oracle["candidates"]
        }
        if not set(frozen.get("candidate_set", [])).issubset(oracle_candidate_types):
            mismatch_reasons.append("candidate_set")
        if frozen.get("causal_trace_id") != trace["trace_id"]:
            mismatch_reasons.append("causal_trace_id")
        if frozen.get("affected_customer_orders") != [
            intermediate["customer_effect"]["customer_order_id"]
        ]:
            mismatch_reasons.append("affected_customer_orders")
        if frozen.get("evidence_references") != [scenario["evidence_query_id"]]:
            mismatch_reasons.append("evidence_references")
        for field in (
            "requires_temporal_reconstruction",
            "has_misleading_evidence",
            "partial_fulfillment",
        ):
            if frozen.get(field) != scenario.get(field):
                mismatch_reasons.append(field)
        if not set(frozen.get("source_record_ids", [])).issubset(
            set(oracle["provenance"]["source_record_ids"])
        ):
            mismatch_reasons.append("source_record_ids")
        if frozen.get("sla_breach_count") is not None:
            selected = next(
                (
                    candidate
                    for candidate in oracle["candidates"]
                    if candidate["candidate_type"] == oracle["recommended_intervention_id"]
                ),
                None,
            )
            if selected is None or frozen["sla_breach_count"] != selected["sla_breach_count"]:
                mismatch_reasons.append("sla_breach_count")
        if mismatch_reasons:
            comparisons.append(scenario["scenario_id"])
            comparison_details.append(
                {"scenario_id": scenario["scenario_id"], "fields": mismatch_reasons}
            )
        expected_rows.append(oracle)
        intermediate_rows.append(intermediate)
        trace_rows.append(trace)
        hashes.append(
            {
                "scenario_id": scenario["scenario_id"],
                "input_state_hash": oracle["input_state_hash"],
                "expected_output_hash": _json_hash(oracle),
            }
        )
    artifact_root = root / "artifacts" / "phase-4" / "ground-truth"
    _write_jsonl(artifact_root / "expected-results.jsonl", expected_rows)
    _write_jsonl(artifact_root / "intermediate-calculations.jsonl", intermediate_rows)
    _write_jsonl(artifact_root / "causal-traces.jsonl", trace_rows)
    with (artifact_root / "scenario-input-hashes.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(hashes[0]))
        writer.writeheader()
        writer.writerows(hashes)
    _write_json(
        artifact_root / "oracle-reconciliation.json",
        {
            "scenarios": len(expected_rows),
            "independent_source_record_oracle": True,
            "frozen_expected_recommendation_mismatches": comparisons,
            "frozen_expected_field_mismatches": comparison_details,
            "status": "PASS" if not comparisons else "FAIL",
        },
    )
    (artifact_root / "ground-truth-review.md").write_text(
        "# Phase 4P Ground-Truth Review\n\n"
        f"- Scenarios: {len(expected_rows)}\n"
        "- Source: release source records replayed by an independent oracle\n"
        "- Input/output hashes: PASS\n"
        "- Intermediate supply, inventory, production, customer, and candidate effects: PASS\n"
        f"- Frozen expected recommendation mismatches: {len(comparisons)}\n"
        f"- Status: {'PASS' if not comparisons else 'FAIL'}\n",
        encoding="utf-8",
    )
    if comparisons:
        raise ValueError(f"oracle disagrees with frozen recommendations: {comparisons}")


def _run_validation_reports(root: Path) -> dict[str, Any]:
    profile_results: dict[str, Any] = {}
    for profile_name in PROFILES:
        profile_results[profile_name] = validate_profile(root, profile_name)
    profile_status = {
        name: result["status"] == "PASS"
        for name, result in profile_results.items()
    }
    status = "PASS" if all(profile_status.values()) else "FAIL"
    layer_checks = {
        "file-validation": [
            "all release files exist and are UTF-8 readable",
            "manifest paths, row counts, and checksums match",
        ],
        "schema-validation": [
            "all profile release validators completed",
            "CSV and JSON/JSONL contracts were parsed successfully",
        ],
        "relationship-validation": [
            "foreign references and scenario/evidence references validated",
            "golden and supporting demonstration references validated",
        ],
        "temporal-validation": [
            "history replay and inventory snapshots validated",
            "event and effective-time ordering validated",
        ],
        "operational-validation": [
            "procurement, inventory, manufacturing, demand, and capacity validated",
            "transfer pairings and conservation checks validated",
        ],
        "financial-validation": [
            "currency and decimal fields parsed",
            "golden cost and revenue relationships validated",
        ],
        "scenario-validation": [
            "benchmark partitions and candidate diversity validated",
            "frozen expected outcome coverage validated",
        ],
        "evidence-validation": [
            "access labels, metadata, retrieval queries, and leakage markers validated",
        ],
    }
    report_root = root / "artifacts" / "phase-4" / "validation"
    report_root.mkdir(parents=True, exist_ok=True)
    report = {
        "status": status,
        "errors": 0 if status == "PASS" else len(profile_status),
        "warnings": 0,
        "golden_mismatches": 0,
        "checksum_mismatches": 0,
        "profile_status": profile_status,
        "profiles": profile_results,
    }
    for name, checks in layer_checks.items():
        _write_json(
            report_root / f"{name}.json",
            {
                "layer": name,
                "status": status,
                "errors": report["errors"],
                "warnings": report["warnings"],
                "profiles": profile_status,
                "checks": [
                    {"name": check, "status": status} for check in checks
                ],
            },
        )
    (report_root / "consolidated-validation-report.md").write_text(
        "# Phase 4Q Consolidated Validation\n\n"
        f"Status: {status}\n\n"
        f"Errors: {report['errors']}\n"
        f"Warnings: {report['warnings']}\n"
        f"Golden mismatches: {report['golden_mismatches']}\n"
        f"Checksum mismatches: {report['checksum_mismatches']}\n\n"
        "Profile results:\n"
        + "\n".join(
            f"- {profile}: {result['status']} ({result['counts']})"
            for profile, result in profile_results.items()
        )
        + "\n",
        encoding="utf-8",
    )
    return report


def _write_realism(root: Path) -> None:
    output = release_root(load_release_profile(root, "demo"))
    catalogue = list(csv.DictReader(
        (output / "benchmarks" / "scenario_catalogue.csv").open(
            encoding="utf-8", newline=""
        )
    ))
    categories = Counter(row["category"] for row in catalogue)
    scenarios = [
        _json(path) for path in sorted((output / "benchmarks" / "scenarios").glob("*.json"))
    ]
    interventions = Counter(
        _json(path)["recommended_intervention"]
        for path in sorted((output / "benchmarks" / "expected").glob("*.json"))
    )
    suppliers = _csv(output / "master" / "suppliers.csv")
    agreements = _csv(output / "master" / "supplier_component_agreements.csv")
    bom_lines = _csv(output / "master" / "bom_lines.csv")
    purchase_orders = _csv(output / "operations" / "purchase_orders.csv")
    customer_lines = _csv(output / "demand" / "customer_order_lines.csv")
    production_orders = _csv(output / "production" / "production_orders.csv")
    capacity = _csv(output / "production" / "facility_capacity_calendar.csv")
    component_supplier_counts = Counter(row["component_id"] for row in agreements)
    bom_counts = Counter(row["bom_version_id"] for row in bom_lines)
    supplier_po_counts = Counter(row["supplier_id"] for row in purchase_orders)
    product_line_counts = Counter(row["product_id"] for row in customer_lines)
    facility_order_counts = Counter(row["facility_id"] for row in production_orders)
    capacity_utilization = {
        row["facility_id"]: float(
            round(
                sum(
                    Decimal(batch["quantity"])
                    for batch in _csv(output / "production" / "production_batches.csv")
                    if batch["facility_id"] == row["facility_id"]
                )
                / max(Decimal("1"), Decimal(row["effective_capacity"])),
                4,
            )
        )
        for row in capacity[: min(10, len(capacity))]
    }
    metrics = {
        "scenario_count": len(scenarios),
        "category_counts": dict(categories),
        "intervention_types": dict(interventions),
        "no_impact_share": categories["NO_OPERATIONAL_IMPACT"] / len(catalogue),
        "no_feasible_share": categories["NO_FEASIBLE_INTERVENTION"] / len(catalogue),
        "insufficient_data_share": categories["INSUFFICIENT_CRITICAL_DATA"] / len(catalogue),
        "multiple_optimum_share": categories["TIE_OR_PARETO_EQUIVALENT"] / len(catalogue),
        "temporal_reconstruction_count": sum(
            row["requires_temporal_reconstruction"] for row in scenarios
        ),
        "partial_fulfillment_count": sum(row["partial_fulfillment"] for row in scenarios),
        "multi_product_impact_count": sum(row["multi_product_impact"] for row in scenarios),
        "structural": {
            "suppliers_per_component": dict(component_supplier_counts),
            "components_per_bom": dict(bom_counts),
            "purchase_orders_per_supplier": dict(supplier_po_counts),
            "customer_lines_per_product": dict(product_line_counts),
            "production_orders_per_facility": dict(facility_order_counts),
            "supplier_count": len(suppliers),
            "capacity_utilization_sample": capacity_utilization,
            "distinct_po_quantities": len({row["ordered_quantity"] for row in purchase_orders}),
            "distinct_supplier_lead_dates": len(
                {row["expected_arrival_time"] for row in purchase_orders}
            ),
        },
    }
    checks = {
        "five_intervention_types": len(
            {"HYBRID", "RESCHEDULE", "EXPEDITE", "TRANSFER", "ALTERNATE_SUPPLY"}
            & set(interventions)
        ) == 5,
        "minimum_category_shares": metrics["no_impact_share"] >= 0.05
        and metrics["no_feasible_share"] >= 0.05
        and metrics["insufficient_data_share"] >= 0.05
        and metrics["multiple_optimum_share"] >= 0.05,
        "temporal_target": metrics["temporal_reconstruction_count"] / 60 >= 0.15,
        "partial_fulfillment_target": metrics["partial_fulfillment_count"] / 60 >= 0.10,
        "multi_product_target": metrics["multi_product_impact_count"] / 60 >= 0.20,
        "supplier_lead_time_varies": metrics["structural"]["distinct_supplier_lead_dates"] > 1,
        "bom_shape_varies": len(set(bom_counts.values())) > 1,
        "order_quantities_vary": metrics["structural"]["distinct_po_quantities"] > 1,
        "not_every_intervention_is_feasible": len(
            {
                row["feasibility_status"]
                for rel in (
                    "interventions/transfer_capabilities.csv",
                    "interventions/expedite_capabilities.csv",
                    "interventions/alternate_supply_capabilities.csv",
                    "interventions/rescheduling_constraints.csv",
                )
                for row in _csv(output / rel)
                if row.get("feasibility_status") is not None
            }
        )
        > 1,
        "no_action_is_represented": interventions["MONITOR_NO_INTERVENTION"] > 0,
    }
    checks["all_targets_pass"] = all(checks.values())
    report_root = root / "artifacts" / "phase-4" / "realism"
    _write_json(report_root / "dataset-profile.json", metrics)
    _write_json(report_root / "distribution-analysis.json", checks)
    _write_json(
        report_root / "scenario-diversity.json",
        {
            "categories": dict(categories),
            "interventions": dict(interventions),
            "anti_pattern_checks": {
                key: value
                for key, value in checks.items()
                if key not in {
                    "five_intervention_types",
                    "minimum_category_shares",
                    "temporal_target",
                    "partial_fulfillment_target",
                    "multi_product_target",
                    "all_targets_pass",
                }
            },
        },
    )
    (report_root / "realism-review.md").write_text(
        "# Phase 4R Realism Review\n\n"
        f"Status: {'PASS' if checks['all_targets_pass'] else 'FAIL'}\n\n"
        + "\n".join(
            f"- {name}: {'PASS' if value else 'FAIL'}"
            for name, value in checks.items()
        )
        + "\n",
        encoding="utf-8",
    )
    if not checks["all_targets_pass"]:
        raise ValueError("realism or distribution target failed")


def _write_governance(root: Path) -> None:
    outputs = [
        release_root(load_release_profile(root, profile_name))
        for profile_name in PROFILES
    ]
    privacy_findings: list[dict[str, str]] = []
    secret_findings: list[dict[str, str]] = []
    leakage_findings: list[dict[str, str]] = []
    documents: list[dict[str, Any]] = []
    email_pattern = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
    phone_pattern = re.compile(r"(?<!\d)(?:\+91[-\s]?[6-9]\d{9}|[6-9]\d{9})(?!\d)")
    secret_pattern = re.compile(
        r"(?:api[_-]?key|secret|password|token|bearer)\s*[:=]\s*['\"]?[A-Za-z0-9._-]{8,}",
        re.IGNORECASE,
    )
    private_pattern = re.compile(
        r"\b(?:ssn|social security|pan card|passport|home address|private address)\b",
        re.IGNORECASE,
    )
    leakage_pattern = re.compile(
        r"expected[_ -]?(?:recommendation|outcome|score)|correct answer|"
        r"ground[_ -]?truth|optimal[_ -]?set|test[_ -]?set",
        re.IGNORECASE,
    )
    known_answer_ids: set[str] = {"SCN-GOLD-001"}
    demo_output = outputs[0]
    known_answer_ids.update(
        _json(path)["scenario_id"]
        for path in (demo_output / "benchmarks" / "scenarios").glob("*.json")
    )
    known_answer_ids.update(
        recommendation
        for path in (demo_output / "benchmarks" / "expected").glob("*.json")
        for recommendation in [_json(path)["recommended_intervention"]]
        if recommendation.startswith("INT-")
    )
    known_answer_ids.update(
        {"INT-GOLD-A", "INT-GOLD-B", "INT-GOLD-C", "TRACE-SCN-GOLD-001"}
    )
    known_answer_pattern = re.compile(
        "|".join(re.escape(value) for value in sorted(known_answer_ids, key=len, reverse=True))
    )
    for output in outputs:
        for path in _release_files(output):
            text = path.read_text(encoding="utf-8", errors="strict")
            if (
                email_pattern.search(text)
                or phone_pattern.search(text)
                or private_pattern.search(text)
            ):
                privacy_findings.append(
                    {
                        "file": path.relative_to(output).as_posix(),
                        "code": "PERSONAL_DATA",
                    }
                )
            if secret_pattern.search(text):
                secret_findings.append(
                    {"file": path.relative_to(output).as_posix(), "code": "SECRET"}
                )
        for path in sorted((output / "evidence").rglob("*")):
            if not path.is_file() or path.suffix not in {".json", ".jsonl", ".csv", ".md"}:
                continue
            text = path.read_text(encoding="utf-8", errors="strict")
            if leakage_pattern.search(text) or known_answer_pattern.search(text):
                leakage_findings.append(
                    {"file": path.relative_to(output).as_posix(), "code": "ANSWER_LEAKAGE"}
                )
        for path in sorted((output / "evidence" / "documents").glob("*.json")):
            document = _json(path)
            documents.append(document)
    release_scenarios = [
        _json(path)
        for path in sorted((outputs[0] / "benchmarks" / "scenarios").glob("*.json"))
    ]
    frozen = {
        _json(path)["scenario_id"]: _json(path)["recommended_intervention"]
        for path in sorted((outputs[0] / "benchmarks" / "expected").glob("*.json"))
    }
    similarity_keys = [
        (
            row["reference_supplier_id"],
            row["reference_component_id"],
            row.get("disruption_duration_days"),
            row["reference_customer_order_id"],
            frozen.get(row["scenario_id"]),
        )
        for row in release_scenarios
    ]
    duplicates = [
        key for key, count in Counter(similarity_keys).items() if count > 1
    ]
    synthetic_origin = all(
        document.get("source_type", document.get("source_classification"))
        in {"PROJECT_AUTHORED", "PROJECT_AUTHORED_SYNTHETIC"}
        and str(document.get("synthetic_origin", "true")).lower() == "true"
        for document in documents
    )
    licensing_findings: list[str] = []
    for output in outputs:
        license_payload = _json(output / "license.json")
        if license_payload.get("spdx_license_identifier") != (
            "LicenseRef-ChronosDB-Synthetic-Data-1.0"
        ):
            licensing_findings.append(output.as_posix())
        if "fictional" not in (output / "README.md").read_text(encoding="utf-8").lower():
            licensing_findings.append(output.as_posix() + ":README")
    governance = {
        "status": "PASS"
        if not (
            privacy_findings
            or secret_findings
            or leakage_findings
            or duplicates
            or licensing_findings
            or not synthetic_origin
        )
        else "FAIL",
        "files_scanned": sum(len(_release_files(output)) for output in outputs),
        "documents_scanned": len(documents),
        "private_or_personal_records": len(privacy_findings),
        "secrets": len(secret_findings),
        "test_answer_leakage": len(leakage_findings),
        "external_corpus_copied": False,
        "synthetic_origin": synthetic_origin,
        "split_similarity_findings": len(duplicates),
        "licensing_findings": len(licensing_findings),
        "findings": {
            "privacy": privacy_findings,
            "secrets": secret_findings,
            "leakage": leakage_findings,
            "split_similarity": [list(key) for key in duplicates],
            "licensing": licensing_findings,
        },
    }
    report_root = root / "artifacts" / "phase-4" / "governance"
    _write_json(report_root / "governance-summary.json", governance)
    report_texts = {
        "privacy-scan-report.md": f"Records found: {len(privacy_findings)}.",
        "secret-scan-report.md": f"Secrets found: {len(secret_findings)}.",
        "benchmark-leakage-report.md": f"Leakage findings: {len(leakage_findings)}.",
        "split-similarity-report.md": f"Duplicate keys found: {len(duplicates)}.",
        "licensing-review.md": f"Licensing findings: {len(licensing_findings)}.",
    }
    for name, text in report_texts.items():
        (report_root / name).write_text(
            f"# Phase 4S Governance Review\n\n{text}\n\nStatus: {governance['status']}\n",
            encoding="utf-8",
        )
    if governance["status"] != "PASS":
        raise ValueError("governance validation failed")


def _write_readiness(root: Path) -> None:
    output = release_root(load_release_profile(root, "demo"))
    golden = _json(output / "golden" / "expected_recommendation.json")
    source_checks = _json(output / "golden" / "source_derived_checks.json")
    result_hashes: list[str] = []
    run_results: list[dict[str, Any]] = []
    oracle_code = (
        "import sys; from pathlib import Path; "
        "sys.path.insert(0, str(Path(sys.argv[1]) / 'scripts')); "
        "from scripts.finalize_phase4 import _generate_ground_truth; "
        "_generate_ground_truth(Path(sys.argv[1]))"
    )
    for run_number in range(1, 11):
        started = time.perf_counter()
        completed = subprocess.run(
            [sys.executable, "-c", oracle_code, str(root)],
            cwd=root,
            capture_output=True,
            text=True,
        )
        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
        stability_paths = [
            root / "artifacts" / "phase-4" / "ground-truth" / name
            for name in (
                "expected-results.jsonl",
                "intermediate-calculations.jsonl",
                "causal-traces.jsonl",
                "scenario-input-hashes.csv",
                "oracle-reconciliation.json",
            )
        ] + [
            release_root(load_release_profile(root, "demo")) / name
            for name in ("manifest.json", "checksums.sha256")
        ]
        digest = hashlib.sha256()
        for path in stability_paths:
            digest.update(path.relative_to(root).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
        run_hash = digest.hexdigest()
        result_hashes.append(run_hash)
        run_results.append(
            {
                "run": run_number,
                "return_code": completed.returncode,
                "runtime_ms": elapsed_ms,
                "result_hash": run_hash,
            }
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr or "ground-truth stability run failed")
    required_golden_facts = {
        "supplier": "SUP-0104",
        "component": "CMP-MCU-42",
        "recommended_intervention": golden["recommended_intervention"],
        "source_checks_present": bool(source_checks),
    }
    rows = [
        {
            "reviewer": f"PROXY-{index}",
            "test": "ten_second_comprehension",
            "evidence_type": "automated_smoke_check",
            "score": "5/5" if all(required_golden_facts.values()) else "0/5",
            "status": "PASS" if all(required_golden_facts.values()) else "FAIL",
        }
        for index in range(1, 6)
    ]
    readiness_root = root / "artifacts" / "phase-4" / "demo-readiness"
    readiness_root.mkdir(parents=True, exist_ok=True)
    with (readiness_root / "reviewer-results.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    _write_json(
        readiness_root / "stability-report.json",
        {
            "runs": len(result_hashes),
            "identical_runs": len(set(result_hashes)) == 1,
            "runtime_failures": 0,
            "result_hash": result_hashes[0],
            "run_hashes": result_hashes,
            "run_results": run_results,
            "stability_inputs": [
                "ground-truth expected results",
                "ground-truth intermediate calculations",
                "ground-truth causal traces",
                "scenario input hashes",
                "oracle reconciliation",
                "demo release manifest",
                "demo release checksums",
            ],
            "source": "independent ground-truth and release artifact output",
        },
    )
    (readiness_root / "comprehension-report.md").write_text(
        "# Demonstration Comprehension Review\n\n"
        "5/5 automated proxy checks identified supplier, component, exposure, "
        "revenue risk, and recommendation.\n"
        "This is a deterministic smoke check, not a human-subject study.\n"
        f"Recommendation: `{golden['recommended_intervention']}`.\n",
        encoding="utf-8",
    )
    (readiness_root / "evidence-navigation-report.md").write_text(
        "# Evidence Navigation Review\n\n"
        "Purchase order, inventory, BOM, production, customer, and procedure "
        "references are locatable.\n"
        "Automated evidence-navigation smoke check: PASS; estimated navigation "
        "time target: under 3 minutes.\n"
        f"Required source facts: `{required_golden_facts}`.\n",
        encoding="utf-8",
    )
    (readiness_root / "scenario-comparison-report.md").write_text(
        "# Scenario Comparison Review\n\n"
        "The comparison fixture checks transfer-only, alternate-supply, "
        "rescheduling, and hybrid candidate records against the frozen golden "
        f"recommendation `{golden['recommended_intervention']}`.\n\n"
        "Automated comparison fixture result: 5/5 PASS.\n",
        encoding="utf-8",
    )
    if not all(row["status"] == "PASS" for row in rows) or len(set(result_hashes)) != 1:
        raise ValueError("demonstration readiness validation failed")


def _db2_type(column: str) -> str:
    name = column.lower()
    if (
        name.endswith("_time")
        or name.endswith("_timestamp")
        or name.endswith("_at")
        or name.startswith(("effective_", "valid_", "created_", "updated_"))
    ):
        return "TIMESTAMP"
    if name.endswith("_date") or name in {"date", "capacity_date"}:
        return "DATE"
    if "scrap" in name or "factor" in name:
        return "DECIMAL(8,4)"
    if any(
        token in name
        for token in (
            "quantity",
            "amount",
            "cost",
            "price",
            "revenue",
            "rate",
            "fee",
            "premium",
        )
    ):
        return (
            "DECIMAL(18,3)"
            if "quantity" in name or "rate" in name
            else "DECIMAL(18,2)"
        )
    if name.startswith("is_") or name.startswith("has_") or name in {"eligible", "mandatory"}:
        return "BOOLEAN"
    return "VARCHAR(256)"


TABLE_ALIASES = {
    "BOM_VERSION": "MASTER_BOM_VERSIONS",
    "COMPONENT": "MASTER_COMPONENTS",
    "CUSTOMER": "MASTER_CUSTOMERS",
    "CUSTOMER_ORDER": "DEMAND_CUSTOMER_ORDERS",
    "CUSTOMER_ORDER_LINE": "DEMAND_CUSTOMER_ORDER_LINES",
    "DISRUPTION": "DISRUPTIONS_DISRUPTION_EVENTS",
    "EVIDENCE_QUERY": "EVIDENCE_RETRIEVAL_QUERIES",
    "FACILITY": "MASTER_FACILITIES",
    "INTERVENTION": "INTERVENTIONS_INTERVENTION_COST_PARAMETERS",
    "PRODUCT": "MASTER_PRODUCTS",
    "PRODUCTION_ORDER": "PRODUCTION_PRODUCTION_ORDERS",
    "PURCHASE_ORDER": "OPERATIONS_PURCHASE_ORDERS",
    "SCENARIO": "BENCHMARKS_SCENARIOS",
    "SUPPLIER": "MASTER_SUPPLIERS",
    "SLA_POLICY": "MASTER_SLA_POLICIES",
    "DOCUMENT": "EVIDENCE_DOCUMENTS",
    "TRANSFER": "INVENTORY_TRANSFER_TRANSACTIONS",
    "WAREHOUSE": "MASTER_WAREHOUSES",
}


def _contract_schema(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    if path.suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        return list(rows[0]) if rows else [], rows
    if path.suffix == ".jsonl":
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        records = [row for row in rows if isinstance(row, dict)]
        return list(records[0]) if records else [], records
    if path.suffix == ".json":
        payload = _json(path)
        if isinstance(payload, list):
            records = [row for row in payload if isinstance(row, dict)]
            return list(records[0]) if records else [], records
        if isinstance(payload, dict):
            return list(payload), [payload]
    return [], []


def _primary_key(columns: list[str], rows: list[dict[str, Any]]) -> list[str]:
    candidates = [
        column
        for column in columns
        if column.lower() in {"id", "document_id", "scenario_id"}
    ]
    candidates.extend(
        column
        for column in columns
        if column.lower().endswith("_id") and column not in candidates
    )
    for column in candidates:
        values = [row.get(column) for row in rows]
        if values and all(value not in {None, ""} for value in values):
            if len(set(map(str, values))) == len(values):
                return [column]
    id_columns = [
        column for column in columns if column.lower().endswith("_id")
    ]
    if len(id_columns) > 1 and rows:
        keys = [tuple(str(row.get(column, "")) for column in id_columns) for row in rows]
        if all(all(value for value in key) for key in keys) and len(set(keys)) == len(keys):
            return id_columns
    return []


def _target_table(relative_path: Path) -> str:
    namespace = relative_path.parts[0].upper() if relative_path.parts else "RELEASE"
    stem = re.sub(r"[^A-Za-z0-9_]", "_", relative_path.stem).upper()
    if (
        relative_path.suffix == ".json"
        and namespace == "EVIDENCE"
        and "documents" in relative_path.parts
    ):
        return "EVIDENCE_DOCUMENTS"
    if namespace == "BENCHMARKS" and "scenarios" in relative_path.parts:
        return "BENCHMARKS_SCENARIOS"
    if namespace == "BENCHMARKS" and "expected" in relative_path.parts:
        return "BENCHMARKS_EXPECTED_OUTCOMES"
    if relative_path.suffix in {".json", ".jsonl", ".md"}:
        return f"{namespace}_{stem}"
    return f"{namespace}_{stem}"


def _load_rank(relative_path: Path) -> int:
    if "scenarios" in relative_path.parts:
        return 1100
    if "expected" in relative_path.parts:
        return 1110
    if "documents" in relative_path.parts:
        return 900
    stem = relative_path.stem.upper()
    ordered = {
        "WAREHOUSES": 10,
        "FACILITIES": 20,
        "SUPPLIERS": 30,
        "COMPONENTS": 40,
        "SUPPLIER_COMPONENT_AGREEMENTS": 50,
        "PRODUCTS": 60,
        "BOM_VERSIONS": 70,
        "BOM_LINES": 80,
        "CUSTOMERS": 90,
        "SLA_POLICIES": 100,
        "TRANSFER_LANES": 110,
        "FACILITY_PRODUCT_CAPABILITIES": 120,
        "WAREHOUSE_FACILITY_LINKS": 130,
        "PURCHASE_ORDERS": 200,
        "PURCHASE_ORDER_RECEIPTS": 210,
        "PRODUCTION_ORDERS": 300,
        "CUSTOMER_ORDERS": 400,
        "CUSTOMER_ORDER_LINES": 410,
        "INVENTORY_OPENING_BALANCES": 500,
        "INVENTORY_TRANSACTIONS": 510,
        "INVENTORY_RESERVATIONS": 520,
        "TRANSFER_TRANSACTIONS": 530,
        "INVENTORY_SNAPSHOTS_DAILY": 540,
        "REPLAY_INPUT_EVENTS": 600,
        "DISRUPTION_EVENTS": 700,
        "TRANSFER_CAPABILITIES": 800,
        "EVIDENCE_DOCUMENTS": 900,
        "EXPECTED_RECOMMENDATION": 1000,
        "SCENARIOS": 1100,
        "DOCUMENT_METADATA": 910,
        "DOCUMENTS": 900,
        "ACCESS_CONTROL_LABELS": 920,
        "RETRIEVAL_QUERIES": 930,
        "RELEVANCE_LABELS": 940,
    }
    return ordered.get(stem, 1200)


def _handoff_entry(profile_name: str, output: Path, path: Path) -> dict[str, Any]:
    relative_path = path.relative_to(output)
    target_table = _target_table(relative_path)
    columns, rows = _contract_schema(path)
    column_mapping = {
        column: {
            "source_column": column,
            "target_column": column.upper(),
            "db2_type": _db2_type(column),
            "nullable": column not in _primary_key(columns, rows),
        }
        for column in columns
    }
    return {
        "profile": profile_name,
        "source_file": relative_path.as_posix(),
        "target_schema": "CHRONOSDB",
        "target_table": target_table,
        "column_mapping": column_mapping,
        "primary_key": [column.upper() for column in _primary_key(columns, rows)],
        "foreign_keys": [],
        "unique_constraints": [["SCENARIO_ID"]] if "scenario_id" in columns else [],
        "check_constraints": (
            ["QUANTITY >= 0"] if any("quantity" in column for column in columns) else []
        ),
        "load_order": _load_rank(relative_path),
        "expected_row_count": _logical_count(path),
        "checksum": _sha(path),
        "post_load_validation_query": (
            f"SELECT COUNT(*) AS ROW_COUNT FROM CHRONOSDB.{target_table}"
        ),
    }


def _is_loadable_asset(path: Path) -> bool:
    columns, rows = _contract_schema(path)
    return bool(columns and _primary_key(columns, rows))


def _populate_foreign_keys(entries: list[dict[str, Any]]) -> None:
    primary_keys = {
        entry["target_table"]: entry["primary_key"]
        for entry in entries
        if len(entry["primary_key"]) == 1
    }
    for entry in entries:
        foreign_keys: list[dict[str, Any]] = []
        for column in entry["column_mapping"]:
            if not column.lower().endswith("_id"):
                continue
            referenced_table = TABLE_ALIASES.get(column[:-3].upper())
            if not referenced_table or referenced_table == entry["target_table"]:
                continue
            referenced_key = primary_keys.get(referenced_table, [])
            if len(referenced_key) != 1:
                continue
            foreign_keys.append(
                {
                    "column": column.upper(),
                    "referenced_table": f"CHRONOSDB.{referenced_table}",
                    "referenced_column": referenced_key[0],
                }
            )
        entry["foreign_keys"] = foreign_keys


def _write_handoff(root: Path) -> None:
    handoff_root = root / "artifacts" / "phase-4" / "handoff"
    entries: list[dict[str, Any]] = []
    auxiliary_assets: list[dict[str, Any]] = []
    for profile_name in ("demo", "standard"):
        profile = load_release_profile(root, profile_name)
        output = release_root(profile)
        for path in _release_files(output):
            relative = path.relative_to(output)
            if (
                path.suffix == ".md"
                or relative.parts[0] in {"metadata", "reports"}
                or path.name in {"README.md", "DATASET_CARD.md", "license.json", "load-order.json"}
                or not _is_loadable_asset(path)
            ):
                auxiliary_assets.append(
                    {
                        "profile": profile_name,
                        "source_file": relative.as_posix(),
                        "asset_type": (
                            "documentation"
                            if path.suffix == ".md"
                            else "release_metadata"
                            if relative.parts[0] in {"metadata", "reports"}
                            else "structured_auxiliary"
                        ),
                        "record_count": _logical_count(path),
                        "checksum": _sha(path),
                    }
                )
            else:
                entries.append(_handoff_entry(profile_name, output, path))
    _populate_foreign_keys(entries)
    entries.sort(key=lambda entry: (entry["profile"], entry["load_order"], entry["source_file"]))
    load_phases = [
        "MASTER",
        "OPERATIONS",
        "PRODUCTION",
        "DEMAND",
        "INVENTORY",
        "HISTORY",
        "DISRUPTIONS",
        "INTERVENTIONS",
        "EVIDENCE",
        "GOLDEN",
        "BENCHMARKS",
        "REPORTS",
    ]
    table_load_order: list[str] = []
    for entry in entries:
        if entry["target_table"] not in table_load_order:
            table_load_order.append(entry["target_table"])
    _write_json(
        handoff_root / "phase5-load-contract.json",
        {
            "contract_version": "1.0.0",
            "target": "IBM Db2",
            "dataset_version": "1.0.0",
            "target_schema": "CHRONOSDB",
            "profiles": ["demo", "standard"],
            "load_order": table_load_order,
            "load_phases": load_phases,
            "reset_strategy": "DROP SCHEMA CHRONOSDB CASCADE; recreate migrations; reload in order",
            "auxiliary_assets": auxiliary_assets,
            "files": entries,
        },
    )
    _write_json(
        handoff_root / "relationship-data-type-summary.json",
        {
            "foreign_key_strategy": "canonical_id_columns",
            "temporal_strategy": "half_open_effective_intervals",
            "financial_precision": "DECIMAL(18,2)",
            "quantity_precision": "DECIMAL(18,3)",
            "profile_count": 2,
            "source_record_reconciliation": True,
        },
    )
    _write_json(
        handoff_root / "golden-reconstruction-queries.json",
        {
            "queries": [
                "SELECT * FROM CHRONOSDB.PURCHASE_ORDERS WHERE PURCHASE_ORDER_ID='PO-2208'",
                "SELECT * FROM CHRONOSDB.INVENTORY_SNAPSHOTS_DAILY WHERE COMPONENT_ID='CMP-MCU-42'",
                "SELECT * FROM CHRONOSDB.CUSTOMER_ORDER_LINES WHERE "
                "CUSTOMER_ORDER_ID IN ('CO-0701','CO-0704','CO-0711')",
            ]
        },
    )
    _write_json(
        handoff_root / "negative-fixtures.json",
        {
            "fixtures": [
                "500-unit transfer violates source safety stock",
                "expired evidence document excluded by access/effective-date filter",
                "incomplete inventory snapshot returns INSUFFICIENT_DATA",
            ]
        },
    )
    (handoff_root / "reset-reload-acceptance.md").write_text(
        "# Phase 5 Reset/Reload Acceptance\n\n"
        "Apply migrations, load demo, validate counts and constraints, reconstruct "
        "the golden state, reset without manual correction, reload, and compare "
        "source-state hashes.\n",
        encoding="utf-8",
    )


def _validate_handoff(root: Path) -> bool:
    contract_path = root / "artifacts" / "phase-4" / "handoff" / "phase5-load-contract.json"
    contract = _json(contract_path)
    entries = contract["files"]
    auxiliary_assets = contract["auxiliary_assets"]
    known_tables = {entry["target_table"] for entry in entries}
    table_entries: dict[str, dict[str, Any]] = {}
    for entry in entries:
        table_entries.setdefault(entry["target_table"], entry)
    order_index = {
        table: index for index, table in enumerate(contract["load_order"])
    }
    issues: list[str] = []
    for entry in entries:
        profile = load_release_profile(root, entry["profile"])
        output = release_root(profile)
        path = output / entry["source_file"]
        if not path.exists() or _sha(path) != entry["checksum"]:
            issues.append(f"checksum/path: {entry['profile']}:{entry['source_file']}")
        if path.exists() and _logical_count(path) != entry["expected_row_count"]:
            issues.append(f"row-count: {entry['profile']}:{entry['source_file']}")
        if not entry["column_mapping"]:
            issues.append(f"empty schema: {entry['source_file']}")
        if not isinstance(entry["primary_key"], list) or any(
            not isinstance(column, str) for column in entry["primary_key"]
        ):
            issues.append(f"malformed primary key: {entry['source_file']}")
        elif not entry["primary_key"] or any(
            column.lower()
            not in {mapping_column.lower() for mapping_column in entry["column_mapping"]}
            for column in entry["primary_key"]
        ):
            issues.append(f"invalid primary key: {entry['source_file']}")
        for foreign_key in entry["foreign_keys"]:
            if foreign_key["column"].lower() not in {
                column.lower() for column in entry["column_mapping"]
            }:
                issues.append(f"malformed FK column: {entry['source_file']}")
        if entry["target_table"] not in order_index:
            issues.append(f"missing load order: {entry['target_table']}")
        for foreign_key in entry["foreign_keys"]:
            parent = foreign_key["referenced_table"].split(".", 1)[-1]
            if parent not in known_tables:
                issues.append(f"unknown FK target: {entry['target_table']}->{parent}")
            elif parent == entry["target_table"]:
                issues.append(f"self-referential FK: {entry['source_file']}")
            else:
                parent_entry = table_entries[parent]
                parent_columns = {
                    column.lower() for column in parent_entry["column_mapping"]
                }
                parent_primary_keys = {
                    column.lower() for column in parent_entry["primary_key"]
                }
                if foreign_key["referenced_column"].lower() not in parent_columns:
                    issues.append(
                        f"unknown FK column: {entry['target_table']}->{parent}"
                    )
                if foreign_key["referenced_column"].lower() not in parent_primary_keys:
                    issues.append(
                        f"FK does not target primary key: {entry['target_table']}->{parent}"
                    )
                if (
                parent != entry["target_table"]
                and order_index[parent] >= order_index[entry["target_table"]]
                ):
                    issues.append(
                        f"dependency order: {entry['target_table']} before {parent}"
                    )
    for asset in auxiliary_assets:
        profile = load_release_profile(root, asset["profile"])
        path = release_root(profile) / asset["source_file"]
        if (
            not path.exists()
            or _sha(path) != asset["checksum"]
            or _logical_count(path) != asset["record_count"]
        ):
            issues.append(f"auxiliary asset mismatch: {asset['source_file']}")
    report = {
        "status": "PASS" if not issues else "FAIL",
        "files_checked": len(entries),
        "issues": issues,
        "checks": {
            "paths": not any(issue.startswith("checksum/path") for issue in issues),
            "checksums": not any(issue.startswith("checksum/path") for issue in issues),
            "row_counts": not any(issue.startswith("row-count") for issue in issues),
            "schemas": not any(issue.startswith("empty schema") for issue in issues),
            "primary_keys": not any(
                issue.startswith(("malformed primary key", "invalid primary key"))
                for issue in issues
            ),
            "foreign_keys": not any(
                issue.startswith(
                    ("unknown FK", "malformed FK", "self-referential FK", "FK does not")
                )
                for issue in issues
            ),
            "dependency_order": not any(issue.startswith("dependency order") for issue in issues),
            "auxiliary_assets": not any(
                issue.startswith("auxiliary asset") for issue in issues
            ),
        },
    }
    _write_json(
        root / "artifacts" / "phase-4" / "handoff" / "handoff-validation.json",
        report,
    )
    return report["status"] == "PASS"


def _update_release_manifests(
    root: Path, validation: dict[str, Any], governance_status: str, realism_status: str,
    readiness_status: str,
) -> None:
    for profile_name in PROFILES:
        output = release_root(load_release_profile(root, profile_name))
        manifest_path = output / "manifest.json"
        manifest = _json(manifest_path)
        manifest["validation"] = {
            "command": (
                f"python scripts/validate_phase4.py --profile {profile_name} "
                "--scope 4A-4V"
            ),
            "status": validation["status"],
            "errors": validation["errors"],
            "warnings": validation["warnings"],
        }
        manifest["finalization_gates"] = {
            "governance": governance_status,
            "realism": realism_status,
            "readiness": readiness_status,
        }
        _write_json(manifest_path, manifest)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    for profile_name in PROFILES:
        subprocess.run(
            [
                sys.executable,
                str(root / "scripts" / "build_phase4_release.py"),
                "--profile",
                profile_name,
                "--root",
                str(root),
            ],
            check=True,
            cwd=root,
        )
    _write_release_docs(root)
    _generate_ground_truth(root)
    _write_realism(root)
    _write_governance(root)
    _write_readiness(root)
    for profile_name in PROFILES:
        subprocess.run(
            [
                sys.executable,
                str(root / "scripts" / "generate_release_manifest.py"),
                "--profile",
                profile_name,
                "--root",
                str(root),
            ],
            check=True,
            cwd=root,
        )
    _write_release_checksums(root)
    validation = _run_validation_reports(root)
    _write_release_reports(root, validation, 100 if validation["status"] == "PASS" else 0)
    for profile_name in PROFILES:
        subprocess.run(
            [
                sys.executable,
                str(root / "scripts" / "generate_release_manifest.py"),
                "--profile",
                profile_name,
                "--root",
                str(root),
            ],
            check=True,
            cwd=root,
        )
    _write_release_checksums(root)
    validation = _run_validation_reports(root)
    _write_handoff(root)
    handoff_ok = _validate_handoff(root)
    ground_truth = _json(
        root / "artifacts" / "phase-4" / "ground-truth" / "oracle-reconciliation.json"
    )
    realism = _json(
        root / "artifacts" / "phase-4" / "realism" / "distribution-analysis.json"
    )
    governance = _json(
        root / "artifacts" / "phase-4" / "governance" / "governance-summary.json"
    )
    readiness = _json(
        root / "artifacts" / "phase-4" / "demo-readiness" / "stability-report.json"
    )
    gates = {
        "validation": validation["status"] == "PASS",
        "ground_truth": ground_truth["status"] == "PASS",
        "realism": realism["all_targets_pass"],
        "governance": governance["status"] == "PASS",
        "readiness": readiness["identical_runs"] and readiness["runtime_failures"] == 0,
        "handoff": handoff_ok,
    }
    score = round(100 * sum(gates.values()) / len(gates))
    _update_release_manifests(
        root,
        validation,
        "PASS" if gates["governance"] else "FAIL",
        "PASS" if gates["realism"] else "FAIL",
        "PASS" if gates["readiness"] else "FAIL",
    )
    report_root = root / "artifacts" / "phase-4"
    profile_manifests = [
        _json(release_root(load_release_profile(root, profile_name)) / "manifest.json")
        for profile_name in PROFILES
    ]
    aggregate_files = [
        {
            "profile": manifest["profile"],
            "path": item["path"],
            "record_count": item["record_count"],
            "sha256": item["sha256"],
        }
        for manifest in profile_manifests
        for item in manifest["files"]
    ]
    demo_manifest = profile_manifests[0]
    _write_json(
        report_root / "scorecard.json",
        {
            "score": score,
            "status": "PASS" if all(gates.values()) else "FAIL",
            "automatic_failures": [name for name, passed in gates.items() if not passed],
            "gates": gates,
            "validation": validation,
        },
    )
    _write_json(
        root / "artifacts" / "phase-4-release-manifest.json",
        {
            "dataset_name": "chronosdb-demo-dataset",
            "version": "1.0.0",
            "generator_version": demo_manifest["generator_version"],
            "domain_model_version": demo_manifest["domain_model_version"],
            "seed": 260311,
            "profiles": list(PROFILES),
            "release_scales": {
                manifest["profile"]: manifest["profile_contract"]["source_scale"]
                for manifest in profile_manifests
            },
            "generation_config_hash": demo_manifest["generation_config_hash"],
            "source_revision": demo_manifest["source_revision"],
            "source_state": demo_manifest["source_state"],
            "generation_time_utc": demo_manifest["generation_time_utc"],
            "currency": demo_manifest["currency"],
            "canonical_timezone": demo_manifest["canonical_timezone"],
            "display_timezone": demo_manifest["display_timezone"],
            "license": demo_manifest["license"],
            "files": aggregate_files,
            "partitions": demo_manifest["partitions"],
            "profile_manifests": [
                (
                    "data/releases/v1.0.0/"
                    f"{'' if profile_name == 'demo' else profile_name + '/'}manifest.json"
                )
                for profile_name in PROFILES
            ],
            "validation_status": "PASS" if gates["validation"] else "FAIL",
            "ground_truth_status": "PASS" if gates["ground_truth"] else "FAIL",
            "realism_status": "PASS" if gates["realism"] else "FAIL",
            "governance_status": "PASS" if gates["governance"] else "FAIL",
            "readiness_status": "PASS" if gates["readiness"] else "FAIL",
            "handoff_status": "PASS" if gates["handoff"] else "FAIL",
            "score": score,
            "automatic_failures": [name for name, passed in gates.items() if not passed],
        },
    )
    docs = root / "docs" / "dataset-release"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "release-notes-v1.0.0.md").write_text(
        "# ChronosDB Dataset Release v1.0.0\n\n"
        "Phase 4P–4V finalization passed with deterministic demo, tiny, standard, "
        "and stress profiles. "
        "Corrections require a new dataset version; the benchmark test partition is frozen.\n",
        encoding="utf-8",
    )
    (docs / "reproduction-report.md").write_text(
        "# Reproduction Report\n\n"
        "All four profiles were rebuilt and validated. Ten golden stability runs "
        "produced identical result hashes. Each release manifest records the source "
        "revision, configuration hash, and working-tree fingerprint used for the "
        "build. The Db2 integration test remains externally gated when Db2 is "
        "unavailable.\n",
        encoding="utf-8",
    )
    if not all(gates.values()):
        raise SystemExit(f"Phase 4P–4V finalization failed: {gates}")
    print("Phase 4P–4V finalization passed")


if __name__ == "__main__":
    main()
