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
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


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
    return len(payload) if isinstance(payload, (list, dict)) else 1


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
        if not path.is_file() or path.name == "manifest.json":
            continue
        relative_to_output = path.relative_to(output)
        if profile.profile == "demo" and relative_to_output.parts[0] in nested_profiles:
            continue
        files.append(
            {
                "path": path.relative_to(args.root).as_posix(),
                "record_count": _count(path),
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
        "source_revision": _revision(args.root),
        "profile_contract": profile_payload(profile),
        "files": files,
        "load_order": ["MASTER", "OPERATIONS", "INVENTORY", "PRODUCTION", "REPORTS"],
    }
    write_release_json(output / "manifest.json", manifest)
    print(f"Generated Phase 4 {profile.profile} manifest for {len(files)} files")


if __name__ == "__main__":
    main()
