from __future__ import annotations

import json
from pathlib import Path

import pytest

from chronosdb.simulation.counterfactual import (
    Overlay,
    Phase6Engine,
    ScenarioLedger,
    SimulationValidationError,
    load_golden_overlays,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def engine() -> Phase6Engine:
    return Phase6Engine(ROOT)


@pytest.fixture(scope="module")
def golden() -> dict[str, tuple[Overlay, ...]]:
    return load_golden_overlays(ROOT / "data" / "golden" / "phase6-overlays.json")


def test_baseline_is_the_frozen_phase5_result(engine: Phase6Engine) -> None:
    artifact = json.loads(
        (ROOT / "artifacts" / "phase-5" / "golden-impact-result.json").read_text(
            encoding="utf-8"
        )
    )
    baseline = engine.baseline()
    assert baseline.result_hash == artifact["result_hash"]
    assert baseline.input_state_hash == artifact["input_state_hash"]
    assert baseline.headline_metrics["revenue_at_risk"] == {
        "amount": "1600000.00",
        "currency": "INR",
    }
    assert baseline.headline_metrics["sla_breached_customer_order_count"] == 2


def test_every_golden_intervention_reduces_or_preserves_baseline_risk(
    engine: Phase6Engine, golden: dict[str, tuple[Overlay, ...]]
) -> None:
    expected = json.loads(
        (ROOT / "data" / "golden" / "phase6-expected.json").read_text(encoding="utf-8")
    )
    for name, overlays in golden.items():
        result = engine.run(overlays)
        assert result.status in {"COMPLETED", "PARTIALLY_COMPLETED"}
        assert result.delta["revenue_protected"] == expected[name]["revenue_protected"]
        assert result.delta["breaches_avoided"] == expected[name]["breaches_avoided"]
        assert result.delta["delay_reduction_hours"] == expected[name][
            "delay_reduction_hours"
        ]
        assert result.intervention_cost == expected[name]["intervention_cost"]


def test_baseline_records_are_not_mutated_by_simulations(
    engine: Phase6Engine, golden: dict[str, tuple[Overlay, ...]]
) -> None:
    before = json.dumps(
        {name: [dict(row) for row in rows] for name, rows in engine.state.records.items()},
        sort_keys=True,
    )
    for overlays in golden.values():
        engine.run(overlays)
    after = json.dumps(
        {name: [dict(row) for row in rows] for name, rows in engine.state.records.items()},
        sort_keys=True,
    )
    assert before == after


def test_result_hash_is_stable_across_runs(
    engine: Phase6Engine, golden: dict[str, tuple[Overlay, ...]]
) -> None:
    first = engine.run(golden["transfer"])
    second = engine.run(golden["transfer"])
    assert first.result_hash == second.result_hash
    assert first.delta == second.delta
    assert first.simulation_run_id == second.simulation_run_id


def test_result_hash_is_stable_across_engine_instances(
    golden: dict[str, tuple[Overlay, ...]]
) -> None:
    first = Phase6Engine(ROOT).run(golden["hybrid"])
    second = Phase6Engine(ROOT).run(golden["hybrid"])
    assert first.result_hash == second.result_hash


@pytest.mark.parametrize(
    "overlay",
    [
        Overlay(
            "BAD-QTY",
            "TRANSFER_INVENTORY",
            {
                "component_id": "CMP-MCU-42",
                "quantity": "-5",
                "from_warehouse": "WH-CHENNAI",
                "to_warehouse": "WH-PUNE",
            },
        ),
        Overlay(
            "BAD-STOCK",
            "TRANSFER_INVENTORY",
            {
                "component_id": "CMP-MCU-42",
                "quantity": "999999",
                "from_warehouse": "WH-CHENNAI",
                "to_warehouse": "WH-PUNE",
            },
        ),
        Overlay(
            "BAD-SUPPLIER",
            "ALTERNATE_SUPPLIER",
            {
                "supplier_id": "SUP-UNKNOWN",
                "component_id": "CMP-MCU-42",
                "available_quantity": "10",
            },
        ),
        Overlay(
            "BAD-PO",
            "EXPEDITE_PO",
            {"purchase_order_id": "PO-UNKNOWN", "lead_time_reduction_days": 5},
        ),
        Overlay(
            "BAD-PRIORITY",
            "RESCHEDULE_PRODUCTION",
            {"production_order_id": "MO-0882", "priority": "URGENT"},
        ),
    ],
)
def test_infeasible_overlays_are_rejected(
    engine: Phase6Engine, overlay: Overlay
) -> None:
    with pytest.raises(SimulationValidationError):
        engine.run((overlay,))


def test_duplicate_and_conflicting_overlays_are_rejected(
    engine: Phase6Engine, golden: dict[str, tuple[Overlay, ...]]
) -> None:
    transfer = golden["transfer"][0]
    duplicate = Overlay(transfer.overlay_id, transfer.action, transfer.parameters)
    with pytest.raises(SimulationValidationError):
        engine.run((transfer, duplicate))
    conflicting = Overlay("OTHER", "TRANSFER_INVENTORY", transfer.parameters)
    with pytest.raises(SimulationValidationError):
        engine.run((transfer, conflicting))
    with pytest.raises(SimulationValidationError):
        engine.run((Overlay("BROKEN", "UNKNOWN_ACTION", {}),))


def test_safety_stock_and_missing_agreement_are_rejected(engine: Phase6Engine) -> None:
    with pytest.raises(SimulationValidationError):
        engine.run(
            (
                Overlay(
                    "SAFETY",
                    "TRANSFER_INVENTORY",
                    {
                        "component_id": "CMP-MCU-42",
                        "quantity": "581",
                        "from_warehouse": "WH-CHENNAI",
                        "to_warehouse": "WH-PUNE",
                    },
                ),
            )
        )
    with pytest.raises(SimulationValidationError):
        engine.run(
            (
                Overlay(
                    "EXPIRED",
                    "ALTERNATE_SUPPLIER",
                    {
                        "supplier_id": "SUP-0104",
                        "component_id": "CMP-P4-0002",
                        "available_quantity": "10",
                    },
                ),
            )
        )


def test_ledger_persists_one_record_per_run(
    engine: Phase6Engine,
    golden: dict[str, tuple[Overlay, ...]],
    tmp_path: Path,
) -> None:
    ledger = ScenarioLedger(tmp_path / "ledger.jsonl")
    for overlays in golden.values():
        engine.run(overlays, ledger=ledger)
    records = [
        json.loads(line)
        for line in (tmp_path / "ledger.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(records) == len(golden)
    assert all(record["result_hash"] for record in records)
    assert all(record["baseline_run_id"] for record in records)
    assert all("runtime_ms" in record for record in records)
