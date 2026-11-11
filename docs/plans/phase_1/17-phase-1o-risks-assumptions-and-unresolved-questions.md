17. Phase 1O: Risks, assumptions and unresolved questions
Goal

Prevent hidden assumptions from entering the domain model.

Product assumptions to record
A-001

One supplier may supply multiple components.

## A-002

A component may have multiple approved suppliers.

## A-003

Products may require multiple components.

## A-004

A production order is constrained by required component availability.

## A-005

Customer orders are associated with products and delivery commitments.

## A-006

Revenue at risk is the value of projected SLA-breaching orders, not confirmed revenue loss.

## A-007

Recovery cost and revenue at risk use one normalized currency in the MVP.

## A-008

Transportation capacity is simplified to transfer lead time and cost.

## A-009

The MVP uses synthetic data.

## A-010

Interventions require human approval.

Critical product questions Phase 2 must resolve
Domain questions
DOM-001 What exact entities define the supply-chain state?
DOM-002 Can one component substitute for another?
DOM-003 How are BOM effective dates handled?
DOM-004 How is reserved inventory allocated?
DOM-005 What causes a production order to be delayed?
DOM-006 How is customer-order delivery derived?

Temporal questions
TIME-001 What timestamp defines scenario state?
TIME-002 How are late-arriving updates handled?
TIME-003 Are snapshots daily, hourly or event-based?
TIME-004 What happens when records overlap in validity?

Financial questions
FIN-001 What exactly counts as recovery cost?
FIN-002 How is revenue at risk calculated?
FIN-003 Do partial order delays expose full or partial revenue?
FIN-004 How are currency and unit conversions handled?

Optimization questions
OPT-001 How are objectives normalized?
OPT-002 Which constraints are hard?
OPT-003 Which preferences are soft?
OPT-004 How are ties handled?
OPT-005 Can mixed interventions be partially applied?

Product risks
| ID | Risk | Impact | Phase 1 treatment |
| --- | --- | --- | --- |
| P1-R01 | Too many features dilute the core | Critical | Lock Priority 0 and 1 |
| P1-R02 | Revenue-at-risk definition is misleading | High | Define exact rule |
| P1-R03 | AI receives calculation authority | Critical | Enforce AI contract |
| P1-R04 | Simulation looks like prediction | High | Use precise terminology |
| P1-R05 | Requirements cannot be tested | High | Acceptance-test mapping |
| P1-R06 | Db2 appears superficial | Critical | Rubric evidence matrix |
| P1-R07 | Synthetic dataset appears unrealistic | High | Domain rules in Phase 2 |
| P1-R08 | Optimization recommends infeasible action | Critical | Hard feasibility gate |
| P1-R09 | No feasible plan is hidden | High | Explicit no-plan state |
| P1-R10 | Success metrics are decided after results | High | Freeze measurement contract |

Deliverables
docs/product/product-risk-register.md
docs/product/product-assumption-register.md
docs/product/phase-2-question-register.md

