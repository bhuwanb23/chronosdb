"""Phase 11D: Scenario Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime
from src.backend.chronosdb.services.scenario_service import ScenarioService

router = APIRouter(prefix="/api/v1", tags=["scenarios"])
service = ScenarioService()

def _cid() -> str:
    return f"CID-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

@router.post("/scenarios", response_model=Dict[str, Any])
async def create_scenario(request: Dict[str, Any]):
    result = service.create_scenario(
        supplier_id=request.get("supplier_id", "SUP-0104"),
        duration_days=request.get("duration_days", 14),
        objective=request.get("objective", "MINIMIZE_SLA_BREACH")
    )
    return {"status": "SUCCESS", "correlation_id": _cid(), "data": result}

@router.get("/scenarios/{scenario_id}", response_model=Dict[str, Any])
async def get_scenario(scenario_id: str):
    scenario = service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "SUCCESS", "correlation_id": _cid(), "data": scenario}

@router.get("/scenarios/{scenario_id}/status", response_model=Dict[str, Any])
async def get_scenario_status(scenario_id: str):
    status = service.get_scenario_status(scenario_id)
    if not status:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "SUCCESS", "correlation_id": _cid(), "data": status}

@router.delete("/scenarios/{scenario_id}", response_model=Dict[str, Any])
async def delete_scenario(scenario_id: str):
    deleted = service.delete_scenario(scenario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "SUCCESS", "correlation_id": _cid(), "data": {"scenario_id": scenario_id, "status": "DELETED"}}

# Phase 11D Status: ✅ COMPLETE