5. Phase 1C: Stakeholder and user specification
Goal

Define who uses ChronosDB, who depends on its outputs, and which needs take priority.

5.1 Primary user
Supply-chain operations manager

## The primary user is responsible for:

Monitoring supplier disruptions
Protecting production continuity
Managing inventory allocation
Coordinating warehouses and production facilities
Protecting customer service-level commitments
Controlling recovery expenditure
Explaining recovery decisions to management
Primary-user goals

## The user needs to:

Understand the consequence of a disruption quickly.
Identify the operational bottleneck.
Compare recovery alternatives.
Ensure each alternative is feasible.
Balance service impact against cost.
Explain the recommendation to leadership.
Preserve a record of why the decision was made.
Primary-user pain points
Data is split across suppliers, inventory, production and orders.
Immediate disruption impact is visible, but downstream impact is not.
Spreadsheet analysis is slow and difficult to reproduce.
AI-generated recommendations may contain unsupported numbers.
Recovery options may violate inventory or supplier constraints.
Decisions are difficult to audit after the event.
5.2 Secondary stakeholders
Production planner

## Needs:

Component availability
Production-order impact
Rescheduling possibilities
Facility capacity consequences
Procurement analyst

## Needs:

Alternate supplier availability
Lead-time changes
Supply cost
Supplier qualification status
Warehouse manager

## Needs:

Transferable inventory
Safety-stock constraints
Transfer timing
Source-warehouse impact
Customer-service manager

## Needs:

Affected customer orders
Promised dates
Projected delay
SLA exposure
Finance or business manager

## Needs:

Revenue at risk
Recovery cost
Revenue protected
Trade-off explanation
Auditor or risk reviewer

## Needs:

Scenario inputs
Source records
Rule versions
Candidate interventions
Final recommendation
Timestamps and decision history
5.3 User-priority hierarchy

## When stakeholder goals conflict, ChronosDB should use this default priority:

Data integrity and intervention feasibility
Committed customer service level
Production continuity
Revenue protection
Recovery cost
Convenience or narrative quality

This ordering is a product default, not an immutable business rule. Later phases should make optimization weights configurable.

## 5.4 User-persona specification

Create one detailed primary persona.

Example persona
Name: Ananya Rao
Role: Regional Supply-Chain Operations Manager
Organization type: Electronics manufacturer
Responsibilities:
- 2 production facilities
- 3 warehouses
- 20 active suppliers
- 500 open customer orders

Typical disruption:
A critical microcontroller supplier reports a 14-day delay.

Current process:
ERP exports + spreadsheets + calls to procurement and production.

Current decision time:
Approximately 2–6 hours for a complex disruption.

Desired decision time:
First defensible scenario comparison within 5 minutes.


The persona is synthetic and must be labelled as such.

Deliverables
docs/product/stakeholder-map.md
docs/product/primary-persona.md
docs/product/user-needs.md

Benchmark
User-need coverage
UNC=primary user needs mapped to requirementstotal documented primary user needsUNC = \frac{\text{primary user needs mapped to requirements}} {\text{total documented primary user needs}}

## Target:

## UNC = 100%

