18. Phase 1P: Requirements quality benchmark
Goal

Measure whether the specification is complete enough to enter domain design.

18.1 Requirement coverage
RC=user needs mapped to requirementstotal user needsRC = \frac{\text{user needs mapped to requirements}} {\text{total user needs}}

## Target:

100%

18.2 Use-case coverage
UC=Priority 0 requirements mapped to use casestotal Priority 0 requirementsUC = \frac{\text{Priority 0 requirements mapped to use cases}} {\text{total Priority 0 requirements}}

## Target:

100%

18.3 Acceptance-test coverage
ATC=Priority 0 requirements with acceptance teststotal Priority 0 requirementsATC = \frac{\text{Priority 0 requirements with acceptance tests}} {\text{total Priority 0 requirements}}

## Target:

100%


## Priority 1 target:

≥ 80%

18.4 Rubric traceability
RT=rubric categories with implementation, test, metric and demo evidence5RT = \frac{\text{rubric categories with implementation, test, metric and demo evidence}} {5}

## Target:

100%

## 18.5 Requirement ambiguity rate

Review all mandatory requirements and count those containing undefined qualitative terms.

## Examples:

Fast
Intelligent
User-friendly
Accurate
Scalable
Reliable
Secure
Real-time
Optimal
AR=ambiguous mandatory requirementsall mandatory requirementsAR = \frac{\text{ambiguous mandatory requirements}} {\text{all mandatory requirements}}

## Target:

0%

## 18.6 Orphan requirement rate

An orphan requirement has no user need, use case or acceptance method.

## Target:

0%

## 18.7 Scope stability

Count proposed features that have not been assigned a priority.

## Target:

0

## 18.8 Specification review exercise

Conduct three paper walkthroughs.

Walkthrough A: Normal case
Known supplier
14-day outage
Multiple feasible interventions
One clear best plan
Walkthrough B: No feasible recovery
Severe outage
Insufficient inventory
No approved alternative
Budget too low
Walkthrough C: Incomplete data
Missing inventory snapshot
Conflicting supplier capacity
Incomplete customer due date

## For each walkthrough, verify that the specification determines:

Accepted input
Required calculation
Expected state
User-visible message
Audit behavior
Test behavior
Phase 1 scorecard
| Category | Weight |
| --- | --- |
| Product clarity | 10 |
| User and stakeholder definition | 10 |
| Decision specification | 15 |
| Functional requirement completeness | 15 |
| Non-functional requirements | 10 |
| AI authority controls | 10 |
| Scope discipline | 10 |
| Rubric alignment | 10 |
| Measurement contract | 5 |
| Acceptance-test coverage | 5 |
| Total | 100 |

Passing threshold
95–100: Pass
90–94: Conditional pass
Below 90: Fail

## Automatic failures

## Phase 1 fails regardless of score if:

The primary user is undefined.
The decision output is undefined.
Revenue at risk remains undefined.
The LLM is allowed to generate business calculations.
MVP scope is not locked.
A Priority 0 requirement lacks a verification approach.
Db2 depth has no planned proof.
“No feasible intervention” is not handled.
Insufficient data is treated as zero.
Success metrics are postponed until after implementation.
