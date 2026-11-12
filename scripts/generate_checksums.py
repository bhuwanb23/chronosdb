"""Build the Phase 3 package manifest and global checksum file."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

INCLUDED_ROOTS = (
    Path("data/generated"),
    Path("data/golden"),
    Path("data/benchmarks"),
    Path("data/fixtures"),
    Path("artifacts"),
    Path("docs/data"),
)
PACKAGE_FILES = (
    Path("data/README.md"),
    Path("data/phase4_load_contract.json"),
    Path("data/frozen_inputs.sha256"),
)
EXCLUDED_NAMES = {"checksums.sha256"}


def _record_count(path: Path) -> int:
    if path.suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as stream:
            return max(0, sum(1 for _ in csv.DictReader(stream)))
    if path.suffix == ".jsonl":
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    if path.suffix == ".json":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return 1
        return len(payload) if isinstance(payload, (dict, list)) else 1
    return 1


def _stage(path: Path) -> str:
    parts = path.parts
    if "generated" in parts:
        return parts[parts.index("generated") + 1]
    if "golden" in parts:
        return "golden"
    if "benchmarks" in parts:
        return "benchmarks"
    if "fixtures" in parts:
        return "fixtures"
    if "artifacts" in parts:
        return "reports"
    return "documentation"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _files(root: Path) -> list[Path]:
    paths: list[Path] = []
    paths.extend(root / relative for relative in PACKAGE_FILES if (root / relative).exists())
    for relative_root in INCLUDED_ROOTS:
        directory = root / relative_root
        if directory.exists():
            paths.extend(
                path
                for path in directory.rglob("*")
                if path.is_file()
                and path.name not in EXCLUDED_NAMES
                and path != root / "data" / "manifest.json"
            )
    return sorted(set(paths))


def _source_revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def build_package_manifest(root: Path) -> dict[str, Any]:
    files = _files(root)
    entries = [
        {
            "path": path.relative_to(root).as_posix(),
            "record_count": _record_count(path),
            "sha256": _sha(path),
            "generator_stage": _stage(path.relative_to(root)),
            "configuration": "config/generation.yaml",
            "random_seed": 260311,
            "schema_version": "1.0.0",
        }
        for path in files
    ]
    return {
        "dataset_name": "chronosdb-synthetic-supply-chain",
        "version": "1.0.0",
        "dataset_version": "1.0.0",
        "phase": "3",
        "status": "release_candidate",
        "random_seed": 260311,
        "source_revision": _source_revision(root),
        "reference_time": "2026-11-11T02:30:00Z",
        "files": entries,
    }


def write_checksums(root: Path, manifest: dict[str, Any]) -> None:
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = data_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    checksum_paths = [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and path.name != "checksums.sha256"
        and (
            path.is_relative_to(root / "data")
            or path.is_relative_to(root / "artifacts")
            or path.is_relative_to(root / "docs" / "data")
        )
    ]
    checksum_lines = [
        f"{_sha(path)}  {path.relative_to(root).as_posix()}" for path in checksum_paths
    ]
    (data_dir / "checksums.sha256").write_text(
        "\n".join(checksum_lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    manifest = build_package_manifest(args.root)
    write_checksums(args.root, manifest)
    print(f"Packaged {len(manifest['files'])} Phase 3 assets")


if __name__ == "__main__":
    main()
