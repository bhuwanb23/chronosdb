from __future__ import annotations

import csv
from pathlib import Path

from data_generator.phase4_validation import validate_interventions_release

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "releases" / "v1.0.0"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_intervention_capabilities_enforce_golden_constraints() -> None:
    interventions = {
        "transfers": _rows(RELEASE / "interventions" / "transfer_capabilities.csv"),
        "expedites": _rows(RELEASE / "interventions" / "expedite_capabilities.csv"),
        "alternates": _rows(
            RELEASE / "interventions" / "alternate_supply_capabilities.csv"
        ),
        "rescheduling": _rows(
            RELEASE / "interventions" / "rescheduling_constraints.csv"
        ),
        "costs": _rows(
            RELEASE / "interventions" / "intervention_cost_parameters.csv"
        ),
    }
    validate_interventions_release(interventions)
    assert next(
        row for row in interventions["transfers"] if row["id"] == "INT-GOLD-TRANSFER-500"
    )["feasibility_status"] == "INFEASIBLE"
