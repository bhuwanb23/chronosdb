from __future__ import annotations

import csv
import json
from pathlib import Path

from data_generator.phase4_validation import (
    validate_benchmark_release,
    validate_supporting_demos_release,
)

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "releases" / "v1.0.0"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_benchmark_has_frozen_partitions_and_balance() -> None:
    benchmark_root = RELEASE / "benchmarks"
    benchmark = {
        "scenarios": [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((benchmark_root / "scenarios").glob("*.json"))
        ],
        "expected": [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((benchmark_root / "expected").glob("*.json"))
        ],
        "difficulty_labels": _rows(benchmark_root / "difficulty_labels.csv"),
        "partition_manifest": json.loads(
            (benchmark_root / "partition_manifest.json").read_text(encoding="utf-8")
        ),
    }
    validate_benchmark_release(benchmark)
    assert len(benchmark["scenarios"]) == 60


def test_supporting_demo_set_is_complete() -> None:
    demo_root = RELEASE / "demo-scenarios"
    demos = {
        "scenarios": [
            json.loads(path.read_text(encoding="utf-8"))["scenario"]
            for path in sorted(demo_root.glob("DEMO-*.json"))
        ],
        "catalogue": _rows(demo_root / "scenario_catalogue.csv"),
    }
    validate_supporting_demos_release(demos)
