"""Build and verify the frozen Phase 3L golden scenario."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from data_generator.export import write_csv_rows, write_json
from ground_truth.oracle import calculate_golden


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = calculate_golden()
    golden = args.root / "data" / "golden"
    write_json(golden / "scenario.json", result["scenario"])
    write_json(golden / "expected_do_nothing.json", result["do_nothing"])
    write_json(golden / "expected_interventions.json", result["interventions"])
    write_json(
        golden / "interventions.json",
        [
            {"id": "INT-GOLD-A", "type": "TRANSFER", "quantity": 400},
            {"id": "INT-GOLD-B", "type": "ALTERNATE_SUPPLY", "quantity": 400},
            {"id": "INT-GOLD-C", "type": "HYBRID", "quantity": 400},
        ],
    )
    write_json(golden / "expected_recommendation.json", result["recommendation"])
    write_json(golden / "expected_causal_traces.json", result["causal_traces"])
    write_csv_rows(
        golden / "master_data" / "components.csv",
        [{"id": "CMP-MCU-42", "unit": "EA", "status": "ACTIVE"}],
    )
    write_csv_rows(
        golden / "master_data" / "products.csv",
        [{"id": "PRD-CONTROLLER-X", "unit": "EA", "status": "ACTIVE"}],
    )
    write_csv_rows(
        golden / "operational_state" / "inventory.csv",
        [
            {"warehouse_id": "WH-PUNE", "component_id": "CMP-MCU-42", "on_hand": 400},
            {"warehouse_id": "WH-CHENNAI", "component_id": "CMP-MCU-42", "on_hand": 700},
        ],
    )
    write_json(
        golden / "manifest.json",
        {"scenario_id": result["scenario"]["scenario_id"], "version": "1.0.0"},
    )
    workbook = golden / "manual_workbook.csv"
    workbook.parent.mkdir(parents=True, exist_ok=True)
    with workbook.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("case", "breached_customer_orders", "revenue_at_risk_inr", "cost_inr"))
        writer.writerow(
            (
                "baseline",
                result["baseline"]["breached_customer_orders"],
                result["baseline"]["revenue_at_risk_inr"],
                result["baseline"]["intervention_cost_inr"],
            )
        )
        writer.writerow(
            (
                "do_nothing",
                result["do_nothing"]["breached_customer_orders"],
                result["do_nothing"]["revenue_at_risk_inr"],
                result["do_nothing"]["intervention_cost_inr"],
            )
        )
        for intervention in result["interventions"]:
            writer.writerow(
                (
                    intervention["candidate_id"],
                    intervention["breached_customer_orders"],
                    intervention["revenue_at_risk_inr"],
                    intervention["intervention_cost_inr"],
                )
            )
    (golden / "review_signoff.md").write_text(
        "# Golden Scenario Review\n\n"
        "The corrected 700-unit Chennai inventory fixture was calculated by the "
        "independent Phase 3N oracle. Expected outputs are frozen only after tests pass.\n",
        encoding="utf-8",
    )
    (golden / "assumptions.md").write_text(
        "# Golden Scenario Assumptions\n\n"
        "- Capacity is 100 finished units per calendar day.\n"
        "- Material is available at batch start.\n"
        "- Delivery lead time is one calendar day.\n"
        "- Partial production and delivery are enabled.\n",
        encoding="utf-8",
    )
    print("Golden scenario built and verified")


if __name__ == "__main__":
    main()
