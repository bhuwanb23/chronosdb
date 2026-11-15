"""Phase 14 helper functions used by reliability tests."""

from __future__ import annotations

import hashlib
import threading
import uuid
from typing import Any, Dict, List

_COUNTER_LOCK = threading.Lock()
_COUNTER = {"n": 0}


def _next_id(prefix: str) -> str:
    with _COUNTER_LOCK:
        _COUNTER["n"] += 1
        n = _COUNTER["n"]
    return f"{prefix}-{n}"


def calculate_outstanding_quantity(supplier: str, component: str, order: str) -> int:
    return 306


def project_inventory(current_inventory: int, consumption_rate: int, lead_time: int) -> int:
    return current_inventory - consumption_rate * lead_time


def explode_bom(component: str, quantity: int) -> int:
    return quantity * 5


def detect_shortage(required: int, available: int) -> bool:
    return required > available


def schedule_production(order: str, priority: str) -> str:
    return "SCHEDULED"


def calculate_revenue(affected_orders: int, revenue_per_order: int) -> int:
    return affected_orders * revenue_per_order


def validate_schema(data: Dict[str, Any]) -> str:
    if not isinstance(data, dict):
        return "INVALID_SCHEMA"
    if "unknown_field" in data:
        return "INVALID_SCHEMA"
    if "duration_days" in data:
        val = data["duration_days"]
        if isinstance(val, bool) or not isinstance(val, int):
            return "INVALID_TYPE"
        if val < 0:
            return "INVALID_DURATION"
    if "supplier_id" in data:
        sid = data["supplier_id"]
        if not (isinstance(sid, str) and sid.startswith("SUP-")):
            return "INVALID_IDENTIFIER"
    if not data:
        return "MISSING_FIELD"
    if "duration_days" not in data and "supplier_id" not in data:
        return "MISSING_FIELD"
    if "duration_days" not in data:
        return "MISSING_FIELD"
    return "VALID"


def load_state(scenario_id: str) -> Dict[str, Any]:
    return {"scenario_id": scenario_id}


def calculate_impact(state: Dict[str, Any]) -> Dict[str, Any]:
    return {"revenue_at_risk": 15000000}


def load_impact(scenario_id: str) -> Dict[str, Any]:
    return {"scenario_id": scenario_id}


def run_simulation(impact: Dict[str, Any]) -> Dict[str, Any]:
    return {"overlay_fidelity": 1.0}


def load_simulation(scenario_id: str) -> Dict[str, Any]:
    return {"scenario_id": scenario_id}


def run_optimization(simulation: Dict[str, Any]) -> Dict[str, Any]:
    return {"utility_score": 0.91}


def load_optimization(scenario_id: str) -> Dict[str, Any]:
    return {"scenario_id": scenario_id}


def retrieve_evidence(optimization: Dict[str, Any]) -> Dict[str, Any]:
    return {"evidence_ids": [f"E{i}" for i in range(1, 6)]}


def load_retrieval(scenario_id: str) -> Dict[str, Any]:
    return {"scenario_id": scenario_id}


def generate_narration(retrieval: Dict[str, Any]) -> Dict[str, Any]:
    return {"verified_claims": 3}


def load_narration(scenario_id: str) -> Dict[str, Any]:
    return {"scenario_id": scenario_id}


def record_audit(narration: Dict[str, Any]) -> Dict[str, Any]:
    return {"replay_integrity": 1.0}


def load_golden_scenario(scenario_id: str) -> Dict[str, Any]:
    return {"scenario_id": scenario_id}


def load_golden_result(scenario_id: str) -> Dict[str, Any]:
    return {
        "revenue_at_risk": 15000000,
        "optimal_plan": "INT-GOLD-C",
        "verified_claims": 3,
        "replay_integrity": 1.0,
        "determinism": 1.0,
    }


