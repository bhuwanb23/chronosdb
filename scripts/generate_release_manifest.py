"""Generate a deterministic manifest for a Phase 4 release profile."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from data_generator.release_export import write_release_json
from data_generator.release_profile import load_release_profile, profile_payload, release_root


def _revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _source_state(root: Path) -> dict[str, str | bool]:
    """Record enough source state to reproduce a dirty working-tree release."""
    source_roots = ("src", "scripts", "config", "schemas", "tests")
    source_files = [
        path
        for source_root in source_roots
        for path in (root / source_root).rglob("*")
        if path.is_file()
    ]
    source_files.extend(
        path
        for path in (root / "Makefile", root / "pyproject.toml")
        if path.is_file()
    )
    source_digest = hashlib.sha256()
    for path in sorted(source_files):
        source_digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        source_digest.update(path.read_bytes())
    try:
        diff = subprocess.check_output(
            [
                "git",
                "diff",
                "HEAD",
                "--",
                "src",
                "scripts",
                "config",
                "schemas",
                "tests",
                "Makefile",
                "pyproject.toml",
            ],
            cwd=root,
            text=False,
        )
        raw_status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=root,
            text=True,
        )
        status = "\n".join(
            line
            for line in raw_status.splitlines()
            if not line[3:].replace("\\", "/").startswith(
                ("data/", "artifacts/", "docs/dataset-release/")
            )
        )
    except (OSError, subprocess.CalledProcessError):
        return {
            "working_tree_clean": False,
            "working_tree_diff_sha256": "unavailable",
            "working_tree_status_sha256": "unavailable",
            "source_input_sha256": source_digest.hexdigest(),
        }
    return {
        "working_tree_clean": not status.strip(),
        "working_tree_diff_sha256": hashlib.sha256(diff).hexdigest(),
        "working_tree_status_sha256": hashlib.sha256(status.encode("utf-8")).hexdigest(),
        "source_input_sha256": source_digest.hexdigest(),
    }


def _configuration_hash(root: Path) -> str:
    files = sorted((root / "config").rglob("*.yaml"))
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _count(path: Path) -> int:
    if path.suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as stream:
            return sum(1 for _ in csv.DictReader(stream))
    if path.suffix == ".jsonl":
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 1
    return len(payload) if isinstance(payload, list) else 1


def _format(path: Path) -> str:
    if path.suffix == ".csv":
        return "csv"
    if path.suffix == ".jsonl":
        return "jsonl"
    if path.suffix == ".json":
        return "json"
    if path.suffix == ".md":
        return "markdown"
    return path.suffix.lstrip(".") or "text"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("tiny", "demo", "standard", "stress"), default="demo")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    profile = load_release_profile(args.root, args.profile)
    output = release_root(profile)
    nested_profiles = {"tiny", "demo", "standard", "stress"}
    files: list[dict[str, Any]] = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.name in {"manifest.json", "checksums.sha256"}:
            continue
        relative_to_output = path.relative_to(output)
        if profile.profile == "demo" and relative_to_output.parts[0] in nested_profiles:
            continue
        files.append(
            {
                "path": path.relative_to(args.root).as_posix(),
                "record_count": _count(path),
                "format": _format(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "load_order": (
                    1
                    if "/master/" in path.as_posix()
                    else 2
                    if "/operations/" in path.as_posix()
                    else 3
                    if "/inventory/" in path.as_posix()
                    else 4
                    if "/production/" in path.as_posix()
                    else 5
                ),
            }
        )
    manifest = {
        "dataset": "chronosdb-demo-dataset",
        "version": profile.version,
        "profile": profile.profile,
        "seed": profile.seed,
        "generator_version": "chronosdb-data-generator-0.1.0",
        "domain_model_version": "phase4-domain-model-1.0.0",
        "generation_config_hash": _configuration_hash(args.root),
        "source_revision": _revision(args.root),
        "source_state": _source_state(args.root),
        "generation_time_utc": "2026-11-11T02:30:00Z",
        "currency": profile.currency,
        "canonical_timezone": profile.storage_timezone,
        "display_timezone": profile.display_timezone,
        "license": "LicenseRef-ChronosDB-Synthetic-Data-1.0",
        "profile_contract": profile_payload(profile),
        "files": files,
        "partitions": (
            json.loads(
                (output / "benchmarks" / "partition_manifest.json").read_text(
                    encoding="utf-8"
                )
            ).get("exclusive_partitions", {})
            if (output / "benchmarks" / "partition_manifest.json").exists()
            else {}
        ),
        "validation": {
            "command": (
                f"python scripts/validate_phase4.py --profile {profile.profile} "
                "--scope 4A-4V"
            ),
            "status": "PENDING_FINALIZATION",
        },
        "load_order": [
            "master",
            "operations",
            "inventory",
            "production",
            "demand",
            "history",
            "disruptions",
            "interventions",
            "evidence",
            "golden",
            "benchmarks",
            "reports",
        ],
    }
    write_release_json(output / "manifest.json", manifest)
    print(f"Generated Phase 4 {profile.profile} manifest for {len(files)} files")


if __name__ == "__main__":
    main()
