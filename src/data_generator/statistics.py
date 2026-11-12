"""Dataset statistics and Phase 3Q realism checks."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from .scenarios import SCENARIO_CATEGORIES


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _numeric(rows: list[dict[str, str]], field: str) -> list[float]:
    return [float(row[field]) for row in rows if row.get(field, "") != ""]


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": round(mean(values), 4),
    }


def _scale_statistics(root: Path, scale: str) -> dict[str, Any]:
    master = root / "data" / "generated" / "master" / scale
    operation = root / "data" / "generated" / "operational" / scale
    scenarios = root / "data" / "generated" / "scenarios" / scale
    documents = root / "data" / "generated" / "documents" / scale
    agreements = _csv(master / "supplier_component_agreements.csv")
    components = _csv(master / "components.csv")
    boms = _csv(master / "bom_versions.csv")
    bom_lines = _csv(master / "bom_lines.csv")
    suppliers = _csv(master / "suppliers.csv")
    purchase_orders = _csv(operation / "purchase_orders.csv")
    production_orders = _csv(operation / "production_orders.csv")
    customer_lines = _csv(operation / "customer_order_lines.csv")
    definitions = _json(scenarios / "scenario_definitions.json")
    documents_rows = [
        json.loads(line)
        for line in (documents / "documents.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    agreements_per_component = Counter(row["component_id"] for row in agreements)
    components_per_bom = Counter(row["bom_version_id"] for row in bom_lines)
    scenario_categories = Counter(row["category"] for row in definitions)
    difficulty = Counter(row["difficulty"] for row in definitions)
    return {
        "scale": scale,
        "row_counts": {
            "suppliers": len(suppliers),
            "components": len(components),
            "supplier_component_agreements": len(agreements),
            "bom_versions": len(boms),
            "purchase_orders": len(purchase_orders),
            "production_orders": len(production_orders),
            "customer_order_lines": len(customer_lines),
            "documents": len(documents_rows),
        },
        "supply": {
            "suppliers_per_component": _summary(list(agreements_per_component.values())),
            "lead_time_days": _summary(_numeric(agreements, "lead_time_days")),
            "unit_price_inr": _summary(_numeric(agreements, "unit_price_inr")),
            "approval_share": round(
                sum(row["approval_status"] == "APPROVED" for row in agreements)
                / max(1, len(agreements)),
                4,
            ),
        },
        "product_structure": {
            "components_per_bom": _summary(list(components_per_bom.values())),
            "active_bom_count": sum(row["status"] == "ACTIVE" for row in boms),
            "critical_component_count": sum(
                row["component_id"]
                in {
                    component["id"]
                    for component in components
                    if component["criticality"] == "CRITICAL"
                }
                for row in bom_lines
            ),
        },
        "operations": {
            "customer_order_size": _summary(_numeric(customer_lines, "ordered_quantity")),
            "production_planned_quantity": _summary(
                _numeric(production_orders, "planned_quantity")
            ),
            "production_completed_share": round(
                sum(row["status"] == "COMPLETED" for row in production_orders)
                / max(1, len(production_orders)),
                4,
            ),
            "purchase_received_share": round(
                sum(float(row["received_quantity"]) > 0 for row in purchase_orders)
                / max(1, len(purchase_orders)),
                4,
            ),
        },
        "scenarios": {
            "category_counts": dict(scenario_categories),
            "category_shares": {
                category: round(count / max(1, len(definitions)), 4)
                for category, count in scenario_categories.items()
            },
            "difficulty_counts": dict(difficulty),
            "document_status_counts": dict(Counter(row["status"] for row in documents_rows)),
            "document_confidentiality_counts": dict(
                Counter(row["confidentiality_class"] for row in documents_rows)
            ),
        },
    }


def distribution_checks(statistics: dict[str, Any]) -> list[dict[str, Any]]:
    """Compare frozen distributions with Phase 3Q targets."""
    observed = statistics["scenarios"]["category_counts"]
    expected = dict(SCENARIO_CATEGORIES)
    checks: list[dict[str, Any]] = []
    for category, target_count in expected.items():
        actual_count = observed.get(category, 0)
        checks.append(
            {
                "metric": f"scenario_category:{category}",
                "observed": actual_count,
                "target": target_count,
                "tolerance": 0,
                "status": "PASS" if actual_count == target_count else "ERROR",
            }
        )
    target_shares = {
        "NO_OPERATIONAL_IMPACT": 0.10,
        "NO_FEASIBLE_INTERVENTION": 0.05,
        "INSUFFICIENT_CRITICAL_DATA": 0.05,
    }
    shares = statistics["scenarios"]["category_shares"]
    for category, target in target_shares.items():
        actual = shares.get(category, 0.0)
        checks.append(
            {
                "metric": f"realism_target:{category}",
                "observed": actual,
                "target": target,
                "tolerance": 0.05,
                "status": "PASS" if actual >= target else "WARNING",
                "note": (
                    "Recommended realism target; frozen 60-scenario catalogue "
                    "remains authoritative."
                ),
            }
        )
    document_counts = statistics["scenarios"]["document_status_counts"]
    confidentiality = statistics["scenarios"]["document_confidentiality_counts"]
    for metric, actual, target in (
        ("expired_document_count", document_counts.get("EXPIRED", 0), 10),
        ("unauthorized_document_count", confidentiality.get("UNAUTHORIZED", 0), 10),
    ):
        checks.append(
            {
                "metric": metric,
                "observed": actual,
                "target": target,
                "tolerance": 0,
                "status": "PASS" if actual >= target else "ERROR",
            }
        )
    return checks


def build_statistics_report(
    root: Path, scales: tuple[str, ...] = ("tiny", "standard", "stress")
) -> dict[str, Any]:
    reports = [_scale_statistics(root, scale) for scale in scales]
    checks = distribution_checks(
        next(report for report in reports if report["scale"] == "standard")
    )
    return {
        "report_version": "1.0.0",
        "phase": "3Q",
        "scales": reports,
        "distribution_checks": checks,
        "summary": {
            "errors": sum(check["status"] == "ERROR" for check in checks),
            "warnings": sum(check["status"] == "WARNING" for check in checks),
            "status": "PASS" if all(check["status"] != "ERROR" for check in checks) else "FAIL",
        },
    }


def render_statistics_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 3Q Dataset Statistics",
        "",
        f"Status: **{report['summary']['status']}**",
        "",
        "## Distribution checks",
        "",
        "| Metric | Observed | Target | Tolerance | Status |",
        "|---|---:|---:|---:|---|",
    ]
    lines.extend(
        f"| {check['metric']} | {check['observed']} | {check['target']} | "
        f"{check['tolerance']} | {check['status']} |"
        for check in report["distribution_checks"]
    )
    return "\n".join(lines) + "\n"
