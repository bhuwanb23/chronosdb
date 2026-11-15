#!/usr/bin/env python3
"""Phase 15H: load ChronosDB seed data into Db2.

The seed SQL files are intentionally small, reviewable fixtures generated
from the frozen release. Use --dry-run on machines without a Db2 client.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "sql" / "seeds"
DATASETS = (
    "suppliers",
    "components",
    "inventory",
    "orders",
    "customer_orders",
    "production_orders",
    "scenarios",
    "historical_incidents",
    "policies",
    "sops",
)


def seed_files() -> list[Path]:
    return [SEED_DIR / f"{name}.sql" for name in DATASETS]


def validate_seed() -> list[str]:
    issues: list[str] = []
    for path in seed_files():
        if not path.exists():
            issues.append(f"missing seed file: {path.relative_to(ROOT)}")
        elif not path.read_text(encoding="utf-8").strip():
            issues.append(f"empty seed file: {path.relative_to(ROOT)}")
    return issues


def run_sql(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] db2 -tvf {path.relative_to(ROOT)}")
        return
    db2 = shutil.which("db2")
    if db2 is None:
        raise RuntimeError(
            "db2 CLI not found; install the Db2 client or use --dry-run"
        )
    subprocess.run([db2, "-tvf", str(path)], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    issues = validate_seed()
    if issues:
        print("Seed validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1
    print(f"Seed files present: {len(seed_files())}")
    if args.validate_only:
        print("Seed validation complete.")
        return 0

    for path in seed_files():
        print(f"Loading {path.stem}...")
        run_sql(path, args.dry_run)
    print("Dataset seeding complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
