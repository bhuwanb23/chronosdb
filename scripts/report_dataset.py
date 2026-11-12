"""Emit Phase 3Q statistics and Phase 3R privacy reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data_generator.privacy import render_privacy_markdown, scan_documents
from data_generator.statistics import (
    build_statistics_report,
    render_statistics_markdown,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    statistics = build_statistics_report(root)
    privacy = scan_documents(root)
    (artifacts / "dataset-statistics.json").write_text(
        json.dumps(statistics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (artifacts / "dataset-statistics.md").write_text(
        render_statistics_markdown(statistics),
        encoding="utf-8",
    )
    (artifacts / "distribution-checks.json").write_text(
        json.dumps(statistics["distribution_checks"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (artifacts / "privacy-review.json").write_text(
        json.dumps(privacy, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / "docs" / "data").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "data" / "privacy-and-licensing-review.md").write_text(
        render_privacy_markdown(privacy),
        encoding="utf-8",
    )
    if statistics["summary"]["errors"] or privacy["status"] != "PASS":
        raise SystemExit("Phase 3Q/3R report contains release-blocking findings")
    print("Generated Phase 3Q statistics and Phase 3R privacy reports")


if __name__ == "__main__":
    main()
