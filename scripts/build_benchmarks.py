"""Build Phase 3M benchmark scenarios and independent expected envelopes."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_generator.export import write_json
from data_generator.generator import generate_master, load_config
from data_generator.scenarios import generate_scenarios
from ground_truth.benchmarks import build_partitions, expected_for_scenario


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=("tiny", "standard", "stress"), default="standard")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    config = load_config(args.root, args.scale)
    scenarios = generate_scenarios(config, generate_master(config))["scenario_definitions"]
    benchmark_dir = args.root / "data" / "benchmarks"
    write_json(benchmark_dir / "scenarios.json", scenarios)
    expected = [expected_for_scenario(scenario) for scenario in scenarios]
    write_json(benchmark_dir / "expected.json", expected)
    partitions = build_partitions([scenario["id"] for scenario in scenarios])
    partitions["review_holdout"] = [scenario["id"] for scenario in scenarios[57:60]]
    write_json(benchmark_dir / "partitions.json", partitions)
    write_json(
        benchmark_dir / "benchmark_manifest.json",
        {
            "dataset_version": config.dataset_version,
            "scenario_count": len(scenarios),
            "expected_output_count": len(expected),
            "partitions": {key: len(value) for key, value in partitions.items()},
        },
    )
    print(f"Built {len(scenarios)} benchmark scenarios")


if __name__ == "__main__":
    main()
