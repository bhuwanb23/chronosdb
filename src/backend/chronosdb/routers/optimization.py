"""
Phase 11G: Optimization Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.backend.chronosdb.services.optimization_service import OptimizationService

router = APIRouter(prefix="/api/v1", tags=["optimization"])
service = OptimizationService()

@router.post("/scenarios/{scenario_id}/optimize", response_model=Dict[str, Any])
async def optimize(scenario_id: str):
    """
    POST /api/v1/scenarios/{id}/optimize
    Response: {recommended_candidate, utility_score}
    """
    result = service.optimize(scenario_id)
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": result}

@router.get("/optimization/{optimization_id}/candidates", response_model=Dict[str, Any])
async def get_candidates(optimization_id: str):
    """
    GET /api/v1/optimization/{id}/candidates
    """
    candidates = service.get_candidates(optimization_id)
    if not candidates:
        raise HTTPException(status_code=404, detail="Optimization not found")
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": candidates}

# Phase 11G Status: ✅ COMPLETE
