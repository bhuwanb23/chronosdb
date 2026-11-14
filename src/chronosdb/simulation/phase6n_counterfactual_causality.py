"""Phase 6N: Counterfactual Causality."""

from typing import Dict, Any, List

class CounterfactualCausalityEngine:
    """
    Phase 6N: Counterfactual Causality.
    
    Phase 5: Why was impact created?
    Phase 6: Why was impact reduced?
    
    New causal edge types:
    MITIGATES, AVOIDS_BREACH, PROTECTS_REVENUE, RESTORES_SUPPLY, ACCELERATES
    """
    
    def __init__(self):
        self.edge_types = [
            "MITIGATES",
            "AVOIDS_BREACH",
            "PROTECTS_REVENUE",
            "RESTORES_SUPPLY",
            "ACCELERATES"
        ]
    
    def trace_causality(self, baseline_state: Dict[str, Any], scenario_state: Dict[str, Any], 
                       events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Trace counterfactual causality chain.
        
        Example:
        Transfer ↓ Inventory Available Earlier ↓ MO-0882 Starts Earlier ↓ 
        CO-0704 Delivered On Time ↓ Revenue Protected ₹800k
        """
        
        causal_chain = []
        evidence = []
        
        # Build causal chain based on events
        for event in events:
            event_type = event.get("event_type", "")
            
            if event_type == "SIM_TRANSFER_RECEIPT":
                causal_chain.append({
                    "step": "Transfer",
                    "effect": "Inventory Available Earlier",
                    "edge_type": "RESTORES_SUPPLY"
                })
                evidence.append("RESTORES_SUPPLY")
                
            elif event_type == "SIM_ALT_SUPPLIER_RECEIPT":
                causal_chain.append({
                    "step": "Alternate Supplier",
                    "effect": "Supply Restored",
                    "edge_type": "RESTORES_SUPPLY"
                })
                evidence.append("RESTORES_SUPPLY")
                evidence.append("MITIGATES")
                
            elif event_type == "SIM_EXPEDITION_RECEIPT":
                causal_chain.append({
                    "step": "Expedition",
                    "effect": "Delivery Accelerated",
                    "edge_type": "ACCELERATES"
                })
                evidence.append("ACCELERATES")
                evidence.append("PROTECTS_REVENUE")
                
            elif event_type == "SIM_PRODUCTION_RESCHEDULE":
                causal_chain.append({
                    "step": "Reschedule",
                    "effect": "Priority Changed",
                    "edge_type": "MITIGATES"
                })
                evidence.append("MITIGATES")
                evidence.append("AVOIDS_BREACH")
        
        # Compute final impact reduction
        revenue_reduction = baseline_state.get("revenue_risk", 0) - scenario_state.get("revenue_risk", 0)
        breach_reduction = baseline_state.get("breaches", 0) - scenario_state.get("breaches", 0)
        delay_reduction = baseline_state.get("delay_hours", 0) - scenario_state.get("delay_hours", 0)
        
        return {
            "causal_chain": causal_chain,
            "evidence_edges": list(set(evidence)),
            "impact_reduction": {
                "revenue_protected": revenue_reduction,
                "breaches_avoided": breach_reduction,
                "delay_reduction_hours": delay_reduction
            },
            "provenance": {
                "baseline_state_hash": baseline_state.get("state_hash", ""),
                "scenario_state_hash": scenario_state.get("state_hash", ""),
                "events_processed": len(events)
            }
        }
