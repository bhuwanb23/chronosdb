"""Generate Phase 3J scenario inputs and Phase 3K evidence corpus."""

from __future__ import annotations

import argparse
import hashlib
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


def _jsonl_manifest(path: Path, record_count: int) -> dict[str, object]:
    return {
        "path": path.as_posix(),
        "record_count": record_count,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


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
    validate_scenarios(scenarios, master)
    scenario_dir = args.root / "data" / "generated" / "scenarios" / args.scale
    manifest_files = []
    for name, rows in scenarios.items():
        if name in {"scenario_definitions", "scenario_constraints"}:
            manifest_files.append(write_json(scenario_dir / f"{name}.json", rows))
        else:
            manifest_files.append(write_csv_rows(scenario_dir / f"{name}.csv", rows))
    documents, relevance = generate_documents(config, master)
    validate_documents(documents)
    document_dir = args.root / "data" / "generated" / "documents" / args.scale
    document_dir.mkdir(parents=True, exist_ok=True)
    metadata = [{key: value for key, value in row.items() if key != "text"} for row in documents]
    metadata_path = document_dir / "document_metadata.jsonl"
    metadata_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in metadata),
        encoding="utf-8",
    )
    documents_path = document_dir / "documents.jsonl"
    documents_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in documents),
        encoding="utf-8",
    )
    manifest_files.extend(
        [
            _jsonl_manifest(metadata_path, len(metadata)),
            _jsonl_manifest(documents_path, len(documents)),
            write_json(document_dir / "retrieval_relevance.json", relevance),
        ]
    )
    write_json(
        scenario_dir / "manifest.json",
        {
            "dataset_version": config.dataset_version,
            "scale": args.scale,
            "layer": "scenarios_and_documents",
            "files": manifest_files,
        },
    )
    scenario_count = len(scenarios["scenario_definitions"])
    print(f"Generated {scenario_count} scenarios and {len(documents)} documents")


if __name__ == "__main__":
    main()
