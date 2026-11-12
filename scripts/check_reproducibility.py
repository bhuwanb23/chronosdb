"""Run a deterministic second generation and compare generated file hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def _hashes(root: Path) -> dict[str, str]:
    directory = root / "data" / "generated"
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root
    before = _hashes(root)
    for scale in ("tiny", "standard", "stress"):
        for script in ("generate_operational.py", "generate_scenarios.py"):
            subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts" / script),
                    "--root",
                    str(root),
                    "--scale",
                    scale,
                ],
                check=True,
                cwd=root,
                stdout=subprocess.DEVNULL,
            )
    after = _hashes(root)
    changed = sorted(
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    )
    report: dict[str, Any] = {
        "report_version": "1.0.0",
        "seed": 260311,
        "scales": ["tiny", "standard", "stress"],
        "checked_file_count": len(set(before) | set(after)),
        "nondeterministic_files": changed,
        "status": "PASS" if not changed else "FAIL",
    }
    output = root / "artifacts" / "reproducibility.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Reproducibility: {report['status']} ({report['checked_file_count']} files)")
    if changed:
        raise SystemExit("Generated output changed between deterministic runs")


if __name__ == "__main__":
    main()
