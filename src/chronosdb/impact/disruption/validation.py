from __future__ import annotations

from ..contracts.errors import DisruptionValidationError
from ..state.reconstruction import OperationalState
from .supplier_outage import Disruption


def validate_disruption(disruption: Disruption) -> None:
    if disruption.start_time.tzinfo is None or disruption.end_time.tzinfo is None:
        raise DisruptionValidationError("disruption timestamps must include timezone")
    if disruption.end_time <= disruption.start_time:
        raise DisruptionValidationError("disruption end must be after start")
    if disruption.recovery_lag.total_seconds() < 0:
        raise DisruptionValidationError("recovery lag must not be negative")
    if disruption.recovery_lag.total_seconds() % 3600:
        raise DisruptionValidationError("recovery lag must be expressed in whole hours")
    if disruption.event_type not in {"SUPPLIER_OUTAGE", "PARTIAL_SUPPLY_INTERRUPTION"}:
        raise DisruptionValidationError(f"unsupported disruption type: {disruption.event_type}")
    if disruption.scope_type not in {"ALL_SUPPLY", "COMPONENT", "PURCHASE_ORDER"}:
        raise DisruptionValidationError(f"unsupported disruption scope: {disruption.scope_type}")
    if disruption.scope_type == "COMPONENT" and not disruption.component_ids:
        raise DisruptionValidationError("component scope has no component IDs")
    if disruption.scope_type == "PURCHASE_ORDER" and not disruption.purchase_order_ids:
        raise DisruptionValidationError("purchase-order scope has no purchase-order IDs")


def validate_disruption_against_state(
    state: OperationalState,
    disruption: Disruption,
) -> None:
    """Reject scopes that refer to records absent from the reconstructed state."""
    supplier_ids = {row.get("id", "") for row in state.get("suppliers")}
    if disruption.supplier_id not in supplier_ids:
        raise DisruptionValidationError(f"unknown supplier: {disruption.supplier_id}")
    if disruption.scope_type == "COMPONENT":
        component_ids = {row.get("id", "") for row in state.get("components")}
        unknown = sorted(disruption.component_ids - component_ids)
        if unknown:
            raise DisruptionValidationError(f"unknown component scope: {unknown}")
    if disruption.scope_type == "PURCHASE_ORDER":
        purchase_order_ids = {row.get("id", "") for row in state.get("purchase_orders")}
        unknown = sorted(disruption.purchase_order_ids - purchase_order_ids)
        if unknown:
            raise DisruptionValidationError(f"unknown purchase-order scope: {unknown}")
