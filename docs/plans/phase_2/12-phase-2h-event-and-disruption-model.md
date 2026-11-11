12. Phase 2H: Event and Disruption Model
Goal

Define how a supplier outage changes expected supply.

12.1 MVP event type
Plain Text
SUPPLIER_OUTAGE
Required parameters
Plain Text
supplier_id
start_time
end_time or duration
scope
severity
reported_time
Scope options
Plain Text
ALL_SUPPLY
SELECTED_COMPONENTS
SELECTED_PURCHASE_ORDERS

MVP golden scenario:

Plain Text
ALL_SUPPLY
12.2 Outage effect

For an affected purchase order with expected arrival during the outage:

Simple MVP rule

The affected outstanding quantity is delayed until:

Arrivalnew=max⁡(Arrivaloriginal,OutageEnd+RecoveryLag)Arrival_{new} = \max(Arrival_{original}, OutageEnd + RecoveryLag)Arrivalnew​=max(Arrivaloriginal​,OutageEnd+RecoveryLag)

Where:

Plain Text
RecoveryLag = supplier restart and logistics delay

Recommended initial recovery lag:

Plain Text
2 calendar days

This must be configurable.

12.3 Effect boundaries

An outage does not affect:

Quantity already received
Unaffected suppliers
Components outside disruption scope
Purchase orders arriving before outage start
Cancelled purchase orders
Purchase orders after outage if supplier capacity permits
12.4 Post-outage capacity

MVP simplification:

Supply resumes at normal capacity after recovery lag.
No backlog-capacity competition is initially modelled.

This assumption must be recorded because real suppliers may require time to clear accumulated backlog.

12.5 Event precedence

If multiple events affect the same supply:

Phase 2 records the conceptual precedence rule.
Multi-event simulation remains deferred.
MVP rejects overlapping unmodelled disruptions rather than guessing.
Deliverable
Plain Text
docs/domain/disruption-model.md
Exit gate
Outage start and end semantics are precise.
Affected supply is deterministically identifiable.
Already received supply is protected.
Recovery lag is explicit.
Unsupported overlapping disruptions are rejected.
