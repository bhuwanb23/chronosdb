"""
Phase 13F: Optimization Evaluation (Phase 7)
Benchmark and Evaluation System
"""

import json
import os
from typing import Dict, Any

class OptimizationEvaluator:
    """
    Evaluates Phase 7: Intervention Optimization Engine
    
    Metrics:
    - Feasibility Accuracy: Target 100%
    - Optimal Plan Agreement: Selected Optimal Plan / Benchmark Optimal Plan (Target: ≥90%)
    - Constraint Compliance: 100%
    - Utility Fidelity: 100%
    """
    
    def __init__(self, ground_truth_path: str):
        self.ground_truth = self._load_ground_truth(ground_truth_path)
        self.metrics = {}
    
    def _load_ground_truth(self, path: str) -> Dict[str, Any]:
        """Load frozen ground truth from Phase 12O Golden Scenario"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def evaluate_optimization(self, chronosdb_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate Phase 7 Intervention Optimization Engine
        
        Metrics:
        - Feasibility Accuracy: 100%
        - Optimal Plan Agreement: ≥90%
        - Constraint Compliance: 100%
        - Utility Fidelity: 100%
        """
        # Phase 7 Optimization Evaluation
        # Compare ChronosDB output with Ground Truth
        
        # Feasibility Accuracy
        predicted_feasibility = chronosdb_output.get('feasibility', 0.0)
        ground_truth_feasibility = self.ground_truth.get('feasibility', 1.0)
        feasibility_accuracy = 1.0 if predicted_feasibility == ground_truth_feasibility else 0.0
        
        # Optimal Plan Agreement
        predicted_plan = chronosdb_output.get('optimal_plan', '')
        ground_truth_plan = self.ground_truth.get('optimal_plan', '')
        optimal_plan_agreement = 1.0 if predicted_plan == ground_truth_plan else (0.9 if predicted_plan in ground_truth_plan else 0.0)
        
        # Constraint Compliance
        predicted_compliance = chronosdb_output.get('constraint_compliance', 0.0)
        ground_truth_compliance = self.ground_truth.get('constraint_compliance', 1.0)
        constraint_compliance = 1.0 if predicted_compliance == ground_truth_compliance else 0.0
        
        # Utility Fidelity
        predicted_utility = chronosdb_output.get('utility_score', 0.0)
        ground_truth_utility = self.ground_truth.get('utility_score', 1.0)
        utility_fidelity = 1.0 if predicted_utility == ground_truth_utility else 0.0
        
        self.metrics = {
          'feasibility_accuracy': feasibility_accuracy,
          'optimal_plan_agreement': optimal_plan_agreement,
          'constraint_compliance': constraint_compliance,
          'utility_fidelity': utility_fidelity,
          'golden_requirement_met': (
            feasibility_accuracy == 1.0 and
            optimal_plan_agreement >= 0.9 and
            constraint_compliance == 1.0 and
            utility_fidelity == 1.0
          )
        }
        
        return self.metrics

# Phase 13F Status: ✅ COMPLETE
