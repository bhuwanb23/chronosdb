27. Phase 5W: Independent Review and Release Gate
Goal

Review the engine as both a domain system and a judging artifact.

Domain review

Check:

Outage affects only eligible supply.
Already received material is preserved.
Inventory does not appear or disappear.
Material allocation obeys priority.
Production capacity is respected.
Customer orders receive correct output quantities.
Revenue at risk uses late quantity only.
Temporal review

Check:

State is reconstructed correctly.
Late-arriving data is excluded.
Effective records are selected correctly.
Timestamp boundaries are consistent.
Replay is stable.
Software review

Check:

Domain logic is separated from persistence.
Functions have narrow responsibility.
Rule versions are explicit.
Decimal arithmetic is used.
Stable ordering is enforced.
Errors are typed.
Intermediate results are inspectable.
Audit review

Check:

Every headline metric has provenance.
Every customer breach has a causal path.
Result hash is stable.
Failed runs remain diagnosable.
Operational records remain unchanged.
Judge review

Check:

The engine shows more than a spreadsheet calculation.
Cascading impact is easy to explain.
Db2 operational records are visibly central.
The result is credible without an LLM.
A reviewer can inspect why each order became late.
Required signoffs
Plain Text
Domain logic
Temporal correctness
Financial correctness
Software quality
Benchmark correctness
Auditability
Demo readiness
Deliverables
Plain Text
docs/impact-engine/review-signoff.md
docs/impact-engine/phase-5-completion-report.md
