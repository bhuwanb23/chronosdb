9. Phase 14E: Schema and Data Validation Testing

Validate every schema.

Test Cases
Unknown fields

Wrong types

Missing fields

Negative values

Malformed identifiers


Example

{
  "duration_days": -10
}


Expected

INVALID_DURATION

Deliverable
tests/schema/

