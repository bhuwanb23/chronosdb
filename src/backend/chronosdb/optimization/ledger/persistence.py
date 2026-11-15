"""Phase 7N: Persistence and Optimization Ledger.

Records:
- OPTIMIZATION_RUN
- OPTIMIZATION_INPUT
- CANDIDATE_SCORE
- CONSTRAINT_RESULT
- PARETO_RESULT
- RECOMMENDATION
- SENSITIVITY_RESULT
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

@dataclass(frozen=True)
class OptimizationRecord:
    """Optimization ledger record."""
    record_id: str
    record_type: str  # OPTIMIZATION_RUN, INPUT, SCORE, CONSTRAINT, PARETO, RECOMMENDATION, SENSITIVITY
    timestamp: str
    data: Dict[str, Any]
    provenance: Dict[str, Any]

class OptimizationLedger:
    """
    Phase 7N: Persistence and Optimization Ledger.
    
    Persists all optimization records with complete audit trail.
    """
    
    def __init__(self, storage_path: str = "/home/user/chronosdb/config/optimization/ledger/"):
        self.storage_path = storage_path
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory exists."""
        import os
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _generate_record_id(self, record_type: str) -> str:
        """Generate unique record ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        import uuid
        return f"{record_type}-{timestamp}-{uuid.uuid4().hex[:8].upper()}"
    
    def _save_record(self, record: OptimizationRecord):
        """Save record to storage."""
        filename = f"{record.record_id}.json"
        filepath = f"{self.storage_path}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump({
                "record_id": record.record_id,
                "record_type": record.record_type,
                "timestamp": record.timestamp,
                "data": record.data,
                "provenance": record.provenance
            }, f, indent=2)
    
    # Record creation methods
    def create_optimization_run(self, input_data: Dict[str, Any], provenance: Dict[str, Any]) -> OptimizationRecord:
        """Create OPTIMIZATION_RUN record."""
        record_id = self._generate_record_id("OPTIMIZATION_RUN")
        record = OptimizationRecord(
            record_id=record_id,
            record_type="OPTIMIZATION_RUN",
            timestamp=datetime.now().isoformat(),
            data=input_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_optimization_input(self, input_data: Dict[str, Any], provenance: Dict[str, Any]) -> OptimizationRecord:
        """Create OPTIMIZATION_INPUT record."""
        record_id = self._generate_record_id("OPTIMIZATION_INPUT")
        record = OptimizationRecord(
            record_id=record_id,
            record_type="OPTIMIZATION_INPUT",
            timestamp=datetime.now().isoformat(),
            data=input_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_candidate_score(self, score_data: Dict[str, Any], provenance: Dict[str, Any]) -> OptimizationRecord:
        """Create CANDIDATE_SCORE record."""
        record_id = self._generate_record_id("CANDIDATE_SCORE")
        record = OptimizationRecord(
            record_id=record_id,
            record_type="CANDIDATE_SCORE",
            timestamp=datetime.now().isoformat(),
            data=score_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_constraint_result(self, constraint_data: Dict[str, Any], provenance: Dict[str, Any]) -> OptimizationRecord:
        """Create CONSTRAINT_RESULT record."""
        record_id = self._generate_record_id("CONSTRAINT_RESULT")
        record = OptimizationRecord(
            record_id=record_id,
            record_type="CONSTRAINT_RESULT",
            timestamp=datetime.now().isoformat(),
            data=constraint_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_pareto_result(self, pareto_data: Dict[str, Any], provenance: Dict[str, Any]) -> OptimizationRecord:
        """Create PARETO_RESULT record."""
        record_id = self._generate_record_id("PARETO_RESULT")
        record = OptimizationRecord(
            record_id=record_id,
            record_type="PARETO_RESULT",
            timestamp=datetime.now().isoformat(),
            data=pareto_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_recommendation(self, recommendation_data: Dict[str, Any], provenance: Dict[str, Any]) -> OptimizationRecord:
        """Create RECOMMENDATION record."""
        record_id = self._generate_record_id("RECOMMENDATION")
        record = OptimizationRecord(
            record_id=record_id,
            record_type="RECOMMENDATION",
            timestamp=datetime.now().isoformat(),
            data=recommendation_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_sensitivity_result(self, sensitivity_data: Dict[str, Any], provenance: Dict[str, Any]) -> OptimizationRecord:
        """Create SENSITIVITY_RESULT record."""
        record_id = self._generate_record_id("SENSITIVITY_RESULT")
        record = OptimizationRecord(
            record_id=record_id,
            record_type="SENSITIVITY_RESULT",
            timestamp=datetime.now().isoformat(),
            data=sensitivity_data,
            provenance=provenance
        )
        self._save_record(record)
        return record

# Phase 7N Status: IMPLEMENTED
