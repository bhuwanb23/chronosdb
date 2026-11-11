from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from data_generator.generator import generate_master, load_config, write_master
from data_generator.validation import validate_master

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("scale", "expected"),
    [
        ("tiny", {"suppliers": 5, "components": 15, "products": 3}),
        ("standard", {"suppliers": 24, "components": 80, "products": 16}),
    ],
)
def test_counts_and_invariants(scale: str, expected: dict[str, int]) -> None:
    config = load_config(ROOT, scale)
    entities = generate_master(config)
    validate_master(entities)
    for entity, count in expected.items():
        assert len(entities[entity]) == count


def test_same_seed_is_byte_reproducible(tmp_path: Path) -> None:
    first = replace(load_config(ROOT, "tiny", 12345), root=tmp_path / "first")
    second = replace(load_config(ROOT, "tiny", 12345), root=tmp_path / "second")
    first_entities = generate_master(first)
    second_entities = generate_master(second)
    assert json.dumps(first_entities, sort_keys=True) == json.dumps(
        second_entities, sort_keys=True
    )
    first_dir = write_master(first, first_entities)
    second_dir = write_master(second, second_entities)
    for entity in ("components", "bom_versions", "bom_lines"):
        first_hash = hashlib.sha256((first_dir / f"{entity}.csv").read_bytes()).hexdigest()
        second_hash = hashlib.sha256((second_dir / f"{entity}.csv").read_bytes()).hexdigest()
        assert first_hash == second_hash
    assert hashlib.sha256((first_dir / "manifest.json").read_bytes()).hexdigest() == hashlib.sha256(
        (second_dir / "manifest.json").read_bytes()
    ).hexdigest()


def test_different_seed_changes_master_data() -> None:
    first = generate_master(load_config(ROOT, "tiny", 1))
    second = generate_master(load_config(ROOT, "tiny", 2))
    assert first["supplier_component_agreements"] != second["supplier_component_agreements"]
