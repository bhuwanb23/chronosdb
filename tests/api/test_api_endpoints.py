"""
Phase 11: API Endpoint Tests
Backend and API Integration
"""

from fastapi.testclient import TestClient

from src.backend.chronosdb.api.app import app
from tests.conftest import AUDITOR_HEADERS, OPERATOR_HEADERS

client = TestClient(app, headers=OPERATOR_HEADERS)


class TestAPIEndpoints:
    """Phase 11: API Endpoint Tests"""

    def test_health_endpoint(self):
        """Test /health endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["data"]["status"] == "HEALTHY"
        assert "correlation_id" in data

    def test_readiness_endpoint(self):
        """Test /readiness endpoint"""
        response = client.get("/api/v1/readiness")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["data"]["status"] == "READY"
        assert "correlation_id" in data

    def test_scenario_creation(self):
        """Test POST /api/v1/scenarios"""
        response = client.post(
            "/api/v1/scenarios",
            json={
                "supplier_id": "SUP-0104",
                "duration_days": 14,
                "objective": "MINIMIZE_SLA_BREACH",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "scenario_id" in data["data"]
        assert "correlation_id" in data

    def test_scenario_get(self):
        """Test GET /api/v1/scenarios/{id}"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={
                "supplier_id": "SUP-0104",
                "duration_days": 14,
                "objective": "MINIMIZE_SLA_BREACH",
            },
        )
        scenario_id = response.json()["data"]["scenario_id"]

        # Get scenario
        response = client.get(f"/api/v1/scenarios/{scenario_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["data"]["scenario_id"] == scenario_id

    def test_impact_run(self):
        """Test POST /api/v1/scenarios/{id}/impact"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={
                "supplier_id": "SUP-0104",
                "duration_days": 14,
                "objective": "MINIMIZE_SLA_BREACH",
            },
        )
        scenario_id = response.json()["data"]["scenario_id"]

        # Run impact
        response = client.post(f"/api/v1/scenarios/{scenario_id}/impact")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "impact_run_id" in data["data"]
        assert "revenue_at_risk" in data["data"]

    def test_simulation_run(self):
        """Test POST /api/v1/scenarios/{id}/simulate"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={
                "supplier_id": "SUP-0104",
                "duration_days": 14,
                "objective": "MINIMIZE_SLA_BREACH",
            },
        )
        scenario_id = response.json()["data"]["scenario_id"]

        # Run simulation
        response = client.post(
            f"/api/v1/scenarios/{scenario_id}/simulate", json={"intervention": "TRANSFER"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "simulation_id" in data["data"]

    def test_optimization_run(self):
        """Test POST /api/v1/scenarios/{id}/optimize"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={
                "supplier_id": "SUP-0104",
                "duration_days": 14,
                "objective": "MINIMIZE_SLA_BREACH",
            },
        )
        scenario_id = response.json()["data"]["scenario_id"]

        # Run optimization
        response = client.post(f"/api/v1/scenarios/{scenario_id}/optimize")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "recommended_candidate" in data["data"]
        assert "utility_score" in data["data"]
        candidates = client.get(
            f"/api/v1/optimization/{data['data']['optimization_id']}/candidates"
        )
        assert candidates.status_code == 200
        assert candidates.json()["data"]["ranking"]
        other = client.post("/api/v1/scenarios/SCN-OTHER/optimize")
        assert other.status_code == 200
        assert other.json()["data"]["scenario_id"] == "SCN-OTHER"
        assert other.json()["data"]["optimization_id"] != data["data"]["optimization_id"]
        keyed = client.post(
            "/api/v1/scenarios/SCN-IDEMPOTENT/optimize",
            headers={"Idempotency-Key": "optimization-key"},
        )
        replay = client.post(
            "/api/v1/scenarios/SCN-IDEMPOTENT/optimize",
            headers={"Idempotency-Key": "optimization-key"},
        )
        assert keyed.status_code == replay.status_code == 200
        assert replay.json()["idempotent_replay"] is True
        assert (
            keyed.json()["data"]["optimization_id"]
            == replay.json()["data"]["optimization_id"]
        )

    def test_evidence_retrieval(self):
        """Test GET /api/v1/scenarios/{id}/evidence"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={
                "supplier_id": "SUP-0104",
                "duration_days": 14,
                "objective": "MINIMIZE_SLA_BREACH",
            },
        )
        scenario_id = response.json()["data"]["scenario_id"]

        # Retrieve evidence
        response = client.get(f"/api/v1/scenarios/{scenario_id}/evidence")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "operational" in data["data"]

    def test_ai_explanation(self):
        """Test POST /api/v1/explain"""
        response = client.post(
            "/api/v1/explain", json={"query": "Supplier S-104 down for two weeks"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "narrative" in data["data"]
        assert "verification_status" in data["data"]

    def test_audit_and_replay(self):
        """Test GET /api/v1/audit/{id} and POST /api/v1/replay/{id}"""
        # Create scenario and run optimization to get decision_id
        response = client.post(
            "/api/v1/scenarios",
            json={
                "supplier_id": "SUP-0104",
                "duration_days": 14,
                "objective": "MINIMIZE_SLA_BREACH",
            },
        )
        scenario_id = response.json()["data"]["scenario_id"]

        response = client.post(f"/api/v1/scenarios/{scenario_id}/optimize")
        optimization_id = response.json()["data"].get("optimization_id", "OPT-TEST")

        # Get audit
        response = client.get(f"/api/v1/audit/{optimization_id}", headers=AUDITOR_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["data"]["integrity_verified"] is True

        # Replay decision
        response = client.post(f"/api/v1/replay/{optimization_id}", headers=AUDITOR_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"


# Phase 11 Status: ✅ COMPLETE
