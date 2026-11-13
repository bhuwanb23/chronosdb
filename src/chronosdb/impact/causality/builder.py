from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..contracts.results import StateIdentity
from ..disruption.supplier_outage import Disruption, PurchaseOrderImpact
from ..fulfilment.sla import SLAResult
from ..production.scheduler import ProductionImpact


@dataclass(frozen=True)
class CausalTrace:
    trace_id: str
    target_id: str
    target_metric: str
    attribution: str
    nodes: tuple[dict[str, Any], ...]
    edges: tuple[dict[str, Any], ...]
    rule_version: str
    state_hash: str
    source_record_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "target": {"entity_id": self.target_id, "metric": self.target_metric},
            "attribution": self.attribution,
            "nodes": list(self.nodes),
            "edges": list(self.edges),
            "rule_version": self.rule_version,
            "state_hash": self.state_hash,
            "source_record_ids": list(self.source_record_ids),
        }


def build_causal_traces(
    disruption: Disruption,
    purchase_order_impacts: tuple[PurchaseOrderImpact, ...],
    production_impacts: tuple[ProductionImpact, ...],
    sla_results: tuple[SLAResult, ...],
    identity: StateIdentity,
    rule_version: str,
) -> tuple[CausalTrace, ...]:
    purchase_orders = {
        item.component_id: item for item in purchase_order_impacts
    }
    production_by_id = {
        item.production_order_id: item for item in production_impacts
    }
    traces: list[CausalTrace] = []
    for result in sla_results:
        if result.status != "BREACHED":
            continue
        production = production_by_id.get(result.production_order_id)
        component_id = (
            production.blocking_components[0]
            if production and production.blocking_components
            else next(iter(purchase_orders), "")
        )
        purchase = purchase_orders.get(component_id)
        purchase_id = purchase.purchase_order_id if purchase else disruption.event_id
        nodes = (
            {"node_id": disruption.event_id, "node_type": "DISRUPTION"},
            {"node_id": purchase_id, "node_type": "PURCHASE_ORDER"},
            {"node_id": component_id, "node_type": "SHORTAGE"},
            {"node_id": result.production_order_id, "node_type": "PRODUCTION_ORDER"},
            {"node_id": result.customer_order_line_id, "node_type": "CUSTOMER_ORDER_LINE"},
            {
                "node_id": f"REVENUE-{result.customer_order_line_id}",
                "node_type": "REVENUE_AT_RISK",
            },
        )
        edges = (
            {
                "edge_id": f"{result.customer_order_line_id}-01",
                "from": disruption.event_id,
                "to": purchase_id,
                "edge_type": "DELAYS",
                "rule_id": "SUP-004",
            },
            {
                "edge_id": f"{result.customer_order_line_id}-02",
                "from": purchase_id,
                "to": component_id,
                "edge_type": "CAUSES_SHORTAGE",
                "rule_id": "INV-003",
            },
            {
                "edge_id": f"{result.customer_order_line_id}-03",
                "from": component_id,
                "to": result.production_order_id,
                "edge_type": "BLOCKS",
                "rule_id": "ALLOC-001",
            },
            {
                "edge_id": f"{result.customer_order_line_id}-04",
                "from": result.production_order_id,
                "to": result.customer_order_line_id,
                "edge_type": "DELAYS",
                "rule_id": "FUL-001",
            },
            {
                "edge_id": f"{result.customer_order_line_id}-05",
                "from": result.customer_order_line_id,
                "to": f"REVENUE-{result.customer_order_line_id}",
                "edge_type": "EXPOSES_REVENUE",
                "rule_id": "FIN-004",
            },
        )
        source_ids = tuple(
            sorted(
                {
                    disruption.event_id,
                    purchase_id,
                    component_id,
                    result.production_order_id,
                    result.customer_order_line_id,
                }
            )
        )
        traces.append(
            CausalTrace(
                trace_id=f"CT-{result.customer_order_line_id}",
                target_id=result.customer_order_line_id,
                target_metric="projected_delay_hours",
                attribution=result.attribution,
                nodes=nodes,
                edges=edges,
                rule_version=rule_version,
                state_hash=identity.state_hash,
                source_record_ids=source_ids,
            )
        )
    return tuple(sorted(traces, key=lambda trace: trace.trace_id))
