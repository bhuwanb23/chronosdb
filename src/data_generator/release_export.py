"""Stable exports for Phase 4 release files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def write_release_csv(
    path: Path,
    rows: list[dict[str, Any]],
    field_order: list[str] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = field_order or sorted({key for row in rows for key in row})
    ordered = sorted(rows, key=lambda row: str(row.get("id", row.get("document_id", ""))))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in ordered:
            writer.writerow(
                {
                    field: "" if row.get(field) is None else str(row.get(field))
                    for field in fields
                }
            )


def write_release_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
