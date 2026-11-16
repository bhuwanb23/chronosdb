"""
Phase 11M: Idempotency Engine
Backend and API Integration
"""

import hashlib
from typing import Any


class IdempotencyConflictError(ValueError):
    """An idempotency key was reused for a different request."""


class IdempotencyEngine:
    """
    Phase 11M: Critical for enterprise workflows

    Problem: User clicks Run Optimization twice
    Must not create: duplicate decisions, duplicate simulations

    Header: Idempotency-Key
    Behavior: Same request → Same result
    """

    def __init__(self):
        self.idempotency_keys = {}

    def check_idempotency(self, key: str, request_hash: str) -> dict[str, Any] | None:
        """
        Check if request with same key and hash already processed
        """
        if key in self.idempotency_keys:
            stored_hash, result = self.idempotency_keys[key]
            if stored_hash == request_hash:
                return result  # Return cached result
            raise IdempotencyConflictError(
                "Idempotency-Key was already used for a different request"
            )
        return None

    def store_result(self, key: str, request_hash: str, result: dict[str, Any]):
        """
        Store result for future idempotency checks
        """
        self.idempotency_keys[key] = (request_hash, result)

    def generate_request_hash(self, request_data: dict[str, Any]) -> str:
        """
        Generate hash from request data
        """
        import json

        request_str = json.dumps(request_data, sort_keys=True)
        return hashlib.sha256(request_str.encode()).hexdigest()


# Phase 11M Status: ✅ COMPLETE
