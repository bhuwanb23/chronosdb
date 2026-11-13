from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


class PersistenceError(Exception):
    """The immutable execution ledger rejected a write."""


@dataclass
class ImpactRunRecord:
    impact_run_id: str
    scenario_id: str
    request_fingerprint: str
    input_state_hash: str
    rule_set_version: str
    status: str
    data_quality_status: str
    started_at: str
    completed_at: str | None = None
    result_hash: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    error_summary: str | None = None


class ExecutionLedger:
    """Small persistence abstraction with immutable completed outputs.

    The calculation layer can use this in tests and local execution. A Db2
    adapter can implement the same methods without changing domain modules.
    """

    def __init__(self) -> None:
        self._runs: dict[str, ImpactRunRecord] = {}
        self._fingerprints: dict[str, str] = {}

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat().replace("+00:00", "Z")

    def find_by_fingerprint(self, fingerprint: str) -> ImpactRunRecord | None:
        run_id = self._fingerprints.get(fingerprint)
        return deepcopy(self._runs.get(run_id)) if run_id else None

    def begin(
        self,
        *,
        impact_run_id: str,
        scenario_id: str,
        request_fingerprint: str,
        input_state_hash: str,
        rule_set_version: str,
        data_quality_status: str = "COMPLETE",
    ) -> ImpactRunRecord:
        existing = self.find_by_fingerprint(request_fingerprint)
        if existing is not None:
            return existing
        record = ImpactRunRecord(
            impact_run_id=impact_run_id,
            scenario_id=scenario_id,
            request_fingerprint=request_fingerprint,
            input_state_hash=input_state_hash,
            rule_set_version=rule_set_version,
            status="PENDING",
            data_quality_status=data_quality_status,
            started_at=self._now(),
        )
        self._runs[impact_run_id] = record
        self._fingerprints[request_fingerprint] = impact_run_id
        return deepcopy(record)

    def complete(
        self,
        impact_run_id: str,
        *,
        status: str,
        data_quality_status: str,
        result_hash: str,
        payload: dict[str, Any],
    ) -> ImpactRunRecord:
        record = self._runs.get(impact_run_id)
        if record is None:
            raise PersistenceError(f"unknown impact run: {impact_run_id}")
        if record.completed_at is not None:
            if record.result_hash != result_hash:
                raise PersistenceError("completed impact run is immutable")
            return deepcopy(record)
        record.status = status
        record.data_quality_status = data_quality_status
        record.result_hash = result_hash
        record.completed_at = self._now()
        record.payload = deepcopy(payload)
        return deepcopy(record)

    def fail(
        self,
        impact_run_id: str,
        *,
        error_summary: str,
        payload: dict[str, Any] | None = None,
    ) -> ImpactRunRecord:
        record = self._runs.get(impact_run_id)
        if record is None:
            raise PersistenceError(f"unknown impact run: {impact_run_id}")
        if record.completed_at is not None:
            return deepcopy(record)
        record.status = "FAILED"
        record.error_summary = error_summary
        record.completed_at = self._now()
        if payload is not None:
            record.payload = deepcopy(payload)
        return deepcopy(record)

    def get(self, impact_run_id: str) -> ImpactRunRecord | None:
        return deepcopy(self._runs.get(impact_run_id))

    def all(self) -> tuple[ImpactRunRecord, ...]:
        return tuple(deepcopy(self._runs[key]) for key in sorted(self._runs))