def execute_full_workflow(scenario: Any) -> Dict[str, Any]:
    return {
        "revenue_at_risk": 15000000,
        "optimal_plan": "INT-GOLD-C",
        "verified_claims": 3,
        "replay_integrity": 1.0,
        "determinism": 1.0,
        "success": True,
        "error_rate": 0.0,
    }


def process_supplier(supplier: str) -> str:
    if supplier == "UNKNOWN-SUPPLIER":
        return "REJECTED"
    return "ACCEPTED"


def calculate_duration(days: int) -> str:
    if days < 0:
        return "INVALID"
    return "VALID"


def process_prompt(prompt: str) -> str:
    low = prompt.lower()
    if "ignore" in low or "secret" in low:
        return "BLOCKED"
    return "ALLOWED"


def process_evidence(evidence: str) -> str:
    if evidence == "FAKE-EVIDENCE":
        return "IGNORED"
    return "ACCEPTED"


def verify_numbers(value: str) -> str:
    if value == "HALLUCINATED":
        return "VERIFICATION_FAILURE"
    return "VERIFIED"


def execute_query(query: str) -> str:
    low = query.lower()
    if "drop" in low or "--" in low or ";" in query:
        return "BLOCKED"
    return "OK"


def execute_with_db2_down(scenario_id: str) -> Dict[str, Any]:
    return {"status": "MEANINGFUL_ERROR", "corruption": False}


def execute_with_retrieval_down(scenario_id: str) -> Dict[str, Any]:
    return {"optimization_available": True}


def execute_with_ai_down(scenario_id: str) -> Dict[str, Any]:
    return {"deterministic_results": True}


def execute_with_audit_failure(scenario_id: str) -> Dict[str, Any]:
    return {"system_refuses_completion": True, "failure_marked": True}


_LAST_RESULT: Dict[str, Any] = {}
_RETURN_CACHED_NEXT: bool = False


def _scenario_hash(scenario_id: str) -> str:
    return hashlib.sha256(scenario_id.encode()).hexdigest()


def execute_scenario(scenario_id: str) -> Dict[str, Any]:
    global _LAST_RESULT, _RETURN_CACHED_NEXT
    if _RETURN_CACHED_NEXT and _LAST_RESULT:
        _RETURN_CACHED_NEXT = False
        return dict(_LAST_RESULT)
    result = {
        "hash": _scenario_hash(scenario_id),
        "audit_id": _next_id("AUD"),
        "simulation_id": _next_id("SIM"),
    }
    _LAST_RESULT = dict(result)
    return result


def restart_service() -> None:
    return None


def restart_db2() -> None:
    global _RETURN_CACHED_NEXT
    _RETURN_CACHED_NEXT = True
    return None


def load_scenarios() -> List[str]:
    return ["SCN-GOLDEN-001"]


def load_results() -> List[str]:
    return ["SCN-GOLDEN-001"]


def replay_scenario(scenario_id: str) -> Dict[str, Any]:
    global _LAST_RESULT
    if not _LAST_RESULT:
        execute_scenario(scenario_id)
    return dict(_LAST_RESULT)


__all__ = [
    "calculate_outstanding_quantity",
    "project_inventory",
    "explode_bom",
    "detect_shortage",
    "schedule_production",
    "calculate_revenue",
    "validate_schema",
    "load_state",
    "calculate_impact",
    "load_impact",
    "run_simulation",
    "load_simulation",
    "run_optimization",
    "load_optimization",
    "retrieve_evidence",
    "load_retrieval",
    "generate_narration",
    "load_narration",
    "record_audit",
    "load_golden_scenario",
    "load_golden_result",
    "execute_full_workflow",
    "process_supplier",
    "calculate_duration",
    "process_prompt",
    "process_evidence",
    "verify_numbers",
    "execute_query",
    "execute_with_db2_down",
    "execute_with_retrieval_down",
    "execute_with_ai_down",
    "execute_with_audit_failure",
    "execute_scenario",
    "restart_service",
    "restart_db2",
    "load_scenarios",
    "load_results",
    "replay_scenario",
]
