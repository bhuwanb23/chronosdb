"""Run the reproducible Phase 3 release pipeline."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _run(root: Path, script: str, *arguments: str) -> None:
    subprocess.run(
        [sys.executable, str(root / "scripts" / script), "--root", str(root), *arguments],
        check=True,
        cwd=root,
    )


def _clean(root: Path) -> None:
    for relative in ("data/generated", "artifacts"):
        path = root / relative
        if path.exists():
            shutil.rmtree(path)
    for relative in (
        "data/manifest.json",
        "data/checksums.sha256",
        "data/phase4_load_contract.json",
    ):
        path = root / relative
        if path.exists():
            path.unlink()
    traceability = root / "docs" / "data" / "phase-3-traceability-matrix.csv"
    if traceability.exists():
        traceability.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    root = args.root
    if args.clean:
        _clean(root)
    for scale in ("tiny", "standard", "stress"):
        _run(root, "generate_operational.py", "--scale", scale)
        _run(root, "generate_scenarios.py", "--scale", scale)
    _run(root, "check_frozen_inputs.py")
    _run(root, "check_reproducibility.py")
    _run(root, "validate_release.py")
    _run(root, "report_dataset.py")
    _run(root, "build_handoff.py")
    _run(root, "generate_checksums.py")
    _run(root, "score_dataset.py")
    _run(root, "finalize_release.py")
    _run(root, "generate_checksums.py")
    print("Phase 3P–3V data pipeline completed")


if __name__ == "__main__":
    main()
