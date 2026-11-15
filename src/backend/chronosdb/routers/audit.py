"""
Phase 11J: Audit and Replay Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.backend.chronosdb.api.security import AUDIT, require_scope
from src.backend.chronosdb.services.audit_service import audit_service as service

router = APIRouter(prefix="/api/v1", tags=["audit"])

@router.get("/audit/{decision_id}", response_model=Dict[str, Any], dependencies=[Depends(require_scope(AUDIT))])
async def get_audit(decision_id: str):
    """
    GET /api/v1/audit/{decision_id}
    """
    audit = service.get_audit(decision_id)
    if audit is None:
        raise HTTPException(status_code=404, detail="Audit record not found")
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": audit}

@router.post("/replay/{decision_id}", response_model=Dict[str, Any], dependencies=[Depends(require_scope(AUDIT))])
async def replay_decision(decision_id: str):
    """
    POST /api/v1/replay/{decision_id}
    """
    result = service.replay_decision(decision_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Audit record not found")
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": result}

# Phase 11J Status: ✅ COMPLETE
