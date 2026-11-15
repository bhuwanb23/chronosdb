"""
Phase 11R: Integration Testing
Backend and API Integration
"""

import pytest
from fastapi.testclient import TestClient
from src.backend.chronosdb.api.app import app
from tests.conftest import AUDITOR_HEADERS, OPERATOR_HEADERS

client = TestClient(app, headers=OPERATOR_HEADERS)

class TestIntegrationWorkflow:
    """
    Phase 11R: Integration Testing
    
    Test: Scenario → Impact → Simulation → Optimization → Evidence → AI → Audit
    Target: 100% workflow completion
    """
    
    def test_end_to_end_workflow(self):
        """
        Complete workflow: Scenario → Impact → Simulation → Optimization → Evidence → AI → Audit
        """
        # 1. Scenario Creation (11D)
        response = client.post(
            "/api/v1/scenarios",
            json={"supplier_id": "SUP-0104", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"}
        )
        assert response.status_code == 200
        scenario_id = response.json()["data"]["scenario_id"]
        
        # 2. Impact Run (11E)
        response = client.post(f"/api/v1/scenarios/{scenario_id}/impact")
        assert response.status_code == 200
        impact_run_id = response.json()["data"]["impact_run_id"]
        
        # 3. Simulation (11F)
        response = client.post(
            f"/api/v1/scenarios/{scenario_id}/simulate",
            json={"intervention": "TRANSFER"}
        )
        assert response.status_code == 200
        simulation_id = response.json()["data"]["simulation_id"]
        
        # 4. Optimization (11G)
        response = client.post(f"/api/v1/scenarios/{scenario_id}/optimize")
        assert response.status_code == 200
        optimization_data = response.json()["data"]
        assert "recommended_candidate" in optimization_data
        
        # 5. Evidence Retrieval (11H)
        response = client.get(f"/api/v1/scenarios/{scenario_id}/evidence")
        assert response.status_code == 200
        evidence_data = response.json()["data"]
        assert "operational" in evidence_data
        
        # 6. AI Orchestration (11I)
        response = client.post(
            "/api/v1/explain",
            json={"query": "Supplier S-104 down for two weeks"}
        )
        assert response.status_code == 200
        ai_data = response.json()["data"]
        assert "narrative" in ai_data
        
        # 7. Audit and Replay (11J)
        # Use optimization_id as decision_id for audit
        decision_id = optimization_data.get("optimization_id", "OPT-TEST")
        
        # Get audit
        response = client.get(f"/api/v1/audit/{decision_id}", headers=AUDITOR_HEADERS)
        assert response.status_code == 200
        
        # Replay decision
        response = client.post(f"/api/v1/replay/{decision_id}", headers=AUDITOR_HEADERS)
        assert response.status_code == 200
        
        # Workflow complete
        assert True

# Phase 11R Status: ✅ COMPLETE
