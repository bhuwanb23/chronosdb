"""Phase 4 release-profile loading and contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ReleaseProfile:
    root: Path
    version: str
    profile: str
    source_scale: str
    seed: int
    purpose: str
    snapshot_scope: str
    snapshot_days: int
    history_days: int
    planning_horizon_days: int
    currency: str
    storage_timezone: str
    display_timezone: str
    golden_scenario_id: str
    golden_supplier_id: str | None = None
    golden_component_id: str | None = None
    golden_purchase_order_id: str | None = None


def load_release_profile(root: Path, profile: str, version: str = "1.0.0") -> ReleaseProfile:
    path = root / "config" / "releases" / f"{profile}-v{version}.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if payload.get("profile") != profile or payload.get("version") != version:
        raise ValueError(f"release profile identity mismatch: {path}")
    result = ReleaseProfile(root=root, **payload)
    validate_release_profile(result)
    return result


def validate_release_profile(profile: ReleaseProfile) -> None:
    if profile.version != "1.0.0":
        raise ValueError("Phase 4 release version must be 1.0.0")
    if profile.source_scale not in {"tiny", "standard", "stress"}:
        raise ValueError("invalid source scale")
    if profile.seed != 260311:
        raise ValueError("Phase 4 release seed must be 260311")
    if profile.snapshot_scope != "active_pairs":
        raise ValueError("Phase 4 snapshots must declare active_pairs scope")
    if not 1 <= profile.snapshot_days <= 180:
        raise ValueError("snapshot_days must be within the historical period")
    if profile.history_days != 180 or profile.planning_horizon_days != 30:
        raise ValueError("Phase 4 history/horizon contract mismatch")
    if profile.currency != "INR":
        raise ValueError("Phase 4 currency must be INR")
    if profile.storage_timezone != "UTC" or profile.display_timezone != "Asia/Kolkata":
        raise ValueError("Phase 4 timezone contract mismatch")
    if profile.golden_scenario_id != "SCN-GOLD-001":
        raise ValueError("Phase 4 golden scenario mismatch")
    if profile.profile == "demo" and not {
        profile.golden_supplier_id,
        profile.golden_component_id,
        profile.golden_purchase_order_id,
    } == {"SUP-0104", "CMP-MCU-42", "PO-2208"}:
        raise ValueError("demo profile must lock the canonical golden IDs")


def profile_payload(profile: ReleaseProfile) -> dict[str, Any]:
    return {
        key: value
        for key, value in profile.__dict__.items()
        if key != "root"
    }


def release_root(profile: ReleaseProfile) -> Path:
    """Return the immutable package root for a profile."""
    base = profile.root / "data" / "releases" / "v1.0.0"
    return base if profile.profile == "demo" else base / profile.profile
