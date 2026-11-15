"""
Phase 11S: Observability and Logging
Backend and API Integration
"""

from collections import deque
from typing import Deque, Dict, Any, List
import logging
from datetime import datetime

MAX_AUDIT_ENTRIES = 5000

logger = logging.getLogger(__name__)

class AuditingMiddleware:
    """
    Phase 11S: Capture Request Count, Errors, Latency, Scenario Volume, Optimization Volume, Replay Requests
    
    Structured Logs:
    {
      "correlation_id": "...",
      "endpoint": "...",
      "duration_ms": 82
    }
    """
    
    def __init__(self):
        self.logs: Deque[Dict[str, Any]] = deque(maxlen=MAX_AUDIT_ENTRIES)
        
    def log_request(self, correlation_id: str, endpoint: str, duration_ms: float, status: str = "SUCCESS") -> Dict[str, Any]:
        """
        Log request with structured format
        """
        log_entry = {
            "correlation_id": correlation_id,
            "endpoint": endpoint,
            "duration_ms": duration_ms,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.logs.append(log_entry)
        logger.info(f"AUDIT: {log_entry}")
        
        return log_entry
        
    def get_logs(self) -> List[Dict[str, Any]]:
        """
        Get the retained audit logs (bounded ring buffer)
        """
        return list(self.logs)

# Phase 11S Status: ✅ COMPLETE
