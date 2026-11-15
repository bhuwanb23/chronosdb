9. Phase 6E: Scenario Baseline Construction

Every simulation starts from:

Phase 5 State
+
Phase 5 Disruption


NOT from live data.

Simulation baseline:

{
  "baseline_id":"BASE-GOLD-001",
  "state_hash":"...",
  "impact_run_id":"IR-001",
  "revenue_at_risk":"1600000",
  "sla_breaches":2
}

Identity Rule

Every candidate must share:

same state hash

same disruption

same horizon

same rule set


Only overlay differs.

