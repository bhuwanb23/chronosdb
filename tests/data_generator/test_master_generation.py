from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from data_generator.generator import generate_master, load_config, write_master
from data_generator.validation import validate_master

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("scale", "expected"),
    [
        ("tiny", {"suppliers": 4, "components": 12, "products": 4}),
        ("standard", {"suppliers": 24, "components": 80, "products": 16}),
    ],
)
def test_counts_and_invariants(scale: str, expected: dict[str, int]) -> None:
    config = load_config(ROOT, scale)
    entities = generate_master(config)
    validate_master(entities)
    for entity, count in expected.items():
        assert len(entities[entity]) == count


def test_same_seed_is_byte_reproducible() -> None:
    first = load_config(ROOT, "tiny", 12345)
    second = load_config(ROOT, "tiny", 12345)
    first_entities = generate_master(first)
    second_entities = generate_master(second)
    assert json.dumps(first_entities, sort_keys=True) == json.dumps(
        second_entities, sort_keys=True
    )
    write_master(first, first_entities)
    write_master(second, second_entities)
    assert hashlib.sha256(
        (first.root / "data/generated/master/tiny/components.csv").read_bytes()
    ).hexdigest()


def test_different_seed_changes_master_data() -> None:
    first = generate_master(load_config(ROOT, "tiny", 1))
    second = generate_master(load_config(ROOT, "tiny", 2))
    assert first["supplier_component_agreements"] != second["supplier_component_agreements"]
