# User Needs

| ID | Need | Priority | Planned requirement mapping |
|---|---|---:|---|
| UN-001 | Understand disruption impact quickly | P0 | FR-SCN, FR-IMP |
| UN-002 | Identify the dependency bottleneck | P0 | FR-IMP |
| UN-003 | See affected components, production orders, and customer orders | P0 | FR-IMP |
| UN-004 | Compare the do-nothing case with recovery options | P0 | FR-INT, FR-SIM |
| UN-005 | Know why an option is infeasible | P0 | FR-INT |
| UN-006 | Balance service outcomes against cost and constraints | P0 | FR-OPT |
| UN-007 | Trace numerical results to Db2 facts and rules | P0 | FR-EVD |
| UN-008 | Explain the selected option to leadership | P1 | FR-EXP |
| UN-009 | Reopen a completed decision without changing it | P1 | FR-AUD |
| UN-010 | Continue with a deterministic workflow when AI is unavailable | P1 | FR-EXP |

## Coverage rule

Every P0 need must map to at least one functional requirement and one future
acceptance test. P1 needs may follow after the deterministic vertical slice is
stable.

## User-value boundary

The product reduces analysis time and improves decision traceability. It does
not promise that a disruption will be avoided or that a human will accept the
recommended action.
