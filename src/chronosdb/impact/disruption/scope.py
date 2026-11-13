from __future__ import annotations

from .supplier_outage import Disruption


def matches_scope(
    disruption: Disruption,
    *,
    supplier_id: str,
    component_id: str,
    purchase_order_id: str,
) -> bool:
    if supplier_id != disruption.supplier_id:
        return False
    if disruption.scope_type == "ALL_SUPPLY":
        return True
    if disruption.scope_type == "COMPONENT":
        return component_id in disruption.component_ids
    return purchase_order_id in disruption.purchase_order_ids
