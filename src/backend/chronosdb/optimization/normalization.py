"""Phase 7G: min-max normalization over the feasible candidate set."""

from __future__ import annotations

from typing import Any, Iterable

from .contracts import (
    CandidateMetrics,
    NormalizedMetrics,
    OptimizationValidationError,
)

BENEFIT_METRICS = ("revenue_protected", "breaches_avoided", "delay_reduction")
COST_METRICS = ("recovery_cost", "supplier_risk")
METRIC_KEYS = (*BENEFIT_METRICS, *COST_METRICS)


def _value(candidate: CandidateMetrics, key: str) -> float:
    if key == "delay_reduction":
        return candidate.delay_reduction_hours
    return float(getattr(candidate, key))


class NormalizationEngine:
    """Normalize benefits and costs to an oriented 0..1 scale.

    A benefit uses ``(value - min) / (max - min)``. A cost uses
    ``(max - value) / (max - min)`` so that 1.0 always means "better". If all
    feasible candidates share a value, that metric contributes 0.0 to every
    candidate; it cannot break a tie by accident.
    """

    def calculate_ranges(
        self, candidates: Iterable[CandidateMetrics]
    ) -> dict[str, dict[str, float]]:
        items = tuple(candidates)
        if not items:
            raise OptimizationValidationError("normalization requires candidates")
        ranges: dict[str, dict[str, float]] = {}
        for key in METRIC_KEYS:
            values = [_value(item, key) for item in items]
            ranges[key] = {"min": min(values), "max": max(values)}
        return ranges

    def normalize(
        self, candidates: Iterable[CandidateMetrics]
    ) -> tuple[NormalizedMetrics, ...]:
        items = tuple(candidates)
        ranges = self.calculate_ranges(items)
        normalized: list[NormalizedMetrics] = []
        for candidate in items:
            values: dict[str, float] = {}
            for key in METRIC_KEYS:
                minimum = ranges[key]["min"]
                maximum = ranges[key]["max"]
                if maximum - minimum <= 1e-12:
                    values[key] = 0.0
                    continue
                raw = _value(candidate, key)
                if key in BENEFIT_METRICS:
                    score = (raw - minimum) / (maximum - minimum)
                else:
                    score = (maximum - raw) / (maximum - minimum)
                values[key] = round(max(0.0, min(1.0, score)), 12)
            normalized.append(
                NormalizedMetrics(
                    candidate_id=candidate.candidate_id,
                    revenue_protected=values["revenue_protected"],
                    breaches_avoided=values["breaches_avoided"],
                    delay_reduction=values["delay_reduction"],
                    recovery_cost=values["recovery_cost"],
                    supplier_risk=values["supplier_risk"],
                )
            )
        return tuple(normalized)

    # Compatibility helpers for the earlier Phase 7 surface.
    def normalize_single(
        self,
        metrics: dict[str, Any],
        min_values: dict[str, float],
        max_values: dict[str, float],
    ) -> NormalizedMetrics:
        candidate = CandidateMetrics.from_dict(metrics)
        values: dict[str, float] = {}
        for key in METRIC_KEYS:
            minimum = float(min_values.get(key, min_values.get("cost", 0.0)))
            maximum = float(max_values.get(key, max_values.get("cost", 1.0)))
            if maximum - minimum <= 1e-12:
                values[key] = 0.0
                continue
            raw = _value(candidate, key)
            score = (
                (raw - minimum) / (maximum - minimum)
                if key in BENEFIT_METRICS
                else (maximum - raw) / (maximum - minimum)
            )
            values[key] = round(max(0.0, min(1.0, score)), 12)
        return NormalizedMetrics(
            candidate_id=candidate.candidate_id,
            revenue_protected=values["revenue_protected"],
            breaches_avoided=values["breaches_avoided"],
            delay_reduction=values["delay_reduction"],
            recovery_cost=values["recovery_cost"],
            supplier_risk=values["supplier_risk"],
        )

    def normalize_multiple(
        self, metrics_list: list[dict[str, Any]]
    ) -> list[NormalizedMetrics]:
        candidates = [
            CandidateMetrics.from_dict(metrics) for metrics in metrics_list
        ]
        return list(self.normalize(candidates))
