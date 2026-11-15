"""Phase 6D: Intervention Registry."""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any

class InterventionType(Enum):
    INT_TRANSFER = "INT-TRANSFER"
    INT_EXPEDITE = "INT-EXPEDITE"
    INT_SUPPLIER = "INT-SUPPLIER"
    INT_RESCHEDULE = "INT-RESCHEDULE"
    INT_HYBRID = "INT-HYBRID"

@dataclass(frozen=True)
class InterventionDefinition:
    intervention_id: InterventionType
    version: str
    inputs: Dict[str, str]  # e.g., component_id, quantity, etc.
    validation_rules: Dict[str, Any]

# Registry of interventions (Phase 6D)
INTERVENTION_REGISTRY = {
    InterventionType.INT_TRANSFER: InterventionDefinition(
        intervention_id=InterventionType.INT_TRANSFER,
        version="1.0.0",
        inputs={
            "component_id": "str",
            "quantity": "str",
            "source_warehouse": "str",
            "destination_warehouse": "str"
        },
        validation_rules={
            "transferable_inventory_gt_quantity": True,
            "remaining_after_transfer_ge_safety_stock": True
        }
    ),
    InterventionType.INT_EXPEDITE: InterventionDefinition(
        intervention_id=InterventionType.INT_EXPEDITE,
        version="1.0.0",
        inputs={
            "purchase_order_id": "str",
            "lead_time_reduction_days": "int"
        },
        validation_rules={
            "cannot_precede_shipment_release": True,
            "cannot_exceed_supplier_capability": True,
            "must_incur_cost": True
        }
    ),
    InterventionType.INT_SUPPLIER: InterventionDefinition(
        intervention_id=InterventionType.INT_SUPPLIER,
        version="1.0.0",
        inputs={
            "supplier_id": "str",
            "component_id": "str",
            "available_quantity": "str"
        },
        validation_rules={}
    ),
    InterventionType.INT_RESCHEDULE: InterventionDefinition(
        intervention_id=InterventionType.INT_RESCHEDULE,
        version="1.0.0",
        inputs={
            "production_order_id": "str",
            "priority": "int"
        },
        validation_rules={}
    ),
    InterventionType.INT_HYBRID: InterventionDefinition(
        intervention_id=InterventionType.INT_HYBRID,
        version="1.0.0",
        inputs={},
        validation_rules={}
    )
}

def get_intervention(intervention_id: InterventionType) -> InterventionDefinition:
    return INTERVENTION_REGISTRY[intervention_id]
