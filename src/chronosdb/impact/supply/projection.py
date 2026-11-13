from __future__ import annotations

from ..contracts.requests import SimulationHorizon
from ..disruption.supplier_outage import PurchaseOrderImpact
from .receipts import ProjectedReceipt


def project_receipts(
    impacts: tuple[PurchaseOrderImpact, ...], horizon: SimulationHorizon
) -> tuple[ProjectedReceipt, ...]:
    projections = [
        ProjectedReceipt(
            event_id=f"RCPT-PROJ-{impact.purchase_order_id}",
            purchase_order_id=impact.purchase_order_id,
            warehouse_id=impact.warehouse_id,
            component_id=impact.component_id,
            quantity=impact.outstanding_quantity,
            event_time=impact.disrupted_arrival,
            event_type="PROJECTED_PURCHASE_RECEIPT",
            source="DISRUPTION_ADJUSTED",
            original_event_time=impact.original_arrival,
            within_horizon=(
                horizon.as_of_time
                <= impact.disrupted_arrival
                <= horizon.simulation_end_time
            ),
            rule_id="SUP-006",
        )
        for impact in impacts
    ]
    return tuple(sorted(projections, key=lambda item: (item.event_time, item.event_id)))
