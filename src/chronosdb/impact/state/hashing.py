from __future__ import annotations

import hashlib
from typing import Any

from .canonicalization import canonical_json


def state_hash(payload: Any) -> str:
    return hashlib.sha256(canonical_json(payload)).hexdigest()
