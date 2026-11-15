"""Phase 7N: deterministic JSONL ledger for optimization runs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .contracts import OptimizationResult, canonical_hash


RECORD_TYPES = (
    "OPTIMIZATION_RUN",
    "INPUT",
    "CANDIDATE_SCORE",
    "CONSTRAINT_RESULT",
    "PARETO_RESULT",
    "RECOMMENDATION",
    "SENSITIVITY_RESULT",
)


@dataclass(frozen=True)
class OptimizationLedger:
    """Append-only JSONL ledger with injected, deterministic paths."""

    path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.path, Path):
            object.__setattr__(self, "path", Path(self.path))

    def append(
        self,
        result: OptimizationResult,
        *,
        run_id: str | None = None,
        created_at: str | None = None,
        baseline_state_hash: str | None = None,
    ) -> list[dict[str, Any]]:
        rule_set_version = (
            result.candidates[0].rule_set_version if result.candidates else "unknown"
        )
        if run_id is None:
            run_id = "run-" + canonical_hash(
                {
                    "scenario_id": result.scenario_id,
                    "result_hash": result.result_hash,
                    "rule_set_version": rule_set_version,
                }
            )[:16]
        if created_at is None:
            created_at = "deterministic"
        if baseline_state_hash is None:
            baseline_state_hash = result.baseline_state_hash

        common = {
            "run_id": run_id,
            "scenario_id": result.scenario_id,
            "baseline_state_hash": baseline_state_hash,
            "result_hash": result.result_hash,
            "rule_set_version": rule_set_version,
            "created_at": created_at,
        }
        payloads: dict[str, dict[str, Any]] = {
            "OPTIMIZATION_RUN": {
                "engine_version": result.engine_version,
                "objective": result.objective.objective.value,
                "weights": result.objective.weights.to_dict(),
                "runtime_ms": result.runtime_ms,
            },
            "INPUT": {
                "candidate_ids": [item.candidate_id for item in result.candidates],
                "simulation_hashes": [
                    item.simulation_hash for item in result.candidates
                ],
                "constraint_version": result.constraints_version,
                "constraints": dict(result.constraint_set),
            },
            "CANDIDATE_SCORE": {
                "scores": [item.to_dict() for item in result.utilities],
            },
            "CONSTRAINT_RESULT": {
                "results": [item.to_dict() for item in result.feasibility],
            },
            "PARETO_RESULT": {
                "results": [item.to_dict() for item in result.pareto],
                "frontier": [
                    item.candidate_id
                    for item in result.pareto
                    if item.status.value == "PARETO_OPTIMAL"
                ],
            },
            "RECOMMENDATION": result.recommendation.to_dict(),
            "SENSITIVITY_RESULT": result.sensitivity.to_dict(),
        }

        records: list[dict[str, Any]] = []
        for record_type in RECORD_TYPES:
            body = {**common, "record_type": record_type, **payloads[record_type]}
            body["record_hash"] = canonical_hash(body)
            records.append(body)

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        return records

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def run_ids(self) -> list[str]:
        return [row["run_id"] for row in self.read_all()]

    @classmethod
    def default(cls, root: Path | None = None) -> "OptimizationLedger":
        base = Path(root) if root is not None else Path("artifacts/phase-7")
        return cls(base / "optimization-ledger.jsonl")
