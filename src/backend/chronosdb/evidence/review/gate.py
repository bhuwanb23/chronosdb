"""Phase 8V: Evidence Review Gate.

Review Criteria:
- Evidence classification distribution
- Security filter violations
- Performance targets met
- Golden benchmark passed
- Provenance integrity
- Observability logs complete

Gate Rules:
- All criteria must pass
- No security violations
- Performance targets met
- Golden benchmark passed
- Provenance complete
"""

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Any


def _stable_payload(value: Any) -> Any:
    """Remove runtime-only fields before deriving a gate identity."""
    if isinstance(value, dict):
        return {
            key: _stable_payload(item)
            for key, item in value.items()
            if key
            not in {
                "timestamp",
                "log_id",
                "record_id",
                "runtime_ms",
                "generation_time_ms",
                "execution_time_ms",
                "latency_ms",
                "p95_latency_ms",
                "created_at",
                "ingestion_time",
                "cpu_usage_percent",
                "memory_usage_mb",
                "throughput_qps",
                "actual",
                "difference",
                "gate_id",
            }
        }
    if isinstance(value, list):
        return [_stable_payload(item) for item in value]
    return value


@dataclass(frozen=True)
class ReviewGateResult:
    """Evidence review gate result."""

    gate_id: str
    criteria_passed: bool
    security_violations: int
    performance_targets_met: bool
    golden_benchmark_passed: bool
    provenance_complete: bool
    observability_complete: bool
    overall_passed: bool
    analysis: dict[str, Any]


class EvidenceReviewGate:
    """
    Phase 8V: Evidence Review Gate.

    Validates evidence retrieval against review criteria.
    """

    def __init__(self):
        pass

    def evaluate_gate(
        self,
        classification_results: list[dict[str, Any]],
        security_results: list[dict[str, Any]],
        performance_results: list[dict[str, Any]],
        benchmark_results: list[dict[str, Any]],
        provenance_records: list[dict[str, Any]],
        observability_logs: list[dict[str, Any]],
    ) -> ReviewGateResult:
        """Evaluate evidence review gate."""

        # A gate with no evidence cannot pass silently.
        criteria_passed = bool(
            classification_results
            and all(
                isinstance(result, dict)
                and any(
                    isinstance(result.get(key), str) and result[key].strip()
                    for key in ("document_id", "evidence_id")
                )
                for result in classification_results
            )
        )

        # Check security violations
        security_complete = bool(security_results) and all(
            isinstance(result, dict)
            and isinstance(result.get("evidence_id"), str)
            and result["evidence_id"].strip()
            and result["evidence_id"].strip().upper() != "UNKNOWN"
            and isinstance(result.get("authorized"), bool)
            and isinstance(result.get("access_granted"), bool)
            and isinstance(result.get("provenance_secure"), bool)
            for result in security_results
        )
        security_violations = sum(
            1
            for result in security_results
            if not isinstance(result, dict)
            or result.get("authorized") is not True
            or result.get("access_granted") is not True
            or result.get("provenance_secure") is not True
        )

        # Check performance targets
        performance_targets_met = bool(performance_results) and all(
            isinstance(result, dict) and result.get("target_met") is True
            for result in performance_results
        )

        # Check golden benchmark
        golden_benchmark_passed = bool(benchmark_results) and all(
            isinstance(result, dict) and result.get("passed") is True
            for result in benchmark_results
        )

        # Check provenance completeness
        provenance_complete = bool(provenance_records) and all(
            isinstance(record, dict)
            and any(
                isinstance(record.get(key), str) and record[key].strip()
                for key in ("document_id", "evidence_id")
            )
            for record in provenance_records
        )

        # Check observability completeness
        required_events = {
            "RETRIEVAL_START",
            "RETRIEVAL_END",
            "CLASSIFICATION",
            "SECURITY",
            "PERFORMANCE",
            "PACKAGE",
        }
        observed_events = {
            log.get("event_type") for log in observability_logs if isinstance(log, dict)
        }
        observability_complete = (
            bool(observability_logs)
            and required_events <= observed_events
            and all(
                log.get("event_type") in required_events
                and log.get("timestamp")
                and isinstance(log.get("analysis"), dict)
                for log in observability_logs
            )
        )

        # Overall pass
        overall_passed = (
            criteria_passed
            and security_complete
            and security_violations == 0
            and performance_targets_met
            and golden_benchmark_passed
            and provenance_complete
            and observability_complete
        )

        return ReviewGateResult(
            gate_id=(
                "GATE-EVIDENCE-"
                + sha256(
                    json.dumps(
                        {
                            "classification": classification_results,
                            "security": security_results,
                            "performance": performance_results,
                            "benchmark": benchmark_results,
                            "provenance": provenance_records,
                            "observability": _stable_payload(observability_logs),
                        },
                        sort_keys=True,
                        default=str,
                    ).encode("utf-8")
                ).hexdigest()[:16]
            ),
            criteria_passed=criteria_passed,
            security_violations=security_violations,
            performance_targets_met=performance_targets_met,
            golden_benchmark_passed=golden_benchmark_passed,
            provenance_complete=provenance_complete,
            observability_complete=observability_complete,
            overall_passed=overall_passed,
            analysis={
                "classification_count": len(classification_results),
                "security_count": len(security_results),
                "performance_count": len(performance_results),
                "benchmark_count": len(benchmark_results),
                "provenance_count": len(provenance_records),
                "observability_count": len(observability_logs),
                "status": "PASSED" if overall_passed else "FAILED",
            },
        )


# Phase 8V Status: IMPLEMENTED
