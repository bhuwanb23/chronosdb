"""Phase 8O: Retrieval Persistence.

Records:
- RETRIEVAL_RUN
- RETRIEVAL_QUERY
- RETRIEVED_CHUNK
- RANKING_RESULT
- EVIDENCE_PACKAGE

Important: Retrieval must be replayable later.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import json
from datetime import datetime

@dataclass(frozen=True)
class RetrievalRecord:
    """Retrieval persistence record."""
    record_id: str
    record_type: str  # RETRIEVAL_RUN, RETRIEVAL_QUERY, RETRIEVED_CHUNK, RANKING_RESULT, EVIDENCE_PACKAGE
    timestamp: str
    data: Dict[str, Any]
    provenance: Dict[str, Any]

class RetrievalPersistence:
    """
    Phase 8O: Retrieval Persistence.
    
    Persists all retrieval records with complete audit trail.
    Retrieval must be replayable later.
    """
    
    def __init__(self, storage_path: str = "/home/user/chronosdb/config/evidence/persistence/"):
        self.storage_path = storage_path
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory exists."""
        import os
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _generate_record_id(self, record_type: str) -> str:
        """Generate unique record ID."""
        from datetime import datetime
        import uuid
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{record_type}-{timestamp}-{uuid.uuid4().hex[:8].upper()}"
    
    def _save_record(self, record: RetrievalRecord):
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
    def create_retrieval_run(self, run_data: Dict[str, Any], provenance: Dict[str, Any]) -> RetrievalRecord:
        """Create RETRIEVAL_RUN record."""
        record_id = self._generate_record_id("RETRIEVAL_RUN")
        record = RetrievalRecord(
            record_id=record_id,
            record_type="RETRIEVAL_RUN",
            timestamp=datetime.now().isoformat(),
            data=run_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_retrieval_query(self, query_data: Dict[str, Any], provenance: Dict[str, Any]) -> RetrievalRecord:
        """Create RETRIEVAL_QUERY record."""
        record_id = self._generate_record_id("RETRIEVAL_QUERY")
        record = RetrievalRecord(
            record_id=record_id,
            record_type="RETRIEVAL_QUERY",
            timestamp=datetime.now().isoformat(),
            data=query_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_retrieved_chunk(self, chunk_data: Dict[str, Any], provenance: Dict[str, Any]) -> RetrievalRecord:
        """Create RETRIEVED_CHUNK record."""
        record_id = self._generate_record_id("RETRIEVED_CHUNK")
        record = RetrievalRecord(
            record_id=record_id,
            record_type="RETRIEVED_CHUNK",
            timestamp=datetime.now().isoformat(),
            data=chunk_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_ranking_result(self, ranking_data: Dict[str, Any], provenance: Dict[str, Any]) -> RetrievalRecord:
        """Create RANKING_RESULT record."""
        record_id = self._generate_record_id("RANKING_RESULT")
        record = RetrievalRecord(
            record_id=record_id,
            record_type="RANKING_RESULT",
            timestamp=datetime.now().isoformat(),
            data=ranking_data,
            provenance=provenance
        )
        self._save_record(record)
        return record
    
    def create_evidence_package(self, package_data: Dict[str, Any], provenance: Dict[str, Any]) -> RetrievalRecord:
        """Create EVIDENCE_PACKAGE record."""
        record_id = self._generate_record_id("EVIDENCE_PACKAGE")
        record = RetrievalRecord(
            record_id=record_id,
            record_type="EVIDENCE_PACKAGE",
            timestamp=datetime.now().isoformat(),
            data=package_data,
            provenance=provenance
        )
        self._save_record(record)
        return record

# Phase 8O Status: IMPLEMENTED
