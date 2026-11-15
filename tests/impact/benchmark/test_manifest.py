from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / "data" / "releases" / "v1.0.0"


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_partition_manifest_is_complete_and_disjoint() -> None:
    partitions = _json(RELEASE / "benchmarks" / "partition_manifest.json")[
        "exclusive_partitions"
    ]
    scenario_ids = [scenario for values in partitions.values() for scenario in values]
    assert len(scenario_ids) == 60
    assert len(set(scenario_ids)) == 60
    for scenario_id in scenario_ids:
        assert (RELEASE / "benchmarks" / "scenarios" / f"{scenario_id}.json").exists()
        assert (RELEASE / "benchmarks" / "expected" / f"{scenario_id}.json").exists()


def test_every_scenario_has_input_hash_and_do_nothing_result() -> None:
    hashes = {
        row["scenario_id"]: row
        for row in csv.DictReader(
            (ROOT / "artifacts" / "phase-4" / "ground-truth" / "scenario-input-hashes.csv")
            .open(encoding="utf-8", newline="")
        )
    }
    results = {
        row["scenario_id"]: row
        for row in (
            json.loads(line)
            for line in (
                ROOT / "artifacts" / "phase-4" / "ground-truth" / "expected-results.jsonl"
            )
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        )
    }
    assert set(hashes) == set(results)
    for scenario_id, row in results.items():
        assert hashes[scenario_id]["input_state_hash"] == row["input_state_hash"]
        assert row["do_nothing"]["candidate_type"] == "DO_NOTHING"


def test_benchmark_artifact_covers_all_scenarios() -> None:
    artifact = _json(ROOT / "artifacts" / "phase-5" / "impact-benchmark-results.json")
    assert artifact["benchmark_scenario_count"] == 60
    assert sum(artifact["partitions"].values()) == 60
    assert artifact["golden"]["targets_met"] is True
    assert artifact["runtime_expected_output_reads"] is False
