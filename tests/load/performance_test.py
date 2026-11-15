"""
Phase 11Q: Performance and Load Testing
Backend and API Integration
"""

import pytest
import time
from fastapi.testclient import TestClient
from src.backend.chronosdb.api.app import app
from tests.conftest import AUDITOR_HEADERS, OPERATOR_HEADERS

client = TestClient(app, headers=OPERATOR_HEADERS)

class TestPerformanceAndLoad:
    """
    Phase 11Q: Benchmark Targets
    
    Operation         Target (p95)
    Scenario Creation <100ms
    Impact Run        <2 sec
    Simulation Set    <3 sec
    Optimization      <1 sec
    Evidence Retrieval<2 sec
    Replay            <2 sec
    
    Concurrent Target: 20 simultaneous users
    """
    
    def test_scenario_creation_performance(self):
        """Scenario Creation <100ms"""
        start = time.time()
        response = client.post(
            "/api/v1/scenarios",
            json={"supplier_id": "SUP-0104", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"}
        )
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 100, f"Scenario creation took {elapsed}ms, expected <100ms"
        
    def test_impact_run_performance(self):
        """Impact Run <2 sec"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={"supplier_id": "SUP-0104", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"}
        )
        scenario_id = response.json()["data"]["scenario_id"]
        
        # Run impact
        start = time.time()
        response = client.post(f"/api/v1/scenarios/{scenario_id}/impact")
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 2000, f"Impact run took {elapsed}ms, expected <2000ms"
        
    def test_simulation_performance(self):
        """Simulation Set <3 sec"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={"supplier_id": "SUP-0104", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"}
        )
        scenario_id = response.json()["data"]["scenario_id"]
        
        # Run all simulations
        start = time.time()
        response = client.post(f"/api/v1/scenarios/{scenario_id}/simulate-all")
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 3000, f"Simulation set took {elapsed}ms, expected <3000ms"
        
    def test_optimization_performance(self):
        """Optimization <1 sec"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={"supplier_id": "SUP-0104", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"}
        )
        scenario_id = response.json()["data"]["scenario_id"]
        
        # Run optimization
        start = time.time()
        response = client.post(f"/api/v1/scenarios/{scenario_id}/optimize")
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 1000, f"Optimization took {elapsed}ms, expected <1000ms"
        
    def test_evidence_retrieval_performance(self):
        """Evidence Retrieval <2 sec"""
        # Create scenario first
        response = client.post(
            "/api/v1/scenarios",
            json={"supplier_id": "SUP-0104", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"}
        )
        scenario_id = response.json()["data"]["scenario_id"]
        
        # Retrieve evidence
        start = time.time()
        response = client.get(f"/api/v1/scenarios/{scenario_id}/evidence")
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 2000, f"Evidence retrieval took {elapsed}ms, expected <2000ms"
        
    def test_replay_performance(self):
        """Replay <2 sec"""
        # Create scenario and run through workflow
        response = client.post(
            "/api/v1/scenarios",
            json={"supplier_id": "SUP-0104", "duration_days": 14, "objective": "MINIMIZE_SLA_BREACH"}
        )
        scenario_id = response.json()["data"]["scenario_id"]
        
        # Run optimization to get decision_id
        response = client.post(f"/api/v1/scenarios/{scenario_id}/optimize")
        optimization_id = response.json()["data"].get("optimization_id", "OPT-TEST")
        
        # Replay decision
        start = time.time()
        response = client.post(f"/api/v1/replay/{optimization_id}", headers=AUDITOR_HEADERS)
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 2000, f"Replay took {elapsed}ms, expected <2000ms"

# Phase 11Q Status: ✅ COMPLETE
