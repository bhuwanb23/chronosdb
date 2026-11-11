22. Phase 2R: Uncertainty and Data-Quality Model
Goal

Prevent incomplete or assumed data from appearing as precise truth.

22.1 Information classes
OBSERVED

Directly stored operational fact.

DERIVED

Calculated deterministically from observed facts.

ASSUMED

Configured simplification.

Examples:

One-day delivery lead time
Two-day supplier recovery lag
PROJECTED

Future outcome produced by deterministic simulation.

GENERATED

Natural-language explanation produced by AI.

22.2 Data completeness state

For each scenario:

Plain Text
COMPLETE
PARTIAL_NONCRITICAL
PARTIAL_CRITICAL
INVALID
Critical missing data

Examples:

No active BOM
No inventory state
Missing promised delivery
Missing production-order mapping
Unknown supplier relationship

Critical missing data must block the affected calculation.

22.3 No implicit zero rule

Missing values are never automatically treated as:

Plain Text
0 inventory
0 cost
0 lead time
0 revenue
0 demand

Use:

Plain Text
UNKNOWN
NOT_APPLICABLE
ZERO

as distinct concepts.

22.4 Confidence classification

Do not invent a percentage confidence score.

Recommended qualitative classification:

Plain Text
HIGH_EVIDENCE
MEDIUM_EVIDENCE
LOW_EVIDENCE
INSUFFICIENT_EVIDENCE

Example criteria:

High evidence
All critical structured records exist.
No major assumption drives the recommendation.
Causal trace is complete.
Medium evidence
Critical records exist.
One or more configured assumptions affect timing or cost.
Low evidence
Noncritical data is missing.
The recommendation is sensitive to an assumption.
Insufficient evidence
A critical calculation cannot be completed.
Deliverable
Plain Text
docs/domain/uncertainty-and-data-quality-model.md
Exit gate
Missing and zero are distinct.
Facts and assumptions are labelled.
Confidence does not use arbitrary percentages.
Critical missing data blocks affected calculations.
Partial results remain visible when safe.
