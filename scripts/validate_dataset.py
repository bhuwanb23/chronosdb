"""Validate an exported Phase 3 master dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_generator.validation import read_entities, validate_master


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    validate_master(read_entities(args.directory))
    print(f"Valid master dataset: {args.directory}")


if __name__ == "__main__":
    main()
