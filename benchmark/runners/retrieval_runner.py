"""
Phase 13G: Retrieval Evaluation (Phase 8)
Benchmark and Evaluation System
"""

import json
import os
from typing import Dict, Any

class RetrievalEvaluator:
    """
    Evaluates Phase 8: Evidence Retrieval Layer
    
    Metrics:
    - Recall@5: Target ≥0.85
    - Precision@5: Target ≥0.80
    - Mean Reciprocal Rank (MRR): Target ≥0.80
    - Metadata Accuracy: Target 100%
    - Unsupported Source Rate: Target 0%
    """
    
    def __init__(self, ground_truth_path: str):
        self.ground_truth = self._load_ground_truth(ground_truth_path)
        self.metrics = {}
    
    def _load_ground_truth(self, path: str) -> Dict[str, Any]:
        """Load frozen ground truth from Phase 12O Golden Scenario"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def evaluate_retrieval(self, chronosdb_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate Phase 8 Evidence Retrieval Layer
        
        Metrics:
        - Recall@5: ≥0.85
        - Precision@5: ≥0.80
        - Mean Reciprocal Rank: ≥0.80
        - Metadata Accuracy: 100%
        - Unsupported Source Rate: 0%
        """
        # Phase 8 Retrieval Evaluation
        # Compare ChronosDB output with Ground Truth
        
        # Recall@5
        predicted_evidence = chronosdb_output.get('evidence_ids', [])[:5]
        ground_truth_evidence = self.ground_truth.get('evidence_ids', [])
        
        correct_evidence = len(set(predicted_evidence) & set(ground_truth_evidence))
        recall_at_5 = correct_evidence / len(ground_truth_evidence) if ground_truth_evidence else 0.0
        
        # Precision@5
        precision_at_5 = correct_evidence / len(predicted_evidence) if predicted_evidence else 0.0
        
        # Mean Reciprocal Rank (MRR)
        mrr = 0.0
        for i, evidence_id in enumerate(predicted_evidence):
            if evidence_id in ground_truth_evidence:
                mrr = 1.0 / (i + 1)
                break
        
        # Metadata Accuracy
        predicted_metadata = chronosdb_output.get('metadata', {})
        ground_truth_metadata = self.ground_truth.get('metadata', {})
        metadata_accuracy = 1.0 if predicted_metadata == ground_truth_metadata else 0.0
        
        # Unsupported Source Rate
        unsupported_sources = chronosdb_output.get('unsupported_sources', [])
        unsupported_source_rate = len(unsupported_sources) / len(predicted_evidence) if predicted_evidence else 0.0
        
        self.metrics = {
          'recall_at_5': recall_at_5,
          'precision_at_5': precision_at_5,
          'mean_reciprocal_rank': mrr,
          'metadata_accuracy': metadata_accuracy,
          'unsupported_source_rate': unsupported_source_rate,
          'golden_requirement_met': (
            recall_at_5 >= 0.85 and
            precision_at_5 >= 0.80 and
            mrr >= 0.80 and
            metadata_accuracy == 1.0 and
            unsupported_source_rate == 0.0
          )
        }
        
        return self.metrics

# Phase 13G Status: ✅ COMPLETE
