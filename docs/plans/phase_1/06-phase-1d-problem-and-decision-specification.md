6. Phase 1D: Problem and decision specification
Goal

Define the exact decision ChronosDB supports.

## Core problem statement

When a critical supplier becomes unavailable, operational dependencies cause delayed components to propagate into inventory shortages, production delays, customer-order breaches and revenue exposure. Existing dashboards show isolated operational facts but do not consistently simulate alternative recovery actions or preserve an auditable explanation of the selected intervention.

## Core decision

Given a supplier disruption, the current operational state, available interventions and business constraints, which feasible intervention produces the best service and financial outcome?

## Decision inputs

## The decision requires:

Disrupted supplier
Disruption start time
Disruption duration
Affected purchase orders
Component supply from that supplier
Current inventory
Reserved inventory
Expected consumption
Bill-of-material dependencies
Production schedule
Customer orders
Customer due dates
Customer priority
Supplier alternatives
Warehouse transfer availability
Intervention budget
Safety-stock rules
Facility capacity
Decision outputs

## The system must return:

Baseline or do-nothing impact
Affected components
Component shortage quantities
Shortage dates
Affected production orders
Production delay days
Affected customer orders
Projected delivery dates
Projected SLA breaches
Revenue at risk
Intervention comparison

## For each candidate:

Intervention type
Required actions
Feasibility status
Rejection reason, when infeasible
Additional cost
Projected delay
SLA breaches
Revenue at risk
Revenue protected relative to do nothing
Operational risks
Score or Pareto position
Supporting evidence
Recommendation
Selected intervention
Selection objective
Active constraints
Trade-offs
Evidence
Calculation version
Scenario run ID
Warnings
Human-review statement
6.1 Key decision distinction

ChronosDB does not make a procurement transaction. It provides a decision-support recommendation.

## The user remains responsible for:

Approving the intervention
Contacting suppliers
Initiating warehouse transfers
Modifying production
Communicating with customers

This distinction reduces safety, governance and credibility risks.

## 6.2 Objective hierarchy

## The application must support at least these objectives:

MINIMIZE_SLA_BREACHES
MINIMIZE_REVENUE_AT_RISK
MINIMIZE_TOTAL_DELAY
MINIMIZE_RECOVERY_COST
BALANCED_RECOVERY


## The MVP demo should default to:

## MINIMIZE_SLA_BREACHES


subject to:

maximum_recovery_cost
minimum_source_safety_stock
approved_supplier_only
facility_capacity
available_inventory

Deliverable
docs/product/decision-specification.md

Exit gate
The decision has defined inputs.
The decision has defined outputs.
The objective is explicit.
Constraints are separated from preferences.
Recommendations are not confused with autonomous actions.
Every numerical output has a future calculation owner.
