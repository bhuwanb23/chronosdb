"""Build Phase 3O named fixture metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data_generator.fixtures import build_fixtures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    fixtures = build_fixtures()
    for fixture in fixtures:
        path = args.root / "data" / "fixtures" / fixture["family"] / f"{fixture['fixture_id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    expected = {fixture["fixture_id"]: fixture["expected_error"] for fixture in fixtures}
    output = args.root / "data" / "fixtures" / "expected_errors.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Built {len(fixtures)} Phase 3O fixtures")


if __name__ == "__main__":
    main()
