"""Calculate the Phase 3T score and release-blocking gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from ground_truth.oracle import calculate_golden
from ground_truth.quality_score import calculate_quality_score

SOURCE_PATHS = (
    Path("src"),
    Path("scripts"),
    Path("config"),
    Path("schemas"),
    Path("validation"),
    Path("Makefile"),
    Path("pyproject.toml"),
)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    paths = [
        path
        for relative in SOURCE_PATHS
        for path in (
            [root / relative] if (root / relative).is_file() else (root / relative).rglob("*")
        )
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    ]
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _packaging_status(root: Path) -> dict[str, Any]:
    checksum_path = root / "data" / "checksums.sha256"
    if not checksum_path.exists():
        return {"checksum_mismatches": ["data/checksums.sha256"], "nondeterministic_files": []}
    package_roots = (
        root / "data",
        root / "artifacts",
        root / "docs" / "data",
    )
    expected_paths = {
        path.relative_to(root).as_posix()
        for directory in package_roots
        if directory.exists()
        for path in directory.rglob("*")
        if path.is_file() and path.name != "checksums.sha256"
    }
    manifest_path = root / "data" / "manifest.json"
    manifest = _json(manifest_path) if manifest_path.exists() else {}
    manifest_paths = (
        {row["path"] for row in manifest.get("files", [])} | {"data/manifest.json"}
        if manifest_path.exists()
        else set()
    )
    listed_paths: set[str] = set()
    mismatches: list[str] = []
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", maxsplit=1)
        listed_paths.add(relative)
        path = root / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
        if actual != expected:
            mismatches.append(relative)
    mismatches.extend(sorted(expected_paths - listed_paths))
    mismatches.extend(sorted(listed_paths - expected_paths))
    mismatches.extend(sorted(manifest_paths - listed_paths))
    mismatches.extend(sorted(listed_paths - manifest_paths))
    for entry in manifest.get("files", []):
        path = root / entry["path"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
        if actual != entry.get("sha256"):
            mismatches.append(f"manifest:{entry['path']}")
    release_manifest_path = root / "artifacts" / "phase-3-release-manifest.json"
    if release_manifest_path.exists():
        recorded_source_hash = _json(release_manifest_path).get("source_tree_hash")
        if recorded_source_hash != _source_tree_hash(root):
            mismatches.append("source_tree_hash")
    reproducibility_path = root / "artifacts" / "reproducibility.json"
    nondeterministic = (
        _json(reproducibility_path).get("nondeterministic_files", [])
        if reproducibility_path.exists()
        else ["artifacts/reproducibility.json"]
    )
    return {
        "checksum_mismatches": sorted(set(mismatches)),
        "nondeterministic_files": nondeterministic,
    }


def _benchmark_status(root: Path) -> dict[str, Any]:
    expected = _json(root / "data" / "benchmarks" / "expected.json")
    complete = len(expected) == 60
    provenance_complete = all(
        {
            "scenario_id",
            "formula_version",
            "oracle_version",
            "reference_case",
            "unit",
        }.issubset(row.get("provenance", {}))
        for row in expected
    )
    infeasible = [
        row["scenario_id"]
        for row in expected
        if row.get("expected_recommendation")
        and not row.get("expected_candidate_feasibility", {}).get(
            row["expected_recommendation"],
            False,
        )
    ]
    golden = calculate_golden()
    golden_match = (
        _json(root / "data" / "golden" / "expected_do_nothing.json") == golden["do_nothing"]
        and _json(root / "data" / "golden" / "expected_interventions.json")
        == golden["interventions"]
        and _json(root / "data" / "golden" / "expected_recommendation.json")
        == golden["recommendation"]
    )
    return {
        "complete": complete,
        "provenance_complete": provenance_complete,
        "missing_expected_outputs": not complete,
        "infeasible_recommendations": infeasible,
        "golden_match": golden_match,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root
    validation = _json(root / "artifacts" / "data-validation-report.json")
    statistics = _json(root / "artifacts" / "dataset-statistics.json")
    privacy = _json(root / "artifacts" / "privacy-review.json")
    benchmark = _benchmark_status(root)
    packaging = _packaging_status(root)
    score = calculate_quality_score(validation, statistics, privacy, benchmark, packaging)
    (root / "artifacts" / "ground-truth-review.json").write_text(
        json.dumps(benchmark, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / "artifacts" / "phase-3-quality-score.json").write_text(
        json.dumps(score, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Phase 3 score: {score['score']}/100 ({score['status']})")
    if score["status"] != "PASS":
        raise SystemExit("Phase 3 quality gate failed")


if __name__ == "__main__":
    main()
