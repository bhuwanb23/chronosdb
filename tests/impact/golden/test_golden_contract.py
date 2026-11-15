from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _read(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_golden_artifact_matches_frozen_customer_lines() -> None:
    result = _read("artifacts/phase-5/golden-impact-result.json")
    expected = _read("data/golden/expected_do_nothing.json")
    actual = {
        row["customer_order_id"]: row
        for row in result["provenance"]["customer_line_results"]
    }
    assert set(actual) == {row["customer_order_id"] for row in expected["customer_lines"]}
    for line in expected["customer_lines"]:
        row = actual[line["customer_order_id"]]
        assert row["late_quantity"] == str(line["late_quantity"])
        assert row["delay_hours"] == line["delay_hours"]
        assert row["projected_delivery"] == line["projected_delivery"]
        assert row["promised_delivery"] == line["promised_delivery"]
        assert Decimal(row["revenue_at_risk"]) == Decimal(
            line["revenue_at_risk_inr"]
        )


def test_golden_artifact_has_complete_metric_provenance() -> None:
    result = _read("artifacts/phase-5/golden-impact-result.json")
    provenance = result["provenance"]["metric_provenance"]
    for metric in (
        "late_quantity",
        "revenue_at_risk",
        "total_delay_unit_hours",
        "sla_breached_customer_order_count",
        "affected_purchase_order_count",
    ):
        assert metric in provenance
        assert provenance[metric]["rule_id"]
        assert provenance[metric]["rule_version"] == "impact-rules-v1.0.0"
        assert provenance[metric]["state_hash"] == result["input_state_hash"]


def test_golden_causal_traces_cover_both_breaches() -> None:
    result = _read("artifacts/phase-5/golden-impact-result.json")
    traces = result["causal_traces"]
    assert len(traces) == 2
    assert {trace["target"]["entity_id"] for trace in traces} == {
        "COL-CO-0704-01",
        "COL-CO-0711-01",
    }
    for trace in traces:
        assert trace["nodes"][0]["node_type"] == "DISRUPTION"
        assert trace["edges"][-1]["edge_type"] == "EXPOSES_REVENUE"
        assert trace["attribution"] == "DISRUPTION_CAUSED"
