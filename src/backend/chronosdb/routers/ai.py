"""
Phase 11I: AI Orchestration Service Router
Backend and API Integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from src.backend.chronosdb.ai.security import PromptRejectedError
from src.backend.chronosdb.api.security import WRITE, require_scope
from src.backend.chronosdb.services.ai_service import AIService

router = APIRouter(prefix="/api/v1", tags=["ai"])
service = AIService()

@router.post("/explain", response_model=Dict[str, Any], dependencies=[Depends(require_scope(WRITE))])
async def explain(request: Dict[str, Any]):
    """
    POST /api/v1/explain
    Request: {query}
    Response: {narrative, verification_status}
    """
    query = request.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing query")

    try:
        result = service.explain(query)
    except PromptRejectedError as rejected:
        raise HTTPException(status_code=403, detail=f"Query rejected: {rejected.reason}") from rejected

    return {"status": "SUCCESS", "correlation_id": "CID-PLACEHOLDER", "data": result}

# Phase 11I Status: ✅ COMPLETE
