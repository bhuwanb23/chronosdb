"""
Phase 11G: Optimization Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
<<<<<<< HEAD
from src.backend.chronosdb.optimization.contracts import OptimizationError
=======
from src.backend.chronosdb.api.security import READ, WRITE, require_scope
from src.backend.chronosdb.services.audit_service import audit_service
>>>>>>> 7472946a8e1181b45b704f201a36608e260cc041
from src.backend.chronosdb.services.optimization_service import OptimizationService

router = APIRouter(prefix="/api/v1", tags=["optimization"])
service = OptimizationService()

<<<<<<< HEAD
@router.post("/scenarios/{scenario_id}/optimize", response_model=Dict[str, Any])
async def optimize(scenario_id: str, request: Request):
=======
@router.post(
    "/scenarios/{scenario_id}/optimize",
    response_model=Dict[str, Any],
    dependencies=[Depends(require_scope(WRITE))],
)
async def optimize(scenario_id: str):
>>>>>>> 7472946a8e1181b45b704f201a36608e260cc041
    """
    POST /api/v1/scenarios/{id}/optimize
    Response: {recommended_candidate, utility_score}
    """
<<<<<<< HEAD
    try:
        result = service.optimize(scenario_id)
    except OptimizationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": result,
    }

@router.get("/optimization/{optimization_id}/candidates", response_model=Dict[str, Any])
async def get_candidates(optimization_id: str, request: Request):
=======
    result = service.optimize(scenario_id)
    audit_service.record_decision(result["optimization_id"], result)
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": result}

@router.get(
    "/optimization/{optimization_id}/candidates",
    response_model=Dict[str, Any],
    dependencies=[Depends(require_scope(READ))],
)
async def get_candidates(optimization_id: str):
>>>>>>> 7472946a8e1181b45b704f201a36608e260cc041
    """
    GET /api/v1/optimization/{id}/candidates
    """
    candidates = service.get_candidates(optimization_id)
    if not candidates:
        raise HTTPException(status_code=404, detail="Optimization not found")
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": candidates,
    }

# Phase 11G Status: ✅ COMPLETE
