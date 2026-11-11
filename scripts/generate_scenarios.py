"""Generate Phase 3J scenario inputs and Phase 3K evidence corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data_generator.export import write_csv_rows, write_json
from data_generator.generator import generate_master, load_config
from data_generator.scenarios import (
    generate_documents,
    generate_scenarios,
    validate_documents,
    validate_scenarios,
)
from data_generator.validation import validate_master


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=("tiny", "standard", "stress"), default="standard")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    config = load_config(args.root, args.scale, args.seed)
    master = generate_master(config)
    validate_master(master)
    scenarios = generate_scenarios(config, master)
    validate_scenarios(scenarios)
    scenario_dir = args.root / "data" / "generated" / "scenarios"
    for name, rows in scenarios.items():
        if name in {"scenario_definitions", "scenario_constraints"}:
            write_json(scenario_dir / f"{name}.json", rows)
        else:
            write_csv_rows(scenario_dir / f"{name}.csv", rows)
    documents, relevance = generate_documents(config, master)
    validate_documents(documents)
    document_dir = args.root / "data" / "generated" / "documents"
    document_dir.mkdir(parents=True, exist_ok=True)
    metadata = [{key: value for key, value in row.items() if key != "text"} for row in documents]
    (document_dir / "document_metadata.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in metadata),
        encoding="utf-8",
    )
    (document_dir / "documents.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in documents),
        encoding="utf-8",
    )
    write_json(document_dir / "retrieval_relevance.json", relevance)
    scenario_count = len(scenarios["scenario_definitions"])
    print(f"Generated {scenario_count} scenarios and {len(documents)} documents")


if __name__ == "__main__":
    main()
