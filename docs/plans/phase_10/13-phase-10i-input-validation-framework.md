13. Phase 10I: Input Validation Framework

Validate:

Supplier Ids

Dates

Durations

Budgets

Scenario Requests

JSON Schemas

Reject
Negative durations

Impossible budgets

Unknown facilities

Malformed dates

Invalid status codes

Error Format
{
  "code":"INVALID_DURATION",
  "message":"Duration must be positive."
}

