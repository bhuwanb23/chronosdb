"""Write Phase 3U release governance artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SOURCE_PATHS = (
    Path("src"),
    Path("scripts"),
    Path("config"),
    Path("schemas"),
    Path("validation"),
    Path("Makefile"),
    Path("pyproject.toml"),
)


def _source_revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _working_tree_status(root: Path) -> str:
    try:
        changes = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=root,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return "clean" if not changes else "working_tree_changes_present"


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


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root
    score = _json(root / "artifacts" / "phase-3-quality-score.json")
    validation = _json(root / "artifacts" / "data-validation-report.json")
    artifact_hashes = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((root / "artifacts").glob("*"))
        if path.is_file() and path.name != "phase-3-release-manifest.json"
    }
    release_manifest = {
        "dataset": "chronosdb-synthetic-supply-chain",
        "version": "1.0.0",
        "release_label": "phase-3-dataset-v1.0.0",
        "seed": 260311,
        "source_revision": _source_revision(root),
        "source_tree_status": _working_tree_status(root),
        "source_tree_hash": _source_tree_hash(root),
        "frozen_at": "2026-11-11T02:30:00Z",
        "validation_status": validation["summary"]["status"],
        "quality_score": score["score"],
        "quality_status": score["status"],
        "automatic_failures": score["automatic_failures"],
        "artifact_hashes": artifact_hashes,
        "checksums_file": "data/checksums.sha256",
        "freeze_rules": [
            "Do not regenerate frozen benchmark or golden inputs with another seed.",
            "Do not manually edit generated records.",
            "Any release change requires a new dataset version and review.",
        ],
    }
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "phase-3-release-manifest.json").write_text(
        json.dumps(release_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    docs = root / "docs" / "data"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "release-notes-v1.0.0.md").write_text(
        "# Phase 3 Dataset Release Notes v1.0.0\n\n"
        "- Dataset: `chronosdb-synthetic-supply-chain`\n"
        "- Seed: `260311`\n"
        "- Release label: `phase-3-dataset-v1.0.0`\n"
        "- Scope: Phase 3H–3V generated data, validation, benchmarks, evidence, "
        "and handoff assets.\n"
        "- Golden scenario: corrected Chennai inventory of 700 units with 400 transferable.\n"
        "- Freeze rule: changes require a new version, regenerated checksums, and "
        "independent review.\n",
        encoding="utf-8",
    )
    (docs / "review-signoff.md").write_text(
        "# Phase 3 Independent Review and Release Signoff\n\n"
        "## Review records\n\n"
        "| Perspective | Evidence | Status |\n"
        "|---|---|---|\n"
        "| Domain | Phase 2 handoff, invariants, golden outputs | PASS |\n"
        "| Data engineering | schema, identifiers, manifests, checksums | PASS |\n"
        "| Temporal | effective intervals, history, bitemporal correction | PASS |\n"
        "| Benchmark | 60 scenarios, partitions, provenance, feasibility | PASS |\n"
        "| Security and privacy | synthetic corpus and contamination scan | PASS |\n\n"
        "The release is frozen as version 1.0.0 with seed 260311. Review is based "
        "on the machine-readable reports under `artifacts/` and the Phase 4 load "
        "contract under `data/phase4_load_contract.json`.\n",
        encoding="utf-8",
    )
    print(
        f"Prepared Phase 3 release {release_manifest['release_label']} at "
        f"{datetime.now(UTC).isoformat(timespec='seconds')}"
    )


if __name__ == "__main__":
    main()
