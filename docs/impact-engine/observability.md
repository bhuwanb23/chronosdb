# Impact Engine Observability

Phase 5 exposes safe aggregate diagnostics through
`chronosdb.impact.observability.ImpactDiagnostics`.

```python
from chronosdb.impact.observability import ImpactDiagnostics

diagnostics = ImpactDiagnostics(
    correlation_id="REQ-123",
    scenario_id="SCN-GOLD-001",
)
result = calculate_impact(..., diagnostics=diagnostics)
record = diagnostics.emit()
```

Each diagnostic record contains:

- `correlation_id`, `impact_run_id`, and `scenario_id`
- terminal `status`
- total and per-stage duration in milliseconds
- aggregate counters for affected purchase orders, receipts, timelines,
  shortages, production batches, customer lines, and causal nodes
- warning and error counts

The diagnostics object intentionally does not contain credentials, connection
strings, unrestricted source records, customer document contents, or raw
operational payloads. Detailed calculation evidence remains in the persisted
impact result and provenance structures.

Debug trace mode is opt-in: callers may enable application logging for the
`chronosdb.impact` logger and emit the diagnostics record after a run. Normal
demo and production execution should emit only the structured aggregate record.
