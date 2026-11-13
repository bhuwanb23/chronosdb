19. Phase 5O: Partial-Result and Data-Quality Handling
Goal

Return safe, truthful output when some calculations cannot be completed.

Data-quality statuses
Plain Text
COMPLETE
PARTIAL_NONCRITICAL
PARTIAL_CRITICAL
INVALID
Impact-run statuses
Plain Text
COMPLETED
PARTIALLY_COMPLETED
REJECTED
FAILED
Critical missing data examples
No inventory state
No active BOM
Missing component unit
Missing customer promised date
Missing production-customer relationship
Inconsistent production quantity
Unknown supplier
Invalid disruption interval
Noncritical missing data examples
Missing descriptive supplier name
Missing historical incident
Missing optional notes
Missing nonessential classification
Failure-isolation behavior

If one customer line lacks a promised date:

Mark that line INSUFFICIENT_DATA.
Continue calculating other lines.
Exclude the unknown line from numerical SLA totals or report it separately.
Do not treat the line as on time.
Do not treat revenue at risk as zero.
Mark run PARTIALLY_COMPLETED.
Error object
JSON
{
"code": "MISSING_PROMISED_DELIVERY",
"severity": "CRITICAL_FOR_ENTITY",
"entity_type": "CUSTOMER_ORDER_LINE",
"entity_id": "COL-...",
"affected_outputs": [
"sla_status",
"delay_hours",
"revenue_at_risk"
],
"message": "Promised delivery is required for SLA calculation."
}
Deliverables
Plain Text
src/backend/chronosdb/impact/validation/
docs/impact-engine/data-quality-and-partial-results.md
