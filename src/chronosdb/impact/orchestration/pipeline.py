from __future__ import annotations

from ..contracts.enums import DataQualityStatus, ImpactStatus
from ..contracts.requests import SimulationHorizon
from ..contracts.results import ImpactResult, canonical_hash
from ..disruption.supplier_outage import Disruption, resolve_purchase_order_impacts
from ..disruption.validation import validate_disruption
from ..rules.versions import RuleSet
from ..state.reconstruction import OperationalState
from ..supply.projection import project_receipts


def calculate_impact(
    state: OperationalState,
    disruption: Disruption,
    horizon: SimulationHorizon,
    rules: RuleSet,
) -> ImpactResult:
    """Calculate the deterministic 5A–5G supply-impact slice."""
    validate_disruption(disruption)
    impacts = resolve_purchase_order_impacts(state, disruption)
    receipts = project_receipts(impacts, horizon)
    affected_components = sorted({impact.component_id for impact in impacts})
    provenance = {
        "state_version": state.identity.state_version,
        "input_state_hash": state.identity.state_hash,
        "rule_set_version": rules.version,
        "rule_ids": ["STATE-001", "SUP-001", "SUP-004", "SUP-005", "SUP-006"],
        "source_record_ids": sorted(
            {
                source_id
                for impact in impacts
                for source_id in impact.source_record_ids
            }
        ),
    }
    run_fingerprint = canonical_hash(
        {"state": state.identity.state_hash, "event": disruption.event_id}
    )
    result = ImpactResult(
        impact_run_id=f"IR-{run_fingerprint[:16]}",
        scenario_id=state.identity.state_version,
        status=ImpactStatus.PARTIALLY_COMPLETED,
        data_quality_status=(
            DataQualityStatus.PARTIAL if state.warnings else DataQualityStatus.COMPLETE
        ),
        rule_set_version=rules.version,
        input_state_hash=state.identity.state_hash,
        affected_purchase_orders=[impact.to_dict() for impact in impacts],
        affected_components=affected_components,
        inventory_timelines=[receipt.to_dict() for receipt in receipts],
        warnings=[
            "Downstream inventory, production, fulfilment, and financial stages are 5H–5M."
        ],
        provenance=provenance,
    )
    result.result_hash = canonical_hash(result.to_dict())
    return result
