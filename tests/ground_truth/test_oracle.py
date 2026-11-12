from __future__ import annotations

import csv
import json
from decimal import Decimal
from pathlib import Path

from ground_truth.oracle import calculate_golden

GOLDEN_DIR = Path(__file__).resolve().parents[2] / "data" / "golden"


def test_golden_outputs_are_locked() -> None:
    result = calculate_golden()
    assert result["do_nothing"]["breached_customer_orders"] == 2
    assert result["do_nothing"]["revenue_at_risk_inr"] == "1600000.00"
    hybrid = next(row for row in result["interventions"] if row["candidate_id"] == "INT-GOLD-C")
    assert hybrid["intervention_cost_inr"] == "132000"
    assert hybrid["breached_customer_orders"] == 0
    assert hybrid["revenue_protected_inr"] == "1600000.00"
    assert result["recommendation"]["recommended_intervention"] == "INT-GOLD-C"


def test_golden_costs_use_decimal_values() -> None:
    result = calculate_golden()
    hybrid = next(row for row in result["interventions"] if row["candidate_id"] == "INT-GOLD-C")
    assert Decimal(hybrid["intervention_cost_inr"]) <= Decimal("200000")


def test_frozen_golden_artifacts_match_oracle() -> None:
    """Independent path: frozen JSON must match a fresh oracle calculation."""
    result = calculate_golden()
    assert json.loads((GOLDEN_DIR / "expected_do_nothing.json").read_text(encoding="utf-8")) == (
        result["do_nothing"]
    )
    assert json.loads(
        (GOLDEN_DIR / "expected_interventions.json").read_text(encoding="utf-8")
    ) == result["interventions"]
    assert json.loads(
        (GOLDEN_DIR / "expected_recommendation.json").read_text(encoding="utf-8")
    ) == result["recommendation"]
    assert json.loads(
        (GOLDEN_DIR / "expected_causal_traces.json").read_text(encoding="utf-8")
    ) == result["causal_traces"]


def test_manual_workbook_matches_oracle() -> None:
    """Independent path: spreadsheet-style workbook rows must match the oracle."""
    result = calculate_golden()
    by_case = {
        row["case"]: row
        for row in csv.DictReader(
            (GOLDEN_DIR / "manual_workbook.csv").read_text(encoding="utf-8").splitlines()
        )
    }
    oracle_rows = {
        "baseline": result["baseline"],
        "do_nothing": result["do_nothing"],
        **{row["candidate_id"]: row for row in result["interventions"]},
    }
    for case, oracle in oracle_rows.items():
        workbook = by_case[case]
        assert int(workbook["breached_customer_orders"]) == oracle["breached_customer_orders"]
        assert workbook["revenue_at_risk_inr"] == oracle["revenue_at_risk_inr"]
        assert workbook["cost_inr"] == oracle["intervention_cost_inr"]
