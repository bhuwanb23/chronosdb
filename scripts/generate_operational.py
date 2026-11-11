"""Generate Phase 3H and 3I operational/history data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data_generator.export import write_csv_rows
from data_generator.generator import ENTITY_FILES, generate_master, load_config, write_master
from data_generator.operational import generate_history, generate_operational
from data_generator.validation import validate_master, validate_operational


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=("tiny", "standard", "stress"), default="tiny")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    config = load_config(args.root, args.scale, args.seed)
    master = generate_master(config)
    validate_master(master)
    write_master(config, master)
    operational = generate_operational(config, master)
    validate_operational(master, operational)
    history = generate_history(config, master, operational)
    generated = []
    operation_root = args.root / "data" / "generated" / "operational" / args.scale
    history_root = args.root / "data" / "generated" / "history" / args.scale
    for name, rows in operational.items():
        generated.append(
            write_csv_rows(
                operation_root / f"{name}.csv",
                rows,
            )
        )
    for name, rows in history.items():
        generated.append(
            write_csv_rows(
                history_root / f"{name}.csv",
                rows,
            )
        )
    manifest = {
        "dataset_version": config.dataset_version,
        "scale": config.scale,
        "seed": config.seed,
        "layer": "operational_and_history",
        "files": generated,
        "master_entities": ENTITY_FILES,
    }
    manifest_path = operation_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Generated operational and history data for {args.scale}")


if __name__ == "__main__":
    main()
