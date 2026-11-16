"""Phase 11D: Scenario Service Router
Backend and API Integration
"""

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from src.backend.chronosdb.api.security import READ, WRITE, require_scope
from src.backend.chronosdb.middleware.idempotency import (
    IdempotencyConflictError,
    IdempotencyEngine,
)
from src.backend.chronosdb.middleware.validation import ValidationFramework
from src.backend.chronosdb.services.scenario_service import ScenarioService

router = APIRouter(prefix="/api/v1", tags=["scenarios"])
service = ScenarioService()
idempotency = IdempotencyEngine()
validation = ValidationFramework()

def _cid(request: Request) -> str:
    return getattr(request.state, "correlation_id", "")

@router.post(
    "/scenarios",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(WRITE))],
)
async def create_scenario(
    request: dict[str, Any],
    http_request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    request_hash = idempotency.generate_request_hash(request)
    if idempotency_key:
        try:
            cached = idempotency.check_idempotency(idempotency_key, request_hash)
        except IdempotencyConflictError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        if cached is not None:
            return {
                **cached,
                "correlation_id": _cid(http_request),
                "idempotent_replay": True,
            }
    result = validation.validate_scenario(request)
    if result["status"] == "INVALID":
        raise HTTPException(status_code=422, detail=result["errors"])
    result = service.create_scenario(
        supplier_id=request.get("supplier_id", "SUP-0104"),
        duration_days=request.get("duration_days", 14),
        objective=request.get("objective", "MINIMIZE_SLA_BREACH")
    )
    response = {
        "status": "SUCCESS",
        "correlation_id": _cid(http_request),
        "data": result,
    }
    if idempotency_key:
        idempotency.store_result(idempotency_key, request_hash, response)
    return response

@router.get(
    "/scenarios/{scenario_id}",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(READ))],
)
async def get_scenario(scenario_id: str, request: Request):
    scenario = service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "SUCCESS", "correlation_id": _cid(request), "data": scenario}

@router.get(
    "/scenarios/{scenario_id}/status",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(READ))],
)
async def get_scenario_status(scenario_id: str, request: Request):
    status = service.get_scenario_status(scenario_id)
    if not status:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "SUCCESS", "correlation_id": _cid(request), "data": status}

@router.delete(
    "/scenarios/{scenario_id}",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(WRITE))],
)
async def delete_scenario(scenario_id: str, request: Request):
    deleted = service.delete_scenario(scenario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {
        "status": "SUCCESS",
        "correlation_id": _cid(request),
        "data": {"scenario_id": scenario_id, "status": "DELETED"},
    }

# Phase 11D Status: ✅ COMPLETE