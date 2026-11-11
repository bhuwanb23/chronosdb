"""Canonical exports shared by Phase 3 data-generation stages."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


def _value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    return value


def write_csv_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Write sorted, UTF-8 CSV rows and return a manifest entry."""
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows, key=lambda row: str(row.get("id", "")))
    fields = sorted({key for row in ordered for key in row})
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in ordered:
            writer.writerow({key: _value(value) for key, value in row.items()})
    parts = path.parts
    relative = "/".join(parts[parts.index("data") :]) if "data" in parts else path.name
    return {
        "path": relative,
        "record_count": len(rows),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def write_json(path: Path, payload: Any) -> dict[str, Any]:
    """Write stable JSON and return a manifest entry."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return {
        "path": path.as_posix(),
        "record_count": len(payload) if isinstance(payload, (list, dict)) else 1,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))
