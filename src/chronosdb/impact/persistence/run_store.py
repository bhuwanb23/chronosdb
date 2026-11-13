from __future__ import annotations

from .repository import ExecutionLedger, ImpactRunRecord


class RunStore:
    def __init__(self, ledger: ExecutionLedger | None = None) -> None:
        self.ledger = ledger or ExecutionLedger()

    def get(self, impact_run_id: str) -> ImpactRunRecord | None:
        return self.ledger.get(impact_run_id)

    def find_by_fingerprint(self, fingerprint: str) -> ImpactRunRecord | None:
        return self.ledger.find_by_fingerprint(fingerprint)
