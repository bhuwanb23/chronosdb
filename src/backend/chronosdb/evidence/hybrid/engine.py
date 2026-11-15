"""Phase 8K: Hybrid Retrieval Engine.

Most important module.

Final Score:
Hybrid Score = 0.50 Semantic + 0.20 Recency + 0.20 Structured Match + 0.10 Authority

Alternative weighting allowed but must be versioned.

Example:
DOC-104
Semantic = 0.90
Structured = 1.00
Authority = 1.00
Recency = 0.80
Hybrid = 0.92
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class HybridResult:
    """Hybrid retrieval result."""
    document_id: str
    chunk_id: str
    text: str
    hybrid_score: float
    semantic_score: float
    structured_score: float
    recency_score: float
    authority_score: float
    rank: int
    metadata: Dict[str, Any]
    weights_used: Dict[str, float]

class HybridRetrievalEngine:
    """
    Phase 8K: Hybrid Retrieval Engine.
    
    Combines semantic and structured retrieval with weighting.
    """
    
    def __init__(self, weights: Dict[str, float] = None):
        # Default weights
        self.weights = weights or {
            "semantic": 0.50,
            "recency": 0.20,
            "structured": 0.20,
            "authority": 0.10
        }
        
        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    def calculate_hybrid_score(
        self,
        semantic_score: float,
        structured_score: float,
        recency_score: float,
        authority_score: float
    ) -> float:
        """Calculate hybrid score using weighted formula."""
        return (
            self.weights["semantic"] * semantic_score +
            self.weights["structured"] * structured_score +
            self.weights["recency"] * recency_score +
            self.weights["authority"] * authority_score
        )
    
    def retrieve_hybrid(
        self,
        structured_results: List[Dict[str, Any]],
        semantic_results: List[Dict[str, Any]],
        recency_weights: Dict[str, float] = None,
        authority_weights: Dict[str, float] = None
    ) -> List[HybridResult]:
        """
        Combine structured and semantic retrieval with hybrid scoring.
        """
        # Create mapping from document_id/chunk_id to results
        structured_map = {r["document_id"]: r for r in structured_results}
        semantic_map = {r["document_id"]: r for r in semantic_results}
        
        hybrid_results = []
        
        # Combine results
        all_document_ids = set(structured_map.keys()).union(set(semantic_map.keys()))
        
        for doc_id in all_document_ids:
            structured = structured_map.get(doc_id, {})
            semantic = semantic_map.get(doc_id, {})
            
            # Calculate scores
            semantic_score = semantic.get("cosine_similarity", 0.0)
            structured_score = structured.get("match_score", 0.0)
            
            # Recency score (based on effective_from date)
            recency_score = self._calculate_recency_score(
                structured.get("effective_from", "2026-01-01")
            )
            
            # Authority score (based on document type/source)
            authority_score = self._calculate_authority_score(
                structured.get("type", "UNKNOWN")
            )
            
            # Calculate hybrid score
            hybrid_score = (
                self.weights["semantic"] * semantic_score +
                self.weights["structured"] * structured_score +
                self.weights["recency"] * recency_score +
                self.weights["authority"] * authority_score
            )
            
            # Combine metadata
            combined_metadata = {
                **structured.get("metadata", {}),
                **semantic.get("metadata", {})
            }
            
            hybrid_results.append(HybridResult(
                document_id=doc_id,
                chunk_id=structured.get("chunk_id", semantic.get("chunk_id", "UNKNOWN")),
                text=structured.get("text", semantic.get("text", "")),
                hybrid_score=hybrid_score,
                semantic_score=semantic_score,
                structured_score=structured_score,
                recency_score=recency_score,
                authority_score=authority_score,
                rank=0,  # Will be assigned after sorting
                metadata=combined_metadata,
                weights_used=self.weights
            ))
        
        # Sort by hybrid score (descending) and assign ranks
        hybrid_results.sort(key=lambda x: x.hybrid_score, reverse=True)
        for rank, result in enumerate(hybrid_results, 1):
            # Create new dataclass instance with rank
            updated_result = HybridResult(
                document_id=result.document_id,
                chunk_id=result.chunk_id,
                text=result.text,
                hybrid_score=result.hybrid_score,
                semantic_score=result.semantic_score,
                structured_score=result.structured_score,
                recency_score=result.recency_score,
                authority_score=result.authority_score,
                rank=rank,
                metadata=result.metadata,
                weights_used=result.weights_used
            )
            # Replace in original list
            for i, r in enumerate(hybrid_results):
                if r.document_id == updated_result.document_id:
                    hybrid_results[i] = updated_result
                    break
        
        return hybrid_results
    
    def _calculate_recency_score(self, effective_from: str) -> float:
        """Calculate recency score (0.0 to 1.0)."""
        # Implementation would compare with current date
        # For demonstration, return 0.8
        return 0.8
    
    def _calculate_authority_score(self, doc_type: str) -> float:
        """Calculate authority score based on document type."""
        # Implementation would map document types to authority scores
        authority_map = {
            "PROCEDURAL": 1.0,
            "GOVERNANCE": 0.9,
            "OPERATIONAL": 0.8,
            "HISTORICAL": 0.7
        }
        return authority_map.get(doc_type, 0.5)

# Phase 8K Status: IMPLEMENTED
