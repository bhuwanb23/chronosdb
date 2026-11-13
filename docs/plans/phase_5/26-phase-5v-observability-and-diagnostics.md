26. Phase 5V: Observability and Diagnostics
Goal

Make failures diagnosable without leaking secrets or overwhelming users.

Structured logs

Each log entry should include:

Plain Text
correlation_id
impact_run_id
scenario_id
phase
entity_type
entity_id
rule_id
status
duration_ms
error_code
Pipeline-stage timings

Capture:

Plain Text
state_reconstruction_ms
disruption_resolution_ms
inventory_projection_ms
material_allocation_ms
production_scheduling_ms
customer_impact_ms
provenance_build_ms
persistence_ms
total_ms
Diagnostic counters
Records loaded
Purchase orders affected
Receipt events changed
Inventory timelines processed
Shortages found
Production batches scheduled
Customer lines calculated
Causal nodes generated
Warnings
Errors
Safe logging

Never log:

Passwords
Db2 connection strings with credentials
LLM keys
Entire unrestricted document content
Unnecessary raw personal data

The dataset is synthetic, but secure behavior should still be implemented.

Debug trace mode

Provide an optional development mode that emits per-rule calculations.

Production or demo default should preserve calculation traces in structured persistence without flooding standard logs.

Deliverables
Plain Text
src/backend/chronosdb/observability/
docs/impact-engine/observability.md
