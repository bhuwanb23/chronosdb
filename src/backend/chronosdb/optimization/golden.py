"""Phase 7Q: frozen synthetic optimization golden scenario.

This fixture is intentionally separate from the live Phase 6 scenario. It
exercises the complete optimization pipeline on known metrics so scoring and
tie-breaking can be verified independently of simulation changes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .contracts import CandidateMetrics, OptimizationObjective, OptimizationResult
from .engine import OptimizationEngine
from .ledger import OptimizationLedger


@dataclass(frozen=True)
class GoldenScenario:
    path: Path
    scenario_id: str
    baseline_state_hash: str
    baseline_result_hash: str
    rule_set_version: str
    objective: OptimizationObjective
    candidates: tuple[CandidateMetrics, ...]
    expected: Mapping[str, Any]

    @classmethod
    def load(cls, path: Path) -> "GoldenScenario":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        candidates = tuple(
            CandidateMetrics.from_dict(item) for item in payload["candidates"]
        )
        expected_baseline = payload["baseline_result_hash"]
        if any(item.baseline_result_hash != expected_baseline for item in candidates):
            raise ValueError("golden candidates disagree on the baseline result hash")
        return cls(
            path=Path(path),
            scenario_id=payload["scenario_id"],
            baseline_state_hash=payload["baseline_state_hash"],
            baseline_result_hash=expected_baseline,
            rule_set_version=payload["rule_set_version"],
            objective=OptimizationObjective.from_dict(payload["objective"]),
            candidates=candidates,
            expected=payload.get("expected", {}),
        )

    def run(
        self,
        engine: OptimizationEngine,
        ledger: OptimizationLedger | None = None,
    ) -> OptimizationResult:
        return engine.optimize_candidates(
            self.candidates,
            scenario_id=self.scenario_id,
            baseline_state_hash=self.baseline_state_hash,
            rule_set_version=self.rule_set_version,
            ledger=ledger,
        )


def default_golden_path(root: Path) -> Path:
    return Path(root) / "data" / "golden" / "phase7-optimization.json"
