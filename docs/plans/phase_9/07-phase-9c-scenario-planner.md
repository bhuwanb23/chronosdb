7. Phase 9C: Scenario Planner

Purpose:

Convert language into structured requests.

User:

Supplier S-104 is down for 14 days.
Cost ceiling ₹2 lakh.


Planner Output:

{
  "event_type":"SUPPLIER_OUTAGE",
  "supplier_id":"S-104",
  "duration_days":14,
  "objective":"MINIMIZE_SLA_BREACHES",
  "constraints":{
    "max_cost":200000
  }
}

Planner Rules

Output:

JSON ONLY


Never:

recommendations

numbers

predictions

analysis

Deliverables
prompts/planner/

schemas/scenario.schema.json

