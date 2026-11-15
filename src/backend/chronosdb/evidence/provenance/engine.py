"""Phase 8M: Evidence Provenance Engine.

Every evidence item must carry:
- Document
- Version
- Chunk
- Embedding Model
- Retrieval Score
- Scenario
- Retrieval Run

Example:
{
  "document_id": "DOC-104",
  "chunk_id": "CH-12",
  "version": "2.0",
  "score": 0.92
}
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class EvidenceProvenance:
    """Evidence provenance record."""
    evidence_id: str
    document_id: str
    chunk_id: str
    version: str
    embedding_model: str
    dimension: int
    retrieval_score: float
    scenario_id: str
    retrieval_run_id: str
    ranking_tier: str
    hybrid_score: float
    explanation: str
    timestamp: str

class EvidenceProvenanceEngine:
    """
    Phase 8M: Evidence Provenance Engine.
    
    Generates complete audit trail for evidence retrieval.
    """
    
    def __init__(self):
        pass
    
    def generate_provenance(
        self,
        evidence_id: str,
        document_metadata: Dict[str, Any],
        chunk_data: Dict[str, Any],
        embedding_metadata: Dict[str, Any],
        retrieval_score: float,
        scenario_id: str,
        retrieval_run_id: str,
        ranking_tier: str,
        hybrid_score: float,
        explanation: str
    ) -> EvidenceProvenance:
        """Generate complete evidence provenance."""
        from datetime import datetime
        
        return EvidenceProvenance(
            evidence_id=evidence_id,
            document_id=document_metadata.get("document_id", "UNKNOWN"),
            chunk_id=chunk_data.get("chunk_id", "UNKNOWN"),
            version=document_metadata.get("version", "1.0"),
            embedding_model=embedding_metadata.get("model", "bge-small-en-v1.5"),
            dimension=embedding_metadata.get("dimension", 384),
            retrieval_score=retrieval_score,
            scenario_id=scenario_id,
            retrieval_run_id=retrieval_run_id,
            ranking_tier=ranking_tier,
            hybrid_score=hybrid_score,
            explanation=explanation,
            timestamp=datetime.now().isoformat()
        )
    
    def generate_explanation(
        self,
        evidence_id: str,
        hybrid_score: float,
        tier: str,
        document_metadata: Dict[str, Any],
        chunk_data: Dict[str, Any],
        weights_used: Dict[str, float]
    ) -> str:
        """Generate human-readable explanation."""
        explanation = f"Evidence ID: {evidence_id}\n"
        explanation += f"Tier: {tier}\n"
        explanation += f"Hybrid Score: {hybrid_score:.3f}\n"
        explanation += f"Document: {document_metadata.get('source_document', 'UNKNOWN')} (v{document_metadata.get('version', '1.0')})\n"
        explanation += f"Chunk: {chunk_data.get('section', 'UNKNOWN')}\n"
        explanation += f"Weights Used: {weights_used}\n"
        explanation += f"Classification Reason: Based on score {hybrid_score:.3f} and tier {tier}\n"
        
        return explanation

# Phase 8M Status: IMPLEMENTED
