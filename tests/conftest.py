"""Shared test configuration.

The API requires credentials on every business route, so the suite pins a known
operator key and a known auditor key for the whole session.
"""

import pytest

from chronosdb.config import Settings, get_settings
from src.backend.chronosdb.api.app import app

OPERATOR_KEY = "test-operator-key"
AUDITOR_KEY = "test-auditor-key"

OPERATOR_HEADERS = {"X-API-Key": OPERATOR_KEY}
AUDITOR_HEADERS = {"X-API-Key": AUDITOR_KEY}


@pytest.fixture(autouse=True, scope="session")
def _test_credentials():
    app.dependency_overrides[get_settings] = lambda: Settings(
        CHRONOSDB_API_KEY=OPERATOR_KEY,
        CHRONOSDB_AUDIT_KEY=AUDITOR_KEY,
    )
    yield
    app.dependency_overrides.pop(get_settings, None)
