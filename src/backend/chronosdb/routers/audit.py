"""
Phase 11J: Audit and Replay Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.backend.chronosdb.services.audit_service import AuditService

router = APIRouter(prefix="/api/v1", tags=["audit"])
service = AuditService()

@router.get("/audit/{decision_id}", response_model=Dict[str, Any])
async def get_audit(decision_id: str):
    """
    GET /api/v1/audit/{decision_id}
    """
    audit = service.get_audit(decision_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": audit}

@router.post("/replay/{decision_id}", response_model=Dict[str, Any])
async def replay_decision(decision_id: str):
    """
    POST /api/v1/replay/{decision_id}
    """
    result = service.replay_decision(decision_id)
    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": result}

# Phase 11J Status: ✅ COMPLETE
