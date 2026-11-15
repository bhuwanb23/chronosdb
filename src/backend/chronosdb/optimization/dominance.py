"""Compatibility wrapper around Phase 7 Pareto dominance analysis."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .contracts import CandidateMetrics
from .pareto import ParetoEngine


class DominanceAnalysis:
    def __init__(self, tolerance: float = 1e-9) -> None:
        self.engine = ParetoEngine(tolerance=tolerance)

    def analyze(self, candidates: Iterable[Any]) -> list[dict[str, Any]]:
        normalized: list[CandidateMetrics] = []
        for candidate in candidates:
            if isinstance(candidate, CandidateMetrics):
                normalized.append(candidate)
            elif isinstance(candidate, Mapping):
                normalized.append(CandidateMetrics.from_dict(dict(candidate)))
            else:
                raise ValueError("dominance input must be a candidate or mapping")
        return self.engine.analyze(normalized)

    def dominates(self, left: CandidateMetrics, right: CandidateMetrics) -> bool:
        return self.engine.dominates(left, right)
