from __future__ import annotations

from typing import Any

from .repository import ExecutionLedger


class ResultStore:
    def __init__(self, ledger: ExecutionLedger | None = None) -> None:
        self.ledger = ledger or ExecutionLedger()

    def save(
        self,
        impact_run_id: str,
        *,
        status: str,
        data_quality_status: str,
        result_hash: str,
        payload: dict[str, Any],
    ) -> None:
        self.ledger.complete(
            impact_run_id,
            status=status,
            data_quality_status=data_quality_status,
            result_hash=result_hash,
            payload=payload,
        )

    def get(self, impact_run_id: str) -> dict[str, Any] | None:
        record = self.ledger.get(impact_run_id)
        return record.payload if record else None
