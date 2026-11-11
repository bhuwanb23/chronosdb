# Phase 2M: Causal Trace Format

Every affected customer-order line should expose a trace with these fields:

```yaml
trace_id: CT-...
scenario_id: SC-...
simulation_run_id: SIM-...
state_version: ...
rule_version: ...
target:
  customer_order_line_id: ...
  metric: projected_delay_hours
steps:
  - edge_id: CE-001
    source_type: disruption_event
    source_id: ...
    output: affected_purchase_order
    rule_id: DIS-001
  - edge_id: CE-002
    source_type: purchase_order
    source_id: ...
    output: delayed_receipt
    rule_id: DIS-002
  - edge_id: CE-004
    source_type: inventory_and_requirement
    source_id: ...
    output: shortage
    rule_id: INV-003
  - edge_id: CE-006
    source_type: production_order
    source_id: ...
    output: projected_completion
    rule_id: PROD-003
  - edge_id: CE-008
    source_type: customer_order_line
    source_id: ...
    output: projected_delivery
    rule_id: SLA-001
result:
  value: ...
  unit: ...
  evidence_status: complete
```

## Trace rules

- Steps are ordered from cause to result.
- Each step names an edge, rule, source record, and output.
- The result includes unit and reference case when it is a delta.
- A missing step makes the trace incomplete.
- A historical document may add context but cannot replace an operational or
  derived step.
