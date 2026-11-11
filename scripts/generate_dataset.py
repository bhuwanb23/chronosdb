"""Generate a deterministic Phase 3 master dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_generator.generator import generate_master, load_config, write_master
from data_generator.validation import validate_master


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=("tiny", "standard", "stress"), default="standard")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    config = load_config(args.root, args.scale, args.seed)
    entities = generate_master(config)
    validate_master(entities)
    output = write_master(config, entities)
    print(f"Generated valid {args.scale} master dataset at {output}")


if __name__ == "__main__":
    main()
