"""Phase 4N supporting demonstration scenarios."""

from __future__ import annotations

from typing import Any

from .release_export import write_release_csv, write_release_json
from .release_profile import ReleaseProfile, release_root

DEMO_CASES = (
    (
        "DEMO-002",
        "NO_IMPACT_OUTAGE",
        "MONITOR_NO_INTERVENTION",
        "Supply disruption detected; projected inventory covers all demand.",
    ),
    (
        "DEMO-003",
        "NO_FEASIBLE_RECOVERY",
        "NO_FEASIBLE_INTERVENTION",
        "No transferable stock, alternate supplier, or expedition path.",
    ),
    (
        "DEMO-004",
        "BUDGET_TRADE_OFF",
        "TRANSFER_ONLY_BUDGET_COMPLIANT",
        "Hybrid prevents all breaches but exceeds budget.",
    ),
    (
        "DEMO-005",
        "PRIORITY_CONFLICT",
        "PRIORITY_EXTERNALITY_VISIBLE",
        "Rescheduling protects one order while delaying a strategic customer.",
    ),
    (
        "DEMO-006",
        "INSUFFICIENT_DATA",
        "INSUFFICIENT_DATA",
        "Missing inventory snapshot must not be inferred as zero.",
    ),
    (
        "DEMO-007",
        "HISTORICAL_REPLAY",
        "HISTORICAL_REPLAY_DIFFERENCE_VISIBLE",
        "Late correction changes only the later scenario state.",
    ),
)


def build_supporting_demos(profile: ReleaseProfile) -> dict[str, list[dict[str, Any]]]:
    scenarios = [
        {
            "scenario_id": scenario_id,
            "scenario_type": scenario_type,
            "expected_outcome": expected,
            "description": description,
            "status": "FROZEN",
            "test_specific_branch": "false",
        }
        for scenario_id, scenario_type, expected, description in DEMO_CASES
    ]
    catalogue = [
        {
            "id": row["scenario_id"],
            "scenario_type": row["scenario_type"],
            "expected_outcome": row["expected_outcome"],
            "status": row["status"],
        }
        for row in scenarios
    ]
    output = release_root(profile) / "demo-scenarios"
    for scenario in scenarios:
        write_release_json(
            output / f"{scenario['scenario_id']}.json",
            {
                "scenario": scenario,
                "expected": {
                    "outcome": scenario["expected_outcome"],
                    "auditability": "REQUIRED",
                },
            },
        )
    write_release_csv(output / "scenario_catalogue.csv", catalogue)
    return {"scenarios": scenarios, "catalogue": catalogue}
