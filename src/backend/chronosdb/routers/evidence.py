"""
Phase 11H: Evidence Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.backend.chronosdb.api.security import READ, require_scope
from src.backend.chronosdb.services.evidence_service import EvidenceService

router = APIRouter(prefix="/api/v1", tags=["evidence"])
service = EvidenceService()

@router.get(
    "/scenarios/{scenario_id}/evidence",
    response_model=Dict[str, Any],
    dependencies=[Depends(require_scope(READ))],
)
async def retrieve_evidence(scenario_id: str):
    """
    GET /api/v1/scenarios/{id}/evidence
    Response: {operational, policies, historical_incidents}
    """
    result = service.retrieve_evidence(scenario_id)
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": result}

@router.get("/evidence/{evidence_id}", response_model=Dict[str, Any], dependencies=[Depends(require_scope(READ))])
async def get_evidence_package(evidence_id: str):
    """
    GET /api/v1/evidence/{id}
    """
    package = service.get_evidence_package(evidence_id)
    if not package:
        raise HTTPException(status_code=404, detail="Evidence package not found")
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": package}

# Phase 11H Status: ✅ COMPLETE
