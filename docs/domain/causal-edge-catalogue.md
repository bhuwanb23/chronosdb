# Phase 2M: Causal Edge Catalogue

| ID | Edge | Required data | Output | Failure |
|---|---|---|---|---|
| CE-001 | Outage → affected PO | Supplier, scope, PO, outage interval | Affected outstanding PO set | Missing supplier relationship |
| CE-002 | Affected PO → delayed receipt | Outstanding quantity, original arrival, outage end, recovery lag | New receipt timing | Invalid interval or lag |
| CE-003 | Delayed receipt → balance | Opening balance, reservations, receipts, consumption, timestamps | Projected component balance | Missing inventory snapshot |
| CE-004 | Balance → shortage | Requirements and allocatable quantity by time | Shortage date/quantity | Missing requirement or unit |
| CE-005 | Shortage → material unavailability | BOM, mandatory flag, allocation | Component-ready time | Missing active BOM |
| CE-006 | Material → production delay | Material-ready time, capacity, priority, plan | Projected production completion | Missing capacity or schedule |
| CE-007 | Production → product availability | Completion, fulfilment allocation | Product availability | Missing production mapping |
| CE-008 | Product → customer delivery | Product availability, delivery lead time, order line | Projected delivery | Missing promised date |
| CE-009 | Delivery → SLA | Projected delivery, promised date, SLA rule | SLA status | Missing SLA rule |
| CE-010 | SLA → revenue at risk | Late quantity and unit revenue | Revenue at risk | Missing quantity or revenue |

Each edge must preserve source references, rule ID, units, scenario ID,
simulation-run ID, and failure status in later implementations.
