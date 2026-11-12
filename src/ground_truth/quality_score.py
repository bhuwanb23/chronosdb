"""Phase 3T weighted quality score and automatic-failure gate."""

from __future__ import annotations

from typing import Any

WEIGHTS = {
    "domain_model_conformity": 15,
    "referential_and_temporal_integrity": 15,
    "generator_determinism": 12,
    "operational_realism": 10,
    "golden_scenario_correctness": 15,
    "benchmark_breadth": 10,
    "ground_truth_quality": 10,
    "evidence_corpus_quality": 5,
    "privacy_and_licensing": 4,
    "packaging_and_reproducibility": 4,
}


def automatic_failures(
    validation: dict[str, Any],
    privacy: dict[str, Any],
    benchmark: dict[str, Any],
    packaging: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    if validation["summary"]["validation_errors"]:
        failures.append("validation_errors")
    if validation["summary"]["warnings"]:
        failures.append("undocumented_warnings")
    if privacy["status"] != "PASS":
        failures.append("privacy_or_contamination")
    if benchmark.get("missing_expected_outputs"):
        failures.append("missing_expected_outputs")
    if benchmark.get("infeasible_recommendations"):
        failures.append("infeasible_recommendations")
    if packaging.get("checksum_mismatches"):
        failures.append("checksum_mismatches")
    if packaging.get("nondeterministic_files"):
        failures.append("nondeterministic_generation")
    return failures


def calculate_quality_score(
    validation: dict[str, Any],
    statistics: dict[str, Any],
    privacy: dict[str, Any],
    benchmark: dict[str, Any],
    packaging: dict[str, Any],
) -> dict[str, Any]:
    """Calculate the documented 100-point release score."""
    checks = {
        "domain_model_conformity": validation["summary"]["validation_errors"] == 0,
        "referential_and_temporal_integrity": validation["summary"]["validation_errors"] == 0,
        "generator_determinism": not packaging.get("nondeterministic_files"),
        "operational_realism": statistics["summary"]["errors"] == 0,
        "golden_scenario_correctness": benchmark.get("golden_match", False),
        "benchmark_breadth": benchmark.get("complete", False),
        "ground_truth_quality": benchmark.get("provenance_complete", False),
        "evidence_corpus_quality": privacy["counts"]["documents"] == 175,
        "privacy_and_licensing": privacy["status"] == "PASS",
        "packaging_and_reproducibility": not packaging.get("checksum_mismatches"),
    }
    categories = {
        category: weight if checks[category] else 0 for category, weight in WEIGHTS.items()
    }
    failures = automatic_failures(validation, privacy, benchmark, packaging)
    score = sum(categories.values())
    return {
        "score_version": "1.0.0",
        "phase": "3T",
        "weights": WEIGHTS,
        "category_scores": categories,
        "checks": checks,
        "score": score,
        "threshold": 95,
        "automatic_failures": failures,
        "status": "PASS" if score >= 95 and not failures else "FAIL",
    }
