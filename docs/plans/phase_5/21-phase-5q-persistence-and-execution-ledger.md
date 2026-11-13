21. Phase 5Q: Persistence and Execution Ledger
Goal

Persist inputs, intermediate calculations, outputs, and errors without mutating operational truth.

Conceptual result records
Plain Text
IMPACT_RUN
IMPACT_RUN_INPUT
AFFECTED_SUPPLY
PROJECTED_INVENTORY_EVENT
COMPONENT_SHORTAGE
PRODUCTION_IMPACT
CUSTOMER_IMPACT
IMPACT_METRIC
CAUSAL_NODE
CAUSAL_EDGE
CALCULATION_TRACE
IMPACT_WARNING
IMPACT_ERROR

The physical Db2 schema may already exist or may be implemented alongside this phase, but the engine contract remains independent.

Run record
Plain Text
impact_run_id
scenario_id
request_fingerprint
input_state_hash
rule_set_version
status
started_at
completed_at
result_hash
data_quality_status
error_summary
Persistence rules
Operational source records are read-only.
Projected events are stored separately.
Intermediate calculations are linked to an impact run.
Failed runs preserve diagnostics.
Repeated execution does not overwrite historical runs.
Completed results are immutable under the application role.
Verification reruns create a linked verification record or reuse prior output.
Transaction boundary

Recommended:

Create impact-run record.
Freeze input references.
Perform domain calculation outside long database transaction.
Persist result atomically.
Mark run complete.
If persistence fails, retain enough diagnostics to retry safely.
Deliverables
Plain Text
src/backend/chronosdb/impact/persistence/
docs/impact-engine/execution-ledger.md
