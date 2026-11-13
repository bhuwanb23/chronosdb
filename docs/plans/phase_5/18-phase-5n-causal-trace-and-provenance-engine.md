18. Phase 5N: Causal Trace and Provenance Engine
Goal

Explain exactly how each impact was produced.

Causal node types
Plain Text
DISRUPTION
PURCHASE_ORDER
RECEIPT_CHANGE
INVENTORY_STATE
SHORTAGE
MATERIAL_ALLOCATION
PRODUCTION_BATCH
PRODUCTION_ORDER
PRODUCT_AVAILABILITY
CUSTOMER_ORDER_LINE
SLA_BREACH
REVENUE_AT_RISK
Causal edge types
Plain Text
AFFECTS
DELAYS
REDUCES
CAUSES_SHORTAGE
BLOCKS
RESCHEDULES
PRODUCES
FULFILLS
BREACHES
EXPOSES_REVENUE
Golden trace example
Plain Text
EVT-GOLD-001
SUP-0104 outage
↓ DELAYS
PO-2208
800 MCU receipt delayed to 27 Nov
↓ REDUCES
WH-PUNE projected MCU availability
↓ CAUSES_SHORTAGE
CMP-MCU-42 shortage
↓ BLOCKS
MO-0882 and MO-0889
↓ DELAYS
Product availability
↓ DELAYS
CO-0704 and CO-0711
↓ BREACHES
Customer SLA commitments
↓ EXPOSES_REVENUE
₹1,600,000 revenue at risk
Provenance object

Every impact metric should include:

Plain Text
metric ID
metric name
value
unit
currency if applicable
rule ID
rule version
input record IDs
calculation step IDs
scenario ID
impact run ID
state hash
timestamp
data-quality status
Causal trace validation

Every breached customer-order line must trace to:

At least one production constraint
At least one material or capacity cause
At least one upstream operational record
The disruption event when disruption caused the impact
Counterfactual causal comparison

Phase 5 should preserve a no-disruption reference calculation where possible.

This permits distinction between:

Plain Text
Already late before disruption
Newly late because of disruption
Made later by disruption
Unaffected

This is important because ChronosDB must not attribute pre-existing lateness to the supplier outage.

Attribution classes
Plain Text
DISRUPTION_CAUSED
DISRUPTION_WORSENED
PRE_EXISTING
UNRELATED
INSUFFICIENT_EVIDENCE
Deliverables
Plain Text
src/backend/chronosdb/impact/causality/
src/backend/chronosdb/impact/provenance/
docs/impact-engine/causality-and-provenance.md
Target
Plain Text
Causal coverage for golden and benchmark key outputs: 100%
