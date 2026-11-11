from fastapi.testclient import TestClient

from chronosdb.api import create_app
from chronosdb.config import Settings


class FakeDb2:
    def __init__(self, result: dict[str, str] | None = None) -> None:
        self.result = result or {
            "server": "CHRONOS",
            "checked_at": "2026-11-11T00:00:00",
            "user": "DB2INST1",
        }

    def readiness(self) -> dict[str, str]:
        return self.result


class FailingDb2:
    def readiness(self) -> dict[str, str]:
        from chronosdb.db2 import Db2UnavailableError

        raise Db2UnavailableError("internal connection details")


def configured_settings() -> Settings:
    return Settings(
        DB2_DATABASE="CHRONOS",
        DB2_USERNAME="db2inst1",
        DB2_PASSWORD="secret",
        DB2_SCHEMA="CHRONOS",
    )


def test_liveness_does_not_require_db2() -> None:
    client = TestClient(create_app(Settings()))

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_reports_configuration_failure_without_connecting() -> None:
    client = TestClient(create_app(Settings(), FakeDb2()))

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "not_ready",
        "checks": {"configuration": "fail", "db2": "not_checked"},
    }


def test_readiness_reports_db2_success() -> None:
    client = TestClient(create_app(configured_settings(), FakeDb2()))

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"configuration": "pass", "db2": "pass"},
    }


def test_readiness_sanitizes_db2_failure() -> None:
    client = TestClient(create_app(configured_settings(), FailingDb2()))

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {"db2": "fail"},
    }
    assert "internal" not in response.text


def test_version_does_not_expose_credentials() -> None:
    client = TestClient(create_app(configured_settings(), FakeDb2()))

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "version": "0.1.0",
        "environment": "development",
        "schema_version": "0",
    }
    assert "secret" not in response.text.lower()
