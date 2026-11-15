"""
Phase 11J: Audit and Replay Service
Backend and API Integration

Records are only served if they exist. Integrity is recomputed from the stored
payload and compared with the hash captured when the decision was sealed, so a
mutated record fails verification instead of being reported as verified.
"""

import hmac
from datetime import datetime
from typing import Any, Dict, Mapping, Optional

from chronosdb.impact.contracts.results import canonical_hash


class AuditService:
    """
    Phase 11J: Expose Phase 10 engine

    Endpoints:
    - GET /api/v1/audit/{decision_id} (Decision Audit)
    - POST /api/v1/replay/{decision_id} (Replay Decision)
    """

    def __init__(self) -> None:
        self.audits: Dict[str, Dict[str, Any]] = {}
        self.replays: Dict[str, Dict[str, Any]] = {}

    def record_decision(
        self,
        decision_id: str,
        payload: Mapping[str, Any],
        result_hash: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Seal a decision so it can be audited and replayed later."""

        sealed_hash = result_hash or canonical_hash(dict(payload))
        record = {
            "decision_id": decision_id,
            "payload": dict(payload),
            "result_hash": sealed_hash,
            "recorded_at": datetime.utcnow().isoformat(),
        }
        self.audits[decision_id] = record
        return self._public_record(record)

    def _public_record(self, record: Mapping[str, Any]) -> Dict[str, Any]:
        recomputed = canonical_hash(dict(record["payload"]))
        return {
            "decision_id": record["decision_id"],
            "result_hash": record["result_hash"],
            "recomputed_hash": recomputed,
            "integrity_verified": hmac.compare_digest(recomputed, record["result_hash"]),
            "recorded_at": record["recorded_at"],
            "payload": record["payload"],
        }

    def get_audit(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """
        GET /api/v1/audit/{decision_id}

        Returns None when no such decision was recorded.
        """

        record = self.audits.get(decision_id)
        if record is None:
            return None
        return self._public_record(record)

    def replay_decision(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """
        POST /api/v1/replay/{decision_id}

        Re-verifies the sealed record. Returns None for unknown decisions.
        """

        audit = self.get_audit(decision_id)
        if audit is None:
            return None

        replay = {
            "decision_id": decision_id,
            "reconstructed": audit,
            "replay_time": datetime.utcnow().isoformat(),
            "integrity_verified": audit["integrity_verified"],
            "status": "REPLAYED" if audit["integrity_verified"] else "INTEGRITY_FAILURE",
        }

        self.replays[decision_id] = replay
        return replay


# One process-wide audit store, shared by the audit and optimisation routers.
audit_service = AuditService()

# Phase 11J Status: COMPLETE
