"""Run the complete Phase 3P–3R validation gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data_generator.privacy import render_privacy_markdown, scan_documents
from data_generator.release_validation import (
    build_validation_report,
    render_validation_markdown,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    validation = build_validation_report(root)
    privacy = scan_documents(root)
    (artifacts / "data-validation-report.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (artifacts / "data-validation-report.md").write_text(
        render_validation_markdown(validation),
        encoding="utf-8",
    )
    (artifacts / "privacy-review.json").write_text(
        json.dumps(privacy, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / "docs" / "data" / "privacy-and-licensing-review.md").write_text(
        render_privacy_markdown(privacy),
        encoding="utf-8",
    )
    if validation["summary"]["validation_errors"] or validation["summary"]["warnings"]:
        raise SystemExit("Phase 3P validation failed")
    if privacy["status"] != "PASS":
        raise SystemExit("Phase 3R privacy validation failed")
    print("Phase 3P–3R release validation passed")


if __name__ == "__main__":
    main()
