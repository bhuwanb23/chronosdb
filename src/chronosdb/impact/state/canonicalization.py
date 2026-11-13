from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        normalized = [normalize(item) for item in value]
        return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
