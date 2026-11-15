#!/usr/bin/env python3
"""Compare the frozen golden impact result with Phase 4 ground truth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def compare(root: Path) -> dict[str, Any]:
    result = _read(root / "artifacts" / "phase-5" / "golden-impact-result.json")
    expected = _read(root / "data" / "golden" / "expected_do_nothing.json")
    expected_lines = {
        line["customer_order_id"]: line for line in expected["customer_lines"]
    }
    actual_lines = {
        line["customer_order_id"]: line
        for line in result["provenance"]["customer_line_results"]
    }
    checks = {
        "breached_customer_orders": (
            result["headline_metrics"]["breached_customer_order_count"]
            == expected["breached_customer_orders"]
        ),
        "late_quantity": (
            result["headline_metrics"]["late_quantity"]
            == str(sum(line["late_quantity"] for line in expected["customer_lines"]))
        ),
        "total_delay_hours": (
            result["headline_metrics"]["total_delay_unit_hours"]
            == str(expected["total_delay_hours"])
        ),
        "revenue_at_risk": (
            result["headline_metrics"]["revenue_at_risk"]["amount"]
            == expected["revenue_at_risk_inr"]
        ),
        "customer_line_count": set(actual_lines) == set(expected_lines),
        "customer_line_values": all(
            actual_lines[order_id]["late_quantity"]
            == str(expected_lines[order_id]["late_quantity"])
            and actual_lines[order_id]["delay_hours"]
            == expected_lines[order_id]["delay_hours"]
            and actual_lines[order_id]["projected_delivery"]
            == expected_lines[order_id]["projected_delivery"]
            and actual_lines[order_id]["promised_delivery"]
            == expected_lines[order_id]["promised_delivery"]
            for order_id in expected_lines
        ),
        "attribution": {
            actual_lines[order_id]["attribution"]
            for order_id in expected_lines
            if expected_lines[order_id]["late_quantity"] > 0
        }
        == {"DISRUPTION_CAUSED"},
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    report = {
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "failed": failed,
        "result_hash": result.get("result_hash"),
    }
    output = root / "artifacts" / "phase-5" / "ground-truth-comparison.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    report = compare(args.root)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
