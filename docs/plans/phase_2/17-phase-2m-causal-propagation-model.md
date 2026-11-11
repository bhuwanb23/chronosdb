17. Phase 2M: Causal Propagation Model
Goal

Define the complete deterministic path from supplier disruption to business impact.

17.1 Causal graph
Plain Text
Supplier Outage
↓
Affected Outstanding Purchase Orders
↓
Delayed Component Receipts
↓
Lower Projected Component Balance
↓
Component Shortage
↓
Production Material Unavailability
↓
Delayed Production Start
↓
Delayed Production Completion
↓
Delayed Product Availability
↓
Delayed Customer Delivery
↓
SLA Breach
↓
Revenue at Risk
17.2 Causal edge contract

Every edge must define:

Source state
Transformation rule
Required data
Output state
Failure condition
Evidence trace

Example:

Plain Text
Edge:
Delayed receipt → component shortage
 
Required data:
Opening balance
Reserved quantity
Expected receipts
Production consumption
Receipt timestamps
 
Rule:
Ordered inventory balance calculation
 
Output:
Shortage date and quantity
 
Failure:
Missing opening inventory snapshot
17.3 Necessary versus contributing causes

ChronosDB should distinguish:

Necessary operational constraint

A missing mandatory component that directly blocks production.

Contributing factor

A low safety-stock level that makes disruption impact worse but does not independently cause the outage.

Contextual evidence

A historical incident that helps explain risk but does not establish current causality.

17.4 Causal trace

Every affected customer-order line should support a trace like:

Plain Text
Supplier S-104 outage
→ PO-2208 delayed
→ C-042 receipt delayed by 14 days
→ C-042 shortage of 320 units on 14 Nov
→ Production order PROD-876 starts 6 days late
→ Customer order CO-701 delivered 5 days late
→ ₹420,000 revenue at risk
17.5 No unsupported causal jumps

The system must not jump directly from:

Plain Text
Supplier outage → revenue loss

Instead it must preserve intermediate dependencies.

Deliverables
Plain Text
docs/domain/causal-model.md
docs/domain/causal-edge-catalogue.md
docs/domain/causal-trace-format.md
Causal completeness metric
CC=business impact outputs with complete causal pathsall business impact outputsCC = \frac{\text{business impact outputs with complete causal paths}} {\text{all business impact outputs}}CC=all business impact outputsbusiness impact outputs with complete causal paths​

Target for the golden scenario:

Plain Text
100%
