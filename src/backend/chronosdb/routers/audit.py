"""
Phase 11J: Audit and Replay Service Router
Backend and API Integration
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.backend.chronosdb.api.security import AUDIT, require_scope
from src.backend.chronosdb.services.audit_service import audit_service as service

router = APIRouter(prefix="/api/v1", tags=["audit"])


@router.get(
    "/audit/{decision_id}",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(AUDIT))],
)
async def get_audit(decision_id: str, request: Request):
    """
    GET /api/v1/audit/{decision_id}
    """
    audit = service.get_audit(decision_id)
    if audit is None:
        raise HTTPException(status_code=404, detail="Audit record not found")
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": audit,
    }


@router.post(
    "/replay/{decision_id}",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(AUDIT))],
)
async def replay_decision(decision_id: str, request: Request):
    """
    POST /api/v1/replay/{decision_id}
    """
    result = service.replay_decision(decision_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Audit record not found")
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": result,
    }


# Phase 11J Status: ✅ COMPLETE
