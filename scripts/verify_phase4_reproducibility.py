"""Compare a Phase 4 release before and after a deterministic rebuild."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


def _hashes(root: Path, profile: str) -> dict[str, str]:
    base = root / "data" / "releases" / "v1.0.0"
    directory = base if profile == "demo" else base / profile
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("tiny", "demo", "standard", "stress"), default="demo")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    before = _hashes(args.root, args.profile)
    subprocess.run(
        [
            sys.executable,
            str(args.root / "scripts" / "build_phase4_release.py"),
            "--root",
            str(args.root),
            "--profile",
            args.profile,
        ],
        check=True,
        cwd=args.root,
        stdout=subprocess.DEVNULL,
    )
    after = _hashes(args.root, args.profile)
    changed = sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )
    print(f"Phase 4 {args.profile} reproducibility: {'PASS' if not changed else 'FAIL'}")
    if changed:
        raise SystemExit(f"nondeterministic release files: {changed}")


if __name__ == "__main__":
    main()
