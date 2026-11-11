import os

import pytest

from chronosdb.api import health_sql_path
from chronosdb.config import get_settings
from chronosdb.db2 import Db2Client


pytestmark = pytest.mark.db2


def test_db2_health_table_round_trip() -> None:
    if os.getenv("RUN_DB2_INTEGRATION_TESTS") != "1":
        pytest.skip("Set RUN_DB2_INTEGRATION_TESTS=1 to run against local Db2")

    client = Db2Client(get_settings())
    client.ensure_health_table(health_sql_path())
    client.record_health_check("test", "pass", "integration test")

    latest = client.latest_health_check()

    assert latest is not None
    assert latest["component"] == "test"
    assert latest["status"] == "pass"
