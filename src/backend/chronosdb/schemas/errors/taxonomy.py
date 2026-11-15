"""
Phase 11L: Error Taxonomy
Backend and API Integration
"""

from typing import Dict, Any

class ErrorTaxonomy:
    """
    Phase 11L: ChronosDB errors standardized
    
    Categories:
    - VALIDATION_ERROR
    - AUTHORIZATION_ERROR
    - EXECUTION_ERROR
    - RETRIEVAL_ERROR
    - OPTIMIZATION_ERROR
    - SYSTEM_ERROR
    """
    
    ERROR_CODES = {
        "VALIDATION_ERROR": "Validation failed",
        "AUTHORIZATION_ERROR": "Unauthorized access",
        "EXECUTION_ERROR": "Execution failed",
        "RETRIEVAL_ERROR": "Retrieval failed",
        "OPTIMIZATION_ERROR": "Optimization failed",
        "SYSTEM_ERROR": "System error",
        "UNKNOWN_SUPPLIER": "Supplier does not exist",
        "INVALID_DURATION": "Invalid duration",
        "INVALID_OBJECTIVE": "Invalid objective",
        "SCENARIO_NOT_FOUND": "Scenario not found",
        "IMPACT_NOT_FOUND": "Impact run not found",
        "SIMULATION_NOT_FOUND": "Simulation not found",
        "OPTIMIZATION_NOT_FOUND": "Optimization not found",
        "EVIDENCE_NOT_FOUND": "Evidence package not found",
        "AUDIT_NOT_FOUND": "Audit not found"
    }
    
    @classmethod
    def get_error_response(cls, error_code: str, message: str = None) -> Dict[str, Any]:
        """
        Response: {error_code, message}
        """
        default_message = cls.ERROR_CODES.get(error_code, "Unknown error")
        return {
            "error_code": error_code,
            "message": message or default_message
        }

# Phase 11L Status: ✅ COMPLETE
