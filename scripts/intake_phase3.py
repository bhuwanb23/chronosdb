"""Phase 4A intake gate for the frozen Phase 3 release candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data_generator.release_validation import build_validation_report
from data_generator.privacy import scan_documents
from data_generator.release_profile import load_release_profile
from ground_truth.oracle import calculate_golden


REQUIRED_PATHS = (
    "config/enterprise.yaml",
    "config/generation.yaml",
    "config/scales/tiny.yaml",
    "config/scales/standard.yaml",
    "config/scales/stress.yaml",
    "src/data_generator",
    "src/ground_truth",
    "schemas",
    "tests/data_generator",
    "tests/ground_truth",
    "tests/invariants",
    "docs/data/DATASET_CARD.md",
    "data/manifest.json",
    "data/checksums.sha256",
    "artifacts/phase-3-quality-score.json",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root
    findings: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            findings.append(f"missing:{relative}")
    profile = load_release_profile(root, "demo")
    validation = build_validation_report(root)
    privacy = scan_documents(root)
    golden = calculate_golden()
    if validation["summary"]["validation_errors"] or validation["summary"]["warnings"]:
        findings.append("phase3_validation_failed")
    if privacy["status"] != "PASS":
        findings.append("phase3_privacy_failed")
    if golden["recommendation"]["recommended_intervention"] != "INT-GOLD-C":
        findings.append("golden_recommendation_mismatch")
    report = {
        "report_version": "1.0.0",
        "phase": "4A",
        "profile": profile.profile,
        "source_scale": profile.source_scale,
        "checks": {
            "required_paths": not any(item.startswith("missing:") for item in findings),
            "phase3_validation": validation["summary"]["status"] == "PASS",
            "privacy_and_contamination": privacy["status"] == "PASS",
            "independent_oracle": golden["recommendation"]["hard_constraints_satisfied"],
            "golden_outputs": golden["do_nothing"]["revenue_at_risk_inr"] == "1600000.00",
        },
        "findings": findings,
        "status": "PASS" if not findings else "FAIL",
    }
    output = root / "data" / "releases" / "v1.0.0" / "reports"
    output.mkdir(parents=True, exist_ok=True)
    (output / "phase-3-intake.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    docs = root / "docs" / "dataset-release"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "phase-3-intake-report.md").write_text(
        "# Phase 4A Phase 3 Release-Candidate Intake\n\n"
        f"Status: **{report['status']}**\n\n"
        + "\n".join(f"- {key}: {value}" for key, value in report["checks"].items())
        + ("\n\nNo intake findings were detected.\n" if not findings else f"\n\nFindings: {findings}\n"),
        encoding="utf-8",
    )
    if findings:
        raise SystemExit("Phase 4A intake failed")
    print("Phase 4A intake passed")


if __name__ == "__main__":
    main()
