"""
Phase 11H: Evidence Service Router
Backend and API Integration
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.backend.chronosdb.api.security import READ, require_scope
from src.backend.chronosdb.services.evidence_service import EvidenceService

router = APIRouter(prefix="/api/v1", tags=["evidence"])
service = EvidenceService()


@router.get(
    "/scenarios/{scenario_id}/evidence",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(READ))],
)
async def retrieve_evidence(scenario_id: str, request: Request):
    """
    GET /api/v1/scenarios/{id}/evidence
    Response: {operational, policies, historical_incidents}
    """
    result = service.retrieve_evidence(scenario_id)
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": result,
    }


@router.get(
    "/evidence/{evidence_id}",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(READ))],
)
async def get_evidence_package(evidence_id: str, request: Request):
    """
    GET /api/v1/evidence/{id}
    """
    package = service.get_evidence_package(evidence_id)
    if not package:
        raise HTTPException(status_code=404, detail="Evidence package not found")
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": package,
    }


# Phase 11H Status: ✅ COMPLETE
