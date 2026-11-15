"""Phase 7O/P: deterministic performance measurement and budget checking."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class PerformanceEvaluator:
    budget_seconds: float = 1.0

    def measure(self, operation: Callable[[], Any]) -> dict[str, Any]:
        start = time.perf_counter()
        result = operation()
        elapsed = time.perf_counter() - start
        return {
            "elapsed_seconds": elapsed,
            "budget_seconds": self.budget_seconds,
            "within_budget": elapsed <= self.budget_seconds,
            "result": result,
        }
