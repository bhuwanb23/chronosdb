from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_global_checksums_exist_and_match_packaged_files() -> None:
    checksum_file = ROOT / "data" / "checksums.sha256"
    assert checksum_file.exists()
    lines = [line for line in checksum_file.read_text(encoding="utf-8").splitlines() if line]
    assert len(lines) >= 100
    for line in lines:
        expected, relative = line.split("  ", maxsplit=1)
        path = ROOT / relative
        assert path.exists(), relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative
