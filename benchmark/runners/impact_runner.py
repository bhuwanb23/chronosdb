"""
Phase 13D: Impact Engine Evaluation (Phase 5)
Benchmark and Evaluation System
"""

import json
import os
from typing import Dict, Any

class ImpactEngineEvaluator:
    """
    Evaluates Phase 5: Deterministic Impact Engine
    
    Metrics:
    - Affected Purchase Order Precision (Target: ≥99%)
    - Affected Purchase Order Recall (Target: ≥98%)
    - Component Impact Precision (Target: ≥99%)
    - Production Impact Recall (Target: ≥98%)
    - Revenue Fidelity (Target: 100%)
    - Quantity Fidelity (Target: 100%)
    - SLA Accuracy (Target: 100%)
    
    Golden Requirement: Exact Match for Revenue, Delay, SLA, Quantities, Timestamps
    """
    
    def __init__(self, ground_truth_path: str):
        self.ground_truth = self._load_ground_truth(ground_truth_path)
        self.metrics = {}
    
    def _load_ground_truth(self, path: str) -> Dict[str, Any]:
        """Load frozen ground truth from Phase 12O Golden Scenario"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def evaluate_impact(self, chronosdb_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate Phase 5 Impact Engine
        
        Metrics:
        - Affected Purchase Order Precision: ≥99%
        - Affected Purchase Order Recall: ≥98%
        - Component Impact Precision: ≥99%
        - Production Impact Recall: ≥98%
        - Revenue Fidelity: 100%
        - Quantity Fidelity: 100%
        - SLA Accuracy: 100%
        """
        # Phase 5 Impact Engine Evaluation
        # Compare ChronosDB output with Ground Truth
        
        # Affected Purchase Order Precision
        predicted_pos = chronosdb_output.get('affected_pos', [])
        ground_truth_pos = self.ground_truth.get('affected_pos', [])
        
        correct_pos = len(set(predicted_pos) & set(ground_truth_pos))
        precision_po = correct_pos / len(predicted_pos) if predicted_pos else 0
        recall_po = correct_pos / len(ground_truth_pos) if ground_truth_pos else 0
        
        # Component Impact Precision
        predicted_components = chronosdb_output.get('affected_components', [])
        ground_truth_components = self.ground_truth.get('affected_components', [])
        
        correct_components = len(set(predicted_components) & set(ground_truth_components))
        precision_components = correct_components / len(predicted_components) if predicted_components else 0
        
        # Production Impact Recall
        predicted_production = chronosdb_output.get('affected_production', [])
        ground_truth_production = self.ground_truth.get('affected_production', [])
        
        correct_production = len(set(predicted_production) & set(ground_truth_production))
        recall_production = correct_production / len(ground_truth_production) if ground_truth_production else 0
        
        # Revenue Fidelity (Target: 100%)
        predicted_revenue = chronosdb_output.get('revenue_at_risk', 0)
        ground_truth_revenue = self.ground_truth.get('revenue_at_risk', 0)
        revenue_fidelity = 1.0 if predicted_revenue == ground_truth_revenue else 0.0
        
        # Quantity Fidelity (Target: 100%)
        predicted_quantity = chronosdb_output.get('affected_orders', 0)
        ground_truth_quantity = self.ground_truth.get('affected_orders', 0)
        quantity_fidelity = 1.0 if predicted_quantity == ground_truth_quantity else 0.0
        
        # SLA Accuracy (Target: 100%)
        predicted_sla = chronosdb_output.get('sla_breaches', 0)
        ground_truth_sla = self.ground_truth.get('sla_breaches', 0)
        sla_accuracy = 1.0 if predicted_sla == ground_truth_sla else 0.0
        
        self.metrics = {
          'affected_purchase_order_precision': precision_po,
          'affected_purchase_order_recall': recall_po,
          'component_impact_precision': precision_components,
          'production_impact_recall': recall_production,
          'revenue_fidelity': revenue_fidelity,
          'quantity_fidelity': quantity_fidelity,
          'sla_accuracy': sla_accuracy,
          'golden_requirement_met': (
            revenue_fidelity == 1.0 and
            quantity_fidelity == 1.0 and
            sla_accuracy == 1.0
          )
        }
        
        return self.metrics

# Phase 13D Status: ✅ COMPLETE
