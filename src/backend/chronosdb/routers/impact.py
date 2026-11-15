"""
Phase 11E: Impact Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.backend.chronosdb.api.security import READ, WRITE, require_scope
from src.backend.chronosdb.services.impact_service import ImpactService

router = APIRouter(prefix="/api/v1", tags=["impact"])
service = ImpactService()

@router.post(
    "/scenarios/{scenario_id}/impact",
    response_model=Dict[str, Any],
    dependencies=[Depends(require_scope(WRITE))],
)
async def run_impact(scenario_id: str):
    """
    POST /api/v1/scenarios/{id}/impact
    Output: {impact_run_id, revenue_at_risk}
    """
    result = service.run_impact(scenario_id)
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": result}

@router.get("/impact/{impact_run_id}", response_model=Dict[str, Any], dependencies=[Depends(require_scope(READ))])
async def get_impact(impact_run_id: str):
    """
    GET /api/v1/impact/{id}
    """
    impact = service.get_impact(impact_run_id)
    if not impact:
        raise HTTPException(status_code=404, detail="Impact run not found")
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": impact}

# Phase 11E Status: ✅ COMPLETE
