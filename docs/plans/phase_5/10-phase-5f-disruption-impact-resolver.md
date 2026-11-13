10. Phase 5F: Disruption-Impact Resolver
Goal

Determine exactly which inbound commitments are affected by the supplier outage.

Processing sequence
Validate disruption.
Resolve supplier.
Resolve scope.
Select outstanding purchase orders.
Exclude already received quantities.
Apply outage interval.
Apply recovery lag.
Generate changed receipt events.
Preserve original and disrupted values.
Produce impact evidence.
Affected purchase-order condition

A purchase order is affected when:

Supplier matches.
It has outstanding quantity.
Status is eligible.
Scope includes its component or ID.
Expected supply intersects the outage rule.
It was not fully received before the outage.
Outstanding quantity
Qoutstanding=max⁡(0,Qordered−Qreceived)Q_{outstanding} = \max(0, Q_{ordered} - Q_{received})Qoutstanding​=max(0,Qordered​−Qreceived​)
Disrupted arrival

For the locked Phase 2 rule:

Arrivaldisrupted=max⁡(Arrivaloriginal,OutageEnd+RecoveryLag)Arrival_{disrupted} = \max( Arrival_{original}, OutageEnd + RecoveryLag )Arrivaldisrupted​=max(Arrivaloriginal​,OutageEnd+RecoveryLag)
Purchase-order impact object
JSON
{
"purchase_order_id": "PO-2208",
"component_id": "CMP-MCU-42",
"outstanding_quantity": "800",
"original_arrival": "2026-11-13T00:00:00Z",
"disrupted_arrival": "2026-11-27T00:00:00Z",
"delay_hours": 336,
"rule_id": "SUP-004",
"source_record_ids": ["PO-2208", "EVT-GOLD-001"]
}
Edge cases
Partially received purchase order
Arrival exactly at outage start
Arrival exactly at outage end
Cancelled purchase order
Component-scoped outage
Purchase-order-scoped outage
Supplier agreement expires during horizon
Recovery extends beyond simulation horizon
Deliverables
Plain Text
src/backend/chronosdb/impact/disruption/
src/backend/chronosdb/impact/supply/
docs/impact-engine/disruption-resolution.md
