"""Phase 8W: Phase 9 Handoff.

Handoff Package:
- Evidence Package (Phase 8N)
- Review Gate Result (Phase 8V)
- Performance Metrics (Phase 8T)
- Benchmark Results (Phase 8Q)
- Security Validation (Phase 8R)
- Observability Logs (Phase 8U)
- Provenance Records (Phase 8M)

Output:
chronosdb-evidence-layer-v1.0.0
"""

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any


def _stable_payload(value: Any) -> Any:
    """Remove runtime-only fields before deriving a replay identity."""
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
class HandoffPackage:
    """Phase 9 Handoff package."""

    package_id: str
    evidence_package: dict[str, Any]
    review_gate_result: dict[str, Any]
    performance_metrics: list[dict[str, Any]]
    benchmark_results: list[dict[str, Any]]
    security_validation: list[dict[str, Any]]
    observability_logs: list[dict[str, Any]]
    provenance_records: list[dict[str, Any]]
    timestamp: str
    deliverable_version: str


class Phase9Handoff:
    """
    Phase 8W: Phase 9 Handoff.

    Prepares handoff package for Phase 9 consumption.
    """

    def __init__(self):
        pass

    def create_handoff_package(
        self,
        evidence_package: dict[str, Any],
        review_gate_result: dict[str, Any],
        performance_metrics: list[dict[str, Any]],
        benchmark_results: list[dict[str, Any]],
        security_validation: list[dict[str, Any]],
        observability_logs: list[dict[str, Any]],
        provenance_records: list[dict[str, Any]],
    ) -> HandoffPackage:
        """Create Phase 9 handoff package."""
        payload = _stable_payload(
            {
                "evidence_package": evidence_package,
                "review_gate_result": review_gate_result,
                "performance_metrics": performance_metrics,
                "benchmark_results": benchmark_results,
                "security_validation": security_validation,
                "observability_logs": observability_logs,
                "provenance_records": provenance_records,
                "deliverable_version": "chronosdb-evidence-layer-v1.0.0",
            }
        )
        package_hash = (
            sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8"))
            .hexdigest()[:16]
            .upper()
        )
        package_id = f"HANDOFF-PHASE8-PHASE9-{package_hash}"

        return HandoffPackage(
            package_id=package_id,
            evidence_package=evidence_package,
            review_gate_result=review_gate_result,
            performance_metrics=performance_metrics,
            benchmark_results=benchmark_results,
            security_validation=security_validation,
            observability_logs=observability_logs,
            provenance_records=provenance_records,
            timestamp="deterministic",
            deliverable_version="chronosdb-evidence-layer-v1.0.0",
        )

    def save_handoff_package(
        self,
        package: HandoffPackage,
        storage_path: str = "artifacts/evidence/handoff/",
    ):
        """Save handoff package for Phase 9."""
        path = Path(storage_path)
        path.mkdir(parents=True, exist_ok=True)
        filename = f"{package.package_id}.json"
        filepath = path / filename

        with filepath.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "package_id": package.package_id,
                    "evidence_package": package.evidence_package,
                    "review_gate_result": package.review_gate_result,
                    "performance_metrics": package.performance_metrics,
                    "benchmark_results": package.benchmark_results,
                    "security_validation": package.security_validation,
                    "observability_logs": package.observability_logs,
                    "provenance_records": package.provenance_records,
                    "timestamp": package.timestamp,
                    "deliverable_version": package.deliverable_version,
                },
                f,
                indent=2,
            )

        return package


# Phase 8W Status: IMPLEMENTED
