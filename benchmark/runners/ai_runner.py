"""
Phase 13H: Controlled AI Evaluation (Phase 9)
Benchmark and Evaluation System
"""

import json
import os
from typing import Dict, Any

class ControlledAIEvaluator:
    """
    Evaluates Phase 9: Controlled AI Layer
    
    Metrics:
    - Planning: Parse Success (Target: ≥95%)
    - Entity Accuracy (Target: ≥99%)
    - Invalid Input Rejection (Target: 100%)
    - Narration: Verified Claims (Target: 100%)
    - Unsupported Claims (Target: 0%)
    - Evidence Attribution (Target: 100%)
    """
    
    def __init__(self, ground_truth_path: str):
        self.ground_truth = self._load_ground_truth(ground_truth_path)
        self.metrics = {}
    
    def _load_ground_truth(self, path: str) -> Dict[str, Any]:
        """Load frozen ground truth from Phase 12O Golden Scenario"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def evaluate_ai(self, chronosdb_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate Phase 9 Controlled AI Layer
        
        Metrics:
        - Planning: Parse Success (≥95%)
        - Entity Accuracy (≥99%)
        - Invalid Input Rejection (100%)
        - Narration: Verified Claims (100%)
        - Unsupported Claims (0%)
        - Evidence Attribution (100%)
        """
        # Phase 9 Controlled AI Evaluation
        # Compare ChronosDB output with Ground Truth
        
        # Planning: Parse Success
        predicted_parse = chronosdb_output.get('parse_success', 0.0)
        ground_truth_parse = self.ground_truth.get('parse_success', 1.0)
        parse_success = 1.0 if predicted_parse >= 0.95 * ground_truth_parse else 0.0
        
        # Entity Accuracy
        predicted_entities = chronosdb_output.get('entities', [])
        ground_truth_entities = self.ground_truth.get('entities', [])
        correct_entities = len(set(predicted_entities) & set(ground_truth_entities))
        entity_accuracy = correct_entities / len(ground_truth_entities) if ground_truth_entities else 0.0
        
        # Invalid Input Rejection
        predicted_rejection = chronosdb_output.get('invalid_input_rejected', False)
        ground_truth_rejection = self.ground_truth.get('invalid_input_rejected', True)
        invalid_input_rejection = 1.0 if predicted_rejection == ground_truth_rejection else 0.0
        
        # Narration: Verified Claims
        predicted_verified_claims = chronosdb_output.get('verified_claims', 0)
        ground_truth_verified_claims = self.ground_truth.get('verified_claims', 0)
        verified_claims = 1.0 if predicted_verified_claims == ground_truth_verified_claims else 0.0
        
        # Unsupported Claims
        predicted_unsupported = chronosdb_output.get('unsupported_claims', 0)
        ground_truth_unsupported = self.ground_truth.get('unsupported_claims', 0)
        unsupported_claims = 1.0 if predicted_unsupported == ground_truth_unsupported else 0.0
        
        # Evidence Attribution
        predicted_attribution = chronosdb_output.get('evidence_attribution', 0.0)
        ground_truth_attribution = self.ground_truth.get('evidence_attribution', 1.0)
        evidence_attribution = 1.0 if predicted_attribution == ground_truth_attribution else 0.0
        
        self.metrics = {
          'parse_success': parse_success,
          'entity_accuracy': entity_accuracy,
          'invalid_input_rejection': invalid_input_rejection,
          'verified_claims': verified_claims,
          'unsupported_claims': unsupported_claims,
          'evidence_attribution': evidence_attribution,
          'golden_requirement_met': (
            parse_success >= 0.95 and
            entity_accuracy >= 0.99 and
            invalid_input_rejection == 1.0 and
            verified_claims == 1.0 and
            unsupported_claims == 0.0 and
            evidence_attribution == 1.0
          )
        }
        
        return self.metrics

# Phase 13H Status: ✅ COMPLETE
