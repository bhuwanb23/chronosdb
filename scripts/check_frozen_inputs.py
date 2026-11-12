"""Verify or initialize hashes for curated golden and benchmark inputs."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

CURATED_ROOTS = (Path("data/golden"), Path("data/benchmarks"), Path("data/fixtures"))


def _hashes(root: Path) -> list[str]:
    rows: list[str] = []
    for directory in CURATED_ROOTS:
        for path in sorted((root / directory).rglob("*")):
            if path.is_file() and path.name != "frozen_inputs.sha256":
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                rows.append(f"{digest}  {path.relative_to(root).as_posix()}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--initialize", action="store_true")
    args = parser.parse_args()
    root = args.root
    expected_path = root / "data" / "frozen_inputs.sha256"
    current = _hashes(root)
    if not expected_path.exists():
        if not args.initialize:
            raise SystemExit(
                "Missing frozen input lock; run check_frozen_inputs.py --initialize "
                "only when creating a new release baseline"
            )
        expected_path.write_text("\n".join(current) + "\n", encoding="utf-8")
        print(f"Initialized frozen input lock for {len(current)} files")
        return
    expected = [
        line for line in expected_path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    if expected != current:
        raise SystemExit("Curated golden, benchmark, or fixture inputs changed")
    print(f"Frozen input lock passed for {len(current)} files")


if __name__ == "__main__":
    main()
