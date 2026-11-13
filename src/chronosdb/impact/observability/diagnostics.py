from __future__ import annotations

import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ImpactDiagnostics:
    """Safe, structured diagnostics for one impact execution."""

    correlation_id: str
    scenario_id: str
    impact_run_id: str | None = None
    stage_timings_ms: dict[str, float] = field(default_factory=dict)
    counters: dict[str, int] = field(default_factory=dict)
    warnings: int = 0
    errors: int = 0
    status: str = "PENDING"
    _started_at: float | None = field(default=None, init=False, repr=False)

    def start(self, impact_run_id: str) -> None:
        self.impact_run_id = impact_run_id
        self._started_at = time.perf_counter()

    @contextmanager
    def stage(self, name: str) -> Iterator[None]:
        started = time.perf_counter()
        try:
            yield
        finally:
            self.stage_timings_ms[name] = round(
                (time.perf_counter() - started) * 1000,
                3,
            )

    def count(self, name: str, value: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + value

    def finish(self, status: str) -> None:
        self.status = status
        if self._started_at is not None:
            self.stage_timings_ms["total"] = round(
                (time.perf_counter() - self._started_at) * 1000,
                3,
            )

    def log_record(self) -> dict[str, Any]:
        """Return only identifiers and safe aggregate diagnostics."""
        return {
            "correlation_id": self.correlation_id,
            "impact_run_id": self.impact_run_id,
            "scenario_id": self.scenario_id,
            "phase": "impact",
            "status": self.status,
            "duration_ms": self.stage_timings_ms.get("total"),
            "stage_timings_ms": dict(sorted(self.stage_timings_ms.items())),
            "counters": dict(sorted(self.counters.items())),
            "warnings": self.warnings,
            "errors": self.errors,
        }

    def emit(self, logger: logging.Logger | None = None) -> dict[str, Any]:
        record = self.log_record()
        (logger or logging.getLogger("chronosdb.impact")).info(
            "impact_run_diagnostics",
            extra={"impact_diagnostics": record},
        )
        return record
