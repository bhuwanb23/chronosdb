"""
Phase 11G: Optimization Service Router
Backend and API Integration
"""

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from src.backend.chronosdb.api.security import READ, WRITE, require_scope
from src.backend.chronosdb.middleware.idempotency import (
    IdempotencyConflictError,
    IdempotencyEngine,
)
from src.backend.chronosdb.optimization.contracts import OptimizationError
from src.backend.chronosdb.services.audit_service import audit_service
from src.backend.chronosdb.services.optimization_service import OptimizationService

router = APIRouter(prefix="/api/v1", tags=["optimization"])
service = OptimizationService()
idempotency = IdempotencyEngine()

@router.post(
    "/scenarios/{scenario_id}/optimize",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(WRITE))],
)
async def optimize(
    scenario_id: str,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    """
    POST /api/v1/scenarios/{id}/optimize
    Response: {recommended_candidate, utility_score}
    """
    request_payload = {"scenario_id": scenario_id}
    request_hash = idempotency.generate_request_hash(request_payload)
    if idempotency_key:
        try:
            cached = idempotency.check_idempotency(idempotency_key, request_hash)
        except IdempotencyConflictError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        if cached is not None:
            return {
                **cached,
                "correlation_id": getattr(request.state, "correlation_id", ""),
                "idempotent_replay": True,
            }
    try:
        result = service.optimize(scenario_id)
    except OptimizationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    audit_service.record_decision(
        result["optimization_id"],
        result,
    )
    response = {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": result,
    }
    if idempotency_key:
        idempotency.store_result(idempotency_key, request_hash, response)
    return response

@router.get(
    "/optimization/{optimization_id}/candidates",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(READ))],
)
async def get_candidates(optimization_id: str, request: Request):
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
