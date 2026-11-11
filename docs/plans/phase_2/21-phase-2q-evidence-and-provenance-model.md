21. Phase 2Q: Evidence and Provenance Model
Goal

Ensure every important result can be explained and audited later.

21.1 Evidence categories
Operational evidence
Supplier record
Purchase order
Inventory snapshot
BOM version
Production order
Customer order
Rule evidence
Formula ID
Allocation rule
Scheduling rule
Feasibility rule
Objective version
Contextual evidence
Disruption report
Recovery procedure
Historical incident
Execution evidence
Scenario ID
Simulation run ID
Input-state version
Rule version
Timestamp
System version
21.2 Provenance chain

For a displayed metric:

Plain Text
Displayed claim
→ Derived output field
→ Calculation step
→ Rule ID
→ Input records
→ State version
→ Scenario and simulation run
21.3 Example
Plain Text
Claim:
Customer order CO-701 will be five days late.
 
Derived value:
projected_delay_hours = 120
 
Rule:
SLA-003
 
Inputs:
CO-701 promised delivery
PROD-876 projected completion
delivery lead time
 
Causal source:
C-042 shortage caused by delayed PO-2208
 
Run:
SIM-GOLD-DO-NOTHING
21.4 Provenance completeness

A result is not presentation-ready unless:

Its source records are identified.
Its formula version is identified.
Its scenario run is identified.
Its unit is specified.
Its reference case is specified if it is a delta.
Deliverable
Plain Text
docs/domain/provenance-model.md
Benchmark
ProvenanceCoverage=key outputs with complete provenanceall key outputsProvenanceCoverage = \frac{\text{key outputs with complete provenance}} {\text{all key outputs}}ProvenanceCoverage=all key outputskey outputs with complete provenance​

Golden scenario target:

Plain Text
100%
