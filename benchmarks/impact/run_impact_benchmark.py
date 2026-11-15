#!/usr/bin/env python3
"""Run the Phase 5 impact benchmark and freeze its evidence artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.run_impact_benchmarks import run

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = run(args.root)
    print(f"Impact benchmark result: {result['result_hash']}")


if __name__ == "__main__":
    main()
