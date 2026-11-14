"""Phase 7G: Normalization Engine.

Different units (Rupees, Hours, Counts, Percentages) must become comparable.

Min-Max Normalization:
- Benefit Metric: (value - min) / (max - min)
- Cost Metric: (max - value) / (max - min)

Normalized Range: 0.0 → 1.0
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class NormalizedMetrics:
    """Normalized optimization metrics."""
    candidate: str
    revenue_risk_norm: float
    revenue_protected_norm: float
    sla_breaches_norm: float
    breaches_avoided_norm: float
    delay_norm: float
    delay_reduction_norm: float
    recovery_cost_norm: float
    capacity_usage_norm: float
    inventory_consumed_norm: float
    remaining_inventory_norm: float
    supplier_risk_norm: float

class NormalizationEngine:
    """
    Phase 7G: Normalization Engine.
    
    Normalizes different units to comparable 0.0-1.0 range.
    """
    
    def __init__(self):
        pass
    
    def normalize_single(self, metrics: Dict[str, Any], min_values: Dict[str, float], max_values: Dict[str, float]) -> NormalizedMetrics:
        """Normalize single candidate metrics."""
        candidate = metrics.get("candidate", "UNKNOWN")
        
        # Benefit metrics (higher is better -> (value - min) / (max - min))
        revenue_protected_norm = self._normalize_benefit(
            metrics.get("revenue_protected", 0.0),
            min_values.get("revenue_protected", 0.0),
            max_values.get("revenue_protected", 1.0)
        )
        
        breaches_avoided_norm = self._normalize_benefit(
            metrics.get("breaches_avoided", 0),
            min_values.get("breaches_avoided", 0),
            max_values.get("breaches_avoided", 10)
        )
        
        delay_reduction_norm = self._normalize_benefit(
            metrics.get("delay_reduction", 0.0),
            min_values.get("delay_reduction", 0.0),
            max_values.get("delay_reduction", 240)
        )
        
        remaining_inventory_norm = self._normalize_benefit(
            metrics.get("remaining_inventory", 0.0),
            min_values.get("remaining_inventory", 0.0),
            max_values.get("remaining_inventory", 1000)
        )
        
        # Cost metrics (lower is better -> (max - value) / (max - min))
        revenue_risk_norm = self._normalize_cost(
            metrics.get("revenue_risk", 0.0),
            min_values.get("revenue_risk", 0.0),
            max_values.get("revenue_risk", 1000000)
        )
        
        sla_breaches_norm = self._normalize_cost(
            metrics.get("sla_breaches", 0),
            min_values.get("sla_breaches", 0),
            max_values.get("sla_breaches", 10)
        )
        
        delay_norm = self._normalize_cost(
            metrics.get("delay", 0.0),
            min_values.get("delay", 0.0),
            max_values.get("delay", 720)
        )
        
        recovery_cost_norm = self._normalize_cost(
            metrics.get("recovery_cost", 0.0),
            min_values.get("recovery_cost", 0.0),
            max_values.get("recovery_cost", 500000)
        )
        
        capacity_usage_norm = self._normalize_cost(
            metrics.get("capacity_usage", 0.0),
            min_values.get("capacity_usage", 0.0),
            max_values.get("capacity_usage", 100)
        )
        
        inventory_consumed_norm = self._normalize_cost(
            metrics.get("inventory_consumed", 0.0),
            min_values.get("inventory_consumed", 0.0),
            max_values.get("inventory_consumed", 1000)
        )
        
        supplier_risk_norm = self._normalize_cost(
            metrics.get("supplier_risk", 0.0),
            min_values.get("supplier_risk", 0.0),
            max_values.get("supplier_risk", 1.0)
        )
        
        return NormalizedMetrics(
            candidate=candidate,
            revenue_risk_norm=revenue_risk_norm,
            revenue_protected_norm=revenue_protected_norm,
            sla_breaches_norm=sla_breaches_norm,
            breaches_avoided_norm=breaches_avoided_norm,
            delay_norm=delay_norm,
            delay_reduction_norm=delay_reduction_norm,
            recovery_cost_norm=recovery_cost_norm,
            capacity_usage_norm=capacity_usage_norm,
            inventory_consumed_norm=inventory_consumed_norm,
            remaining_inventory_norm=remaining_inventory_norm,
            supplier_risk_norm=supplier_risk_norm
        )
    
    def _normalize_benefit(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize benefit metric: (value - min) / (max - min)"""
        if max_val <= min_val:
            return 0.0
        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))
    
    def _normalize_cost(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize cost metric: (max - value) / (max - min)"""
        if max_val <= min_val:
            return 0.0
        normalized = (max_val - value) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))
    
    def calculate_ranges(self, metrics_list: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Calculate min/max ranges from multiple metrics."""
        ranges = {}
        keys = [
            "revenue_risk", "revenue_protected", "sla_breaches", "breaches_avoided",
            "delay", "delay_reduction", "recovery_cost", "capacity_usage",
            "inventory_consumed", "remaining_inventory", "supplier_risk"
        ]
        
        for key in keys:
            values = [m.get(key, 0.0) for m in metrics_list]
            ranges[key] = {
                "min": min(values) if values else 0.0,
                "max": max(values) if values else 1.0
            }
        
        return ranges
    
    def normalize_multiple(self, metrics_list: List[Dict[str, Any]]) -> List[NormalizedMetrics]:
        """Normalize multiple candidate metrics."""
        ranges = self.calculate_ranges(metrics_list)
        return [self.normalize_single(m, ranges[k]["min"], ranges[k]["max"]) for m in metrics_list for k in ranges.keys()]

# Phase 7G Status: IMPLEMENTED
