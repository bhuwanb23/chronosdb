"""Phase 7 bridge from live Phase 6 simulations to optimization candidates."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .contracts import CandidateMetrics, OptimizationValidationError
from .metrics import MetricExtractionLayer, _result_component_ids

try:
    from chronosdb.simulation.counterfactual import (
        Overlay,
        Phase6Engine,
        load_golden_overlays,
    )
except Exception:  # pragma: no cover - fallback for namespace package layout
    from src.chronosdb.simulation.counterfactual import (  # type: ignore
        Overlay,
        Phase6Engine,
        load_golden_overlays,
    )


CANDIDATE_LABELS = {
    "DO_NOTHING": "Do Nothing",
    "TRANSFER": "Warehouse Transfer",
    "EXPEDITE": "PO Expedition",
    "ALTERNATE_SUPPLIER": "Alternate Supplier",
    "RESCHEDULE": "Production Reschedule",
    "HYBRID": "Hybrid Recovery",
}


OVERLAY_SET_TO_CANDIDATE = {
    "do_nothing": "DO_NOTHING",
    "transfer": "TRANSFER",
    "expedition": "EXPEDITE",
    "alternate_supplier": "ALTERNATE_SUPPLIER",
    "reschedule": "RESCHEDULE",
    "hybrid": "HYBRID",
}


@dataclass(frozen=True)
class Phase6Handoff:
    candidates: tuple[CandidateMetrics, ...]
    baseline_state_hash: str
    scenario_id: str
    rule_set_version: str
    warnings: tuple[str, ...]

    def validate(self) -> dict[str, Any]:
        errors: list[str] = []
        checks: list[dict[str, Any]] = []
        if len(self.candidates) < 2:
            errors.append("fewer than two candidates")
        ids = [item.candidate_id for item in self.candidates]
        if len(ids) != len(set(ids)):
            errors.append("duplicate candidate IDs")
        if "DO_NOTHING" not in ids:
            errors.append("missing DO_NOTHING baseline candidate")
        if any(item.source != "PHASE6" for item in self.candidates):
            errors.append("not all candidates came from Phase 6")
        if any(not item.simulation_hash for item in self.candidates):
            errors.append("missing simulation hash")
        versions = {item.rule_set_version for item in self.candidates}
        if len(versions) != 1:
            errors.append("inconsistent rule set versions")
        baseline_hashes = {item.baseline_result_hash for item in self.candidates}
        if len(baseline_hashes) != 1:
            errors.append("inconsistent baseline result hashes")
        for item in self.candidates:
            for field in (
                "revenue_risk",
                "revenue_protected",
                "delay_hours",
                "delay_reduction_hours",
                "recovery_cost",
                "capacity_utilization_pct",
                "inventory_consumed",
                "remaining_inventory",
                "supplier_risk",
            ):
                value = getattr(item, field)
                if value != value or value in (float("inf"), float("-inf")):
                    errors.append(f"{item.candidate_id}: non-finite {field}")
        checks.append({"check": "candidate_count", "passed": len(self.candidates) >= 2})
        checks.append({"check": "unique_ids", "passed": len(ids) == len(set(ids))})
        checks.append({"check": "has_baseline", "passed": "DO_NOTHING" in ids})
        checks.append({"check": "phase6_source", "passed": all(item.source == "PHASE6" for item in self.candidates)})
        checks.append({"check": "consistent_versions", "passed": len(versions) == 1})
        return {
            "valid": not errors,
            "errors": errors,
            "checks": checks,
            "candidate_count": len(self.candidates),
            "candidate_ids": ids,
        }


class Phase6CandidateBuilder:
    """Run Phase 6 and extract canonical optimization candidates."""

    def __init__(self, extractor: MetricExtractionLayer | None = None) -> None:
        self.extractor = extractor or MetricExtractionLayer()

    @classmethod
    def from_golden(cls, root: Path) -> "Phase6CandidateBuilder":
        return cls()

    def build(
        self,
        engine: Phase6Engine,
        overlay_sets: Mapping[str, Sequence[Any]],
    ) -> Phase6Handoff:
        candidates: list[CandidateMetrics] = []
        warnings: list[str] = []
        sets = dict(overlay_sets)
        if "do_nothing" not in sets and "DO_NOTHING" not in sets:
            sets = {"do_nothing": (), **sets}
        for set_name, overlays in sets.items():
            candidate_id = OVERLAY_SET_TO_CANDIDATE.get(set_name, set_name.upper())
            if candidate_id == "DO_NOTHING":
                candidate = self.extractor.do_nothing(engine)
            else:
                overlay_tuple = tuple(
                    item if hasattr(item, "action") else Overlay.from_dict(item)
                    for item in overlays
                )
                result = engine.run(overlay_tuple)
                candidate = self.extractor.from_phase6(
                    engine, result, candidate_id, overlay_tuple
                )
            warnings.extend(candidate.warnings)
            candidates.append(candidate)
        if not candidates:
            raise OptimizationValidationError("Phase 6 produced no candidates")
        handoff = Phase6Handoff(
            candidates=tuple(candidates),
            baseline_state_hash=engine.state.identity.state_hash,
            scenario_id=engine.scenario_id,
            rule_set_version=candidates[0].rule_set_version,
            warnings=tuple(sorted(set(warnings))),
        )
        validation = handoff.validate()
        if not validation["valid"]:
            raise OptimizationValidationError(
                "Phase 6 handoff validation failed: " + "; ".join(validation["errors"])
            )
        return handoff

    @staticmethod
    def load_overlays(path: Path) -> dict[str, tuple[Overlay, ...]]:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return {
            name: tuple(
                item if hasattr(item, "action") else Overlay.from_dict(item)
                for item in items
            )
            for name, items in payload.items()
        }

    @staticmethod
    def default_overlay_sets(root: Path) -> dict[str, Any]:
        path = root / "data" / "golden" / "phase6-overlays.json"
        loaded = Phase6CandidateBuilder.load_overlays(path)
        return {"do_nothing": (), **loaded}
