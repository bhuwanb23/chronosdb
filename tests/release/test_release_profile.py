from __future__ import annotations

from pathlib import Path

from data_generator.release_profile import load_release_profile

ROOT = Path(__file__).resolve().parents[2]


def test_all_phase4_release_profiles_are_valid() -> None:
    for name in ("tiny", "demo", "standard", "stress"):
        profile = load_release_profile(ROOT, name)
        assert profile.version == "1.0.0"
        assert profile.snapshot_scope == "active_pairs"
        assert profile.planning_horizon_days == 30
