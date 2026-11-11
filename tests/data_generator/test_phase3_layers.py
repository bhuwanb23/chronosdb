from __future__ import annotations

from collections import Counter
from pathlib import Path

from data_generator.fixtures import build_fixtures
from data_generator.generator import generate_master, load_config
from data_generator.operational import generate_history, generate_operational
from data_generator.scenarios import SCENARIO_CATEGORIES, generate_documents, generate_scenarios
from data_generator.validation import validate_master, validate_operational

ROOT = Path(__file__).resolve().parents[2]


def test_tiny_operational_and_history_are_connected() -> None:
    config = load_config(ROOT, "tiny")
    master = generate_master(config)
    operational = generate_operational(config, master)
    validate_master(master)
    validate_operational(master, operational)
    history = generate_history(config, master, operational)
    assert len(operational["customer_orders"]) == config.counts["customer_orders"]
    correction = history["late_arriving_corrections"][0]
    assert correction["known_at"] > correction["event_time"]


def test_scenario_distribution_and_document_count() -> None:
    config = load_config(ROOT, "tiny")
    generated = generate_scenarios(config, generate_master(config))
    assert len(generated["scenario_definitions"]) == 60
    expected = dict(SCENARIO_CATEGORIES)
    observed = Counter(row["category"] for row in generated["scenario_definitions"])
    assert observed == expected
    documents, relevance = generate_documents(config, generate_master(config))
    assert len(documents) == 175
    assert len(relevance) == len(documents)


def test_fixture_suite_has_expected_error_labels() -> None:
    fixtures = build_fixtures()
    assert len(fixtures) >= 30
    assert {fixture["expected_error"] for fixture in fixtures}
