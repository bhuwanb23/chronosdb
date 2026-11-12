"""Phase 3P release validation and report construction."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .generator import ENTITY_FILES
from .scenarios import validate_documents, validate_scenarios
from .validation import (
    ValidationError,
    validate_master,
    validate_operational,
)

SCALES = ("tiny", "standard", "stress")
_SCHEMA_PROPERTIES: dict[str, Any] = {}
REQUIRED_HISTORY_FILES = (
    "entity_versions",
    "status_events",
    "daily_inventory_snapshots",
    "supplier_performance_history",
    "safety_stock_versions",
    "sla_versions",
    "supplier_delay_history",
    "production_history",
    "historical_disruptions",
    "late_arriving_corrections",
)
REQUIRED_OPERATIONAL_FILES = (
    "customer_orders",
    "customer_order_lines",
    "production_orders",
    "production_customer_allocations",
    "production_material_requirements",
    "purchase_orders",
    "inventory_transactions",
    "inventory_snapshots",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _issue(
    issues: list[dict[str, str]],
    severity: str,
    code: str,
    message: str,
    path: str,
) -> None:
    issues.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "path": path,
        }
    )


def _check_timestamps(
    rows: list[dict[str, str]],
    path: str,
    issues: list[dict[str, str]],
) -> None:
    timestamp_keys = {
        key
        for row in rows
        for key in row
        if key.endswith(("_time", "_at", "_from", "_to", "_date"))
    }
    for row_number, row in enumerate(rows, start=2):
        for key in timestamp_keys:
            value = row.get(key, "")
            if not value:
                continue
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                _issue(
                    issues,
                    "ERROR",
                    "SCHEMA_TIMESTAMP",
                    f"Invalid ISO-8601 timestamp in {key}",
                    f"{path}:{row_number}",
                )
                continue
            if parsed.tzinfo is None:
                _issue(
                    issues,
                    "ERROR",
                    "SCHEMA_TIMEZONE",
                    f"Timestamp {key} is missing an explicit timezone",
                    f"{path}:{row_number}",
                )


def _check_rows(
    rows: list[dict[str, str]],
    path: str,
    issues: list[dict[str, str]],
    required_fields: tuple[str, ...] = (),
) -> None:
    if not rows:
        _issue(issues, "ERROR", "SCHEMA_EMPTY", "File has no records", path)
        return
    fields = set(rows[0])
    for field in required_fields:
        if field not in fields:
            _issue(issues, "ERROR", "SCHEMA_FIELD", f"Missing required field {field}", path)
    for row_number, row in enumerate(rows, start=2):
        for field in required_fields:
            if not row.get(field):
                _issue(
                    issues,
                    "ERROR",
                    "SCHEMA_NULL",
                    f"Required field {field} is null or empty",
                    f"{path}:{row_number}",
                )
        for key, value in row.items():
            if not value or key in required_fields:
                continue
            rules = _SCHEMA_PROPERTIES.get(key, {})
            if rules.get("type") == "number":
                try:
                    float(value)
                except (TypeError, ValueError):
                    _issue(
                        issues,
                        "ERROR",
                        "SCHEMA_TYPE",
                        f"Field {key} is not numeric",
                        f"{path}:{row_number}",
                    )
            if "const" in rules and value != rules["const"]:
                _issue(
                    issues,
                    "ERROR",
                    "SCHEMA_ENUM",
                    f"Field {key} is not {rules['const']}",
                    f"{path}:{row_number}",
                )
            if any(
                token in key
                for token in (
                    "quantity",
                    "stock",
                    "capacity",
                    "cost",
                    "price",
                    "revenue",
                    "budget",
                    "premium",
                    "lead_time",
                )
            ):
                try:
                    if float(value) < 0:
                        _issue(
                            issues,
                            "ERROR",
                            "SCHEMA_MINIMUM",
                            f"Numeric field {key} is negative",
                            f"{path}:{row_number}",
                        )
                except ValueError:
                    _issue(
                        issues,
                        "ERROR",
                        "SCHEMA_NUMBER",
                        f"Numeric field {key} is not numeric",
                        f"{path}:{row_number}",
                    )
    _check_timestamps(rows, path, issues)


def _validate_history(root: Path, scale: str, issues: list[dict[str, str]]) -> None:
    history_dir = root / "data" / "generated" / "history" / scale
    for name in REQUIRED_HISTORY_FILES:
        path = history_dir / f"{name}.csv"
        if not path.exists():
            _issue(issues, "ERROR", "MISSING_FILE", "Missing history export", path.as_posix())
            continue
        rows = _read_csv(path)
        _check_rows(rows, path.as_posix(), issues, ("id",))
    corrections_path = history_dir / "late_arriving_corrections.csv"
    snapshots_path = history_dir / "daily_inventory_snapshots.csv"
    if not corrections_path.exists() or not snapshots_path.exists():
        return
    corrections = _read_csv(corrections_path)
    snapshots = {row.get("id"): row for row in _read_csv(snapshots_path)}
    for correction in corrections:
        snapshot = snapshots.get(correction.get("entity_id"))
        if snapshot is None:
            _issue(
                issues,
                "ERROR",
                "TEMPORAL_REFERENCE",
                "Late correction targets an unknown snapshot",
                corrections_path.as_posix(),
            )
            continue
        try:
            known_at = datetime.fromisoformat(correction["known_at"].replace("Z", "+00:00"))
            event_time = datetime.fromisoformat(correction["event_time"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            known_at = event_time = None
        if known_at is None or event_time is None or known_at <= event_time:
            _issue(
                issues,
                "ERROR",
                "TEMPORAL_BITEMPORAL_ORDER",
                "Late correction known_at must be after event_time",
                corrections_path.as_posix(),
            )
        try:
            correction_time = datetime.fromisoformat(
                correction["event_time"].replace("Z", "+00:00")
            )
            snapshot_time = datetime.fromisoformat(snapshot["snapshot_time"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            correction_time = snapshot_time = None
        if correction_time != snapshot_time:
            _issue(
                issues,
                "ERROR",
                "TEMPORAL_CORRECTION_TARGET",
                "Correction event time does not match target snapshot time",
                corrections_path.as_posix(),
            )


def _validate_benchmarks(root: Path, issues: list[dict[str, str]]) -> None:
    benchmark_dir = root / "data" / "benchmarks"
    expected_path = benchmark_dir / "expected.json"
    partitions_path = benchmark_dir / "partitions.json"
    if not expected_path.exists() or not partitions_path.exists():
        _issue(
            issues,
            "ERROR",
            "BENCHMARK_FILES",
            "Benchmark outputs are incomplete",
            benchmark_dir.as_posix(),
        )
        return
    expected = _read_json(expected_path)
    partitions = _read_json(partitions_path)
    if len(expected) != 60:
        _issue(
            issues,
            "ERROR",
            "BENCHMARK_COUNT",
            "Expected output count is not 60",
            expected_path.as_posix(),
        )
    scenario_ids = {row.get("scenario_id") for row in expected}
    partition_names = ("development", "validation", "test", "adversarial", "review_holdout")
    partition_ids = [
        scenario_id for name in partition_names for scenario_id in partitions.get(name, [])
    ]
    if len(partition_ids) != len(set(partition_ids)):
        _issue(
            issues,
            "ERROR",
            "BENCHMARK_PARTITION_OVERLAP",
            "Benchmark partitions overlap",
            partitions_path.as_posix(),
        )
    if set(partition_ids) != {f"SCN-{index:04d}" for index in range(1, 61)}:
        _issue(
            issues,
            "ERROR",
            "BENCHMARK_PARTITION_COVERAGE",
            "Benchmark partitions do not cover SCN-0001..SCN-0060",
            partitions_path.as_posix(),
        )
    for row in expected:
        provenance = row.get("provenance", {})
        if not isinstance(provenance, dict) or not {
            "scenario_id",
            "formula_version",
            "oracle_version",
            "reference_case",
            "unit",
        }.issubset(provenance):
            _issue(
                issues,
                "ERROR",
                "BENCHMARK_PROVENANCE",
                "Expected output has incomplete provenance",
                expected_path.as_posix(),
            )
        recommendation = row.get("expected_recommendation")
        feasibility = row.get("expected_candidate_feasibility", {})
        if recommendation is not None and not feasibility.get(recommendation, False):
            _issue(
                issues,
                "ERROR",
                "BENCHMARK_RECOMMENDATION",
                "Recommendation is infeasible",
                expected_path.as_posix(),
            )
    if scenario_ids != {f"SCN-{index:04d}" for index in range(1, 61)}:
        _issue(
            issues,
            "ERROR",
            "BENCHMARK_SCENARIO_COVERAGE",
            "Expected outputs do not cover all scenarios",
            expected_path.as_posix(),
        )


def _validate_scale(root: Path, scale: str, issues: list[dict[str, str]]) -> None:
    master_dir = root / "data" / "generated" / "master" / scale
    operation_dir = root / "data" / "generated" / "operational" / scale
    scenario_dir = root / "data" / "generated" / "scenarios" / scale
    document_dir = root / "data" / "generated" / "documents" / scale
    master: dict[str, list[dict[str, str]]] = {}
    if not master_dir.exists():
        _issue(
            issues,
            "ERROR",
            "MISSING_DIRECTORY",
            "Missing master directory",
            master_dir.as_posix(),
        )
    for entity in ENTITY_FILES:
        path = master_dir / f"{entity}.csv"
        if not path.exists():
            _issue(issues, "ERROR", "MISSING_FILE", "Missing master export", path.as_posix())
            continue
        master[entity] = _read_csv(path)
        _check_rows(master[entity], path.as_posix(), issues, ("id",))
    if master:
        try:
            validate_master(master)
        except ValidationError as error:
            _issue(issues, "ERROR", "DOMAIN_MASTER", str(error), master_dir.as_posix())
    operational: dict[str, list[dict[str, str]]] = {}
    for name in REQUIRED_OPERATIONAL_FILES:
        path = operation_dir / f"{name}.csv"
        if not path.exists():
            _issue(issues, "ERROR", "MISSING_FILE", "Missing operational export", path.as_posix())
            continue
        operational[name] = _read_csv(path)
        _check_rows(operational[name], path.as_posix(), issues, ("id",))
    if master and len(operational) == len(REQUIRED_OPERATIONAL_FILES):
        try:
            validate_operational(master, operational)
        except ValidationError as error:
            _issue(issues, "ERROR", "DOMAIN_OPERATIONAL", str(error), operation_dir.as_posix())
    _validate_history(root, scale, issues)
    definitions_path = scenario_dir / "scenario_definitions.json"
    if definitions_path.exists():
        payload = {
            "scenario_definitions": _read_json(definitions_path),
            "scenario_constraints": _read_json(scenario_dir / "scenario_constraints.json"),
            "disruptions": _read_csv(scenario_dir / "disruptions.csv"),
            "candidate_parameters": _read_csv(scenario_dir / "candidate_parameters.csv"),
            "intervention_costs": _read_csv(scenario_dir / "intervention_costs.csv"),
        }
        _check_rows(payload["scenario_definitions"], definitions_path.as_posix(), issues, ("id",))
        for name, required in (
            ("scenario_constraints", "scenario_id"),
            ("disruptions", "id"),
            ("candidate_parameters", "id"),
            ("intervention_costs", "candidate_id"),
        ):
            source = scenario_dir / (
                f"{name}.json" if name == "scenario_constraints" else f"{name}.csv"
            )
            _check_rows(payload[name], source.as_posix(), issues, (required,))
        try:
            validate_scenarios(payload, master or None)
        except (ValueError, StopIteration) as error:
            _issue(issues, "ERROR", "DOMAIN_SCENARIO", str(error), scenario_dir.as_posix())
    else:
        _issue(
            issues,
            "ERROR",
            "MISSING_FILE",
            "Missing scenario definitions",
            definitions_path.as_posix(),
        )
    documents_path = document_dir / "documents.jsonl"
    if documents_path.exists():
        documents = [
            json.loads(line)
            for line in documents_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        _check_rows(documents, documents_path.as_posix(), issues, ("document_id",))
        try:
            validate_documents(documents)
        except ValueError as error:
            _issue(issues, "ERROR", "EVIDENCE_CONTAMINATION", str(error), documents_path.as_posix())
    else:
        _issue(
            issues, "ERROR", "MISSING_FILE", "Missing evidence documents", documents_path.as_posix()
        )


def build_validation_report(root: Path, scales: tuple[str, ...] = SCALES) -> dict[str, Any]:
    """Run release-blocking checks and return a stable report payload."""
    global _SCHEMA_PROPERTIES
    issues: list[dict[str, str]] = []
    schema_path = root / "schemas" / "validation" / "phase3.json"
    if not schema_path.exists():
        _issue(
            issues,
            "ERROR",
            "SCHEMA_FILE",
            "Missing serialized schema contract",
            schema_path.as_posix(),
        )
        _SCHEMA_PROPERTIES = {}
    else:
        schema = _read_json(schema_path)
        _SCHEMA_PROPERTIES = schema.get("properties", {})
        if schema.get("type") != "object" or not schema.get("properties"):
            _issue(
                issues,
                "ERROR",
                "SCHEMA_DEFINITION",
                "Invalid serialized schema contract",
                schema_path.as_posix(),
            )
    for scale in scales:
        _validate_scale(root, scale, issues)
    _validate_benchmarks(root, issues)
    for relative in (
        "data/golden/expected_do_nothing.json",
        "data/golden/expected_interventions.json",
    ):
        if not (root / relative).exists():
            _issue(issues, "ERROR", "GOLDEN_FILES", "Missing frozen golden output", relative)
    counts = {
        severity: sum(issue["severity"] == severity for issue in issues)
        for severity in ("ERROR", "WARNING", "INFO")
    }
    return {
        "report_version": "1.0.0",
        "phase": "3P",
        "scales": list(scales),
        "summary": {
            "validation_errors": counts["ERROR"],
            "warnings": counts["WARNING"],
            "info": counts["INFO"],
            "status": "PASS" if counts["ERROR"] == 0 and counts["WARNING"] == 0 else "FAIL",
        },
        "issues": issues,
    }


def render_validation_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Phase 3P Data Validation Report",
        "",
        f"Status: **{summary['status']}**",
        "",
        f"- Validation errors: {summary['validation_errors']}",
        f"- Warnings: {summary['warnings']}",
        f"- Informational observations: {summary['info']}",
        "",
    ]
    if report["issues"]:
        lines.extend(
            ["## Findings", "", "| Severity | Code | Path | Message |", "|---|---|---|---|"]
        )
        lines.extend(
            f"| {issue['severity']} | {issue['code']} | `{issue['path']}` | {issue['message']} |"
            for issue in report["issues"]
        )
    else:
        lines.append("All Phase 3P validation levels passed.")
    return "\n".join(lines) + "\n"


def file_fingerprint(path: Path) -> str:
    """Return a stable SHA-256 fingerprint for release manifests."""
    return hashlib.sha256(path.read_bytes()).hexdigest()
