"""Phase 10R: Security testing.

These tests assert behaviour, not object existence. Every one of them fails if the
control it covers is removed.
"""

import pytest
from fastapi.testclient import TestClient

from src.backend.chronosdb.api.app import app
from src.backend.chronosdb.routers.audit import service as audit_service
from src.backend.chronosdb.routers.scenarios import idempotency as idempotency_engine
from src.backend.chronosdb.routers.scenarios import service as scenario_service
from src.backend.chronosdb.services.audit_service import AuditService

OPERATOR_KEY = "test-operator-key"
AUDITOR_KEY = "test-auditor-key"

VALID_SCENARIO = {
    "supplier_id": "SUP-0104",
    "duration_days": 14,
    "objective": "MINIMIZE_SLA_BREACH",
}


@pytest.fixture
def client():
    scenario_service.scenarios.clear()
    idempotency_engine.idempotency_keys.clear()
    audit_service.audits.clear()
    audit_service.replays.clear()

    with TestClient(app) as test_client:
        yield test_client


def operator() -> dict[str, str]:
    return {"X-API-Key": OPERATOR_KEY}


def auditor() -> dict[str, str]:
    return {"X-API-Key": AUDITOR_KEY}


# --------------------------------------------------------------------------- auth


def test_unauthenticated_read_is_rejected(client):
    response = client.get("/api/v1/scenarios/SCN-1")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "ApiKey"


def test_unauthenticated_write_is_rejected(client):
    response = client.post("/api/v1/scenarios", json=VALID_SCENARIO)

    assert response.status_code == 401


def test_wrong_api_key_is_rejected(client):
    response = client.get("/api/v1/scenarios/SCN-1", headers={"X-API-Key": "not-the-key"})

    assert response.status_code == 401


def test_operator_key_can_write(client):
    response = client.post("/api/v1/scenarios", json=VALID_SCENARIO, headers=operator())

    assert response.status_code == 200
    assert response.json()["data"]["scenario_id"].startswith("SCN-")


def test_auditor_cannot_write(client):
    response = client.post("/api/v1/scenarios", json=VALID_SCENARIO, headers=auditor())

    assert response.status_code == 403


def test_auditor_can_read_audit_records(client):
    audit_service.record_decision("DEC-1", {"revenue_at_risk": "1600000.00", "sla": 2})

    response = client.get("/api/v1/audit/DEC-1", headers=auditor())

    assert response.status_code == 200
    assert response.json()["data"]["integrity_verified"] is True


def test_operator_cannot_read_audit_records(client):
    response = client.get("/api/v1/audit/DEC-1", headers=operator())

    assert response.status_code == 403


def test_security_headers_are_present(client):
    response = client.get("/api/v1/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Cache-Control"] == "no-store"


# --------------------------------------------------------------------------- audit


def test_unknown_decision_is_not_fabricated(client):
    response = client.get("/api/v1/audit/DOES-NOT-EXIST", headers=auditor())

    assert response.status_code == 404


def test_replay_of_unknown_decision_is_404(client):
    response = client.post("/api/v1/replay/DOES-NOT-EXIST", headers=auditor())

    assert response.status_code == 404


def test_tampered_audit_record_fails_integrity_check():
    service = AuditService()
    sealed = service.record_decision("DEC-2", {"revenue_at_risk": "1600000.00", "sla": 2})
    assert sealed["integrity_verified"] is True

    service.audits["DEC-2"]["payload"]["sla"] = 0
    tampered = service.get_audit("DEC-2")

    assert tampered["integrity_verified"] is False
    assert tampered["result_hash"] != tampered["recomputed_hash"]


def test_replay_reports_integrity_failure_for_tampered_record():
    service = AuditService()
    service.record_decision("DEC-3", {"revenue_at_risk": "1600000.00"})
    service.audits["DEC-3"]["payload"]["revenue_at_risk"] = "1.00"

    replay = service.replay_decision("DEC-3")

    assert replay["status"] == "INTEGRITY_FAILURE"
    assert replay["integrity_verified"] is False


# --------------------------------------------------------------------------- input


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"supplier_id": "SUP-0104", "objective": "MINIMIZE_SLA_BREACH"},
        {"supplier_id": "SUP-0104", "duration_days": "fourteen", "objective": "MINIMIZE_SLA_BREACH"},
        {"supplier_id": "SUP-0104", "duration_days": 0, "objective": "MINIMIZE_SLA_BREACH"},
        {"supplier_id": "SUP-0104", "duration_days": 500, "objective": "MINIMIZE_SLA_BREACH"},
        {"supplier_id": "SUP-9999", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"},
        {"supplier_id": "SUP-0104", "duration_days": 14, "objective": "ANYTHING_GOES"},
    ],
)
def test_invalid_scenario_payload_is_rejected(client, payload):
    response = client.post("/api/v1/scenarios", json=payload, headers=operator())

    assert response.status_code == 422


def test_idempotency_key_returns_the_same_decision(client):
    first = client.post(
        "/api/v1/scenarios",
        json=VALID_SCENARIO,
        headers={**operator(), "Idempotency-Key": "key-1"},
    )
    second = client.post(
        "/api/v1/scenarios",
        json=VALID_SCENARIO,
        headers={**operator(), "Idempotency-Key": "key-1"},
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["idempotent_replay"] is True
    assert first.json()["data"]["scenario_id"] == second.json()["data"]["scenario_id"]
