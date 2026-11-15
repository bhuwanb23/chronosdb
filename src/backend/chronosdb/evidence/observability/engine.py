"""Phase 8U: Evidence Observability.

Observability Metrics:
- Retrieval success rate
- Evidence classification distribution
- Security filter violations
- Performance degradation alerts
- Provenance integrity checks

Logs:
- Retrieval run start/end
- Evidence classification
- Security validation
- Performance measurements
- Package creation
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import json
from datetime import datetime

@dataclass(frozen=True)
class ObservabilityLog:
    """Evidence observability log."""
    log_id: str
    timestamp: str
    event_type: str  # RETRIEVAL_START, RETRIEVAL_END, CLASSIFICATION, SECURITY, PERFORMANCE, PACKAGE
    data: Dict[str, Any]
    severity: str  # INFO, WARNING, ERROR
    analysis: Dict[str, Any]

class EvidenceObservability:
    """
    Phase 8U: Evidence Observability.
    
    Provides observability and monitoring for evidence retrieval.
    """
    
    def __init__(self, storage_path: str = "/home/user/chronosdb/config/evidence/observability/"):
        self.storage_path = storage_path
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory exists."""
        import os
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _generate_log_id(self) -> str:
        """Generate unique log ID."""
        from datetime import datetime
        import uuid
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"LOG-{timestamp}-{uuid.uuid4().hex[:8].upper()}"
    
    def _save_log(self, log: ObservabilityLog):
        """Save log to storage."""
        filename = f"{log.log_id}.json"
        filepath = f"{self.storage_path}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump({
                "log_id": log.log_id,
                "timestamp": log.timestamp,
                "event_type": log.event_type,
                "data": log.data,
                "severity": log.severity,
                "analysis": log.analysis
            }, f, indent=2)
    
    # Log creation methods
    def log_retrieval_start(self, run_data: Dict[str, Any]) -> ObservabilityLog:
        """Log retrieval start."""
        log = ObservabilityLog(
            log_id=self._generate_log_id(),
            timestamp=datetime.now().isoformat(),
            event_type="RETRIEVAL_START",
            data=run_data,
            severity="INFO",
            analysis={"status": "started"}
        )
        self._save_log(log)
        return log
    
    def log_retrieval_end(self, run_data: Dict[str, Any], success: bool) -> ObservabilityLog:
        """Log retrieval end."""
        log = ObservabilityLog(
            log_id=self._generate_log_id(),
            timestamp=datetime.now().isoformat(),
            event_type="RETRIEVAL_END",
            data=run_data,
            severity="INFO" if success else "ERROR",
            analysis={"status": "completed" if success else "failed"}
        )
        self._save_log(log)
        return log
    
    def log_classification(self, classification_data: Dict[str, Any]) -> ObservabilityLog:
        """Log evidence classification."""
        log = ObservabilityLog(
            log_id=self._generate_log_id(),
            timestamp=datetime.now().isoformat(),
            event_type="CLASSIFICATION",
            data=classification_data,
            severity="INFO",
            analysis={"status": "classified"}
        )
        self._save_log(log)
        return log
    
    def log_security(self, security_data: Dict[str, Any], violation: bool) -> ObservabilityLog:
        """Log security validation."""
        log = ObservabilityLog(
            log_id=self._generate_log_id(),
            timestamp=datetime.now().isoformat(),
            event_type="SECURITY",
            data=security_data,
            severity="WARNING" if violation else "INFO",
            analysis={"status": "violation" if violation else "passed"}
        )
        self._save_log(log)
        return log
    
    def log_performance(self, performance_data: Dict[str, Any], target_met: bool) -> ObservabilityLog:
        """Log performance measurement."""
        log = ObservabilityLog(
            log_id=self._generate_log_id(),
            timestamp=datetime.now().isoformat(),
            event_type="PERFORMANCE",
            data=performance_data,
            severity="WARNING" if not target_met else "INFO",
            analysis={"status": "target_met" if target_met else "target_missed"}
        )
        self._save_log(log)
        return log
    
    def log_package(self, package_data: Dict[str, Any]) -> ObservabilityLog:
        """Log package creation."""
        log = ObservabilityLog(
            log_id=self._generate_log_id(),
            timestamp=datetime.now().isoformat(),
            event_type="PACKAGE",
            data=package_data,
            severity="INFO",
            analysis={"status": "created"}
        )
        self._save_log(log)
        return log

# Phase 8U Status: IMPLEMENTED
