"""
Phase 11F: Simulation Service Router
Backend and API Integration
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.backend.chronosdb.api.security import WRITE, require_scope
from src.backend.chronosdb.services.simulation_service import SimulationService

router = APIRouter(prefix="/api/v1/scenarios", tags=["simulations"])
service = SimulationService()


@router.post(
    "/{scenario_id}/simulate",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(WRITE))],
)
async def run_simulation(
    scenario_id: str,
    request: dict[str, Any],
    http_request: Request,
):
    """
    POST /api/v1/scenarios/{id}/simulate
    Request: {intervention}
    Response: {simulation_id}
    """
    intervention = request.get("intervention")
    if not intervention:
        raise HTTPException(status_code=400, detail="Missing intervention")

    result = service.run_simulation(scenario_id, intervention)
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(http_request.state, "correlation_id", ""),
        "data": result,
    }


@router.post(
    "/{scenario_id}/simulate-all",
    response_model=dict[str, Any],
    dependencies=[Depends(require_scope(WRITE))],
)
async def run_all_simulations(scenario_id: str, request: Request):
    """
    POST /api/v1/scenarios/{id}/simulate-all
    Returns: Transfer, Expedite, Supplier, Reschedule, Hybrid
    """
    result = service.run_all_simulations(scenario_id)
    return {
        "status": "SUCCESS",
        "correlation_id": getattr(request.state, "correlation_id", ""),
        "data": result,
    }


# Phase 11F Status: ✅ COMPLETE
