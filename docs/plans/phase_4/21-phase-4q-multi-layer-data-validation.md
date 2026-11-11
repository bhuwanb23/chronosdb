21. Phase 4Q: Multi-Layer Data Validation
Goal

Prove that the final dataset is structurally and semantically correct.

Validation layer 1: File validation

Check:

File exists
Encoding is UTF-8
Header matches contract
JSON is valid
Row count matches manifest
Checksum matches
Validation layer 2: Type validation

Check:

IDs
Decimals
Booleans
Timestamps
Enums
Nullability
Currency codes
Units
Validation layer 3: Relationship validation

Check:

Foreign references
Valid effective parent
Unique relationship
Valid scenario references
Valid evidence metadata
Validation layer 4: Temporal validation

Check:

Effective interval
Event ordering
No future consumption
No future-information leakage
Valid state transition
Historical replay
Validation layer 5: Operational validation

Check:

Inventory conservation
Purchase-order reconciliation
Production material balance
Facility capacity
Customer allocation
Transfer pairing
Validation layer 6: Financial validation

Check:

Line revenue
Currency
Intervention cost
Supplier premium
Revenue-at-risk bounds
Revenue-protected bounds
Validation layer 7: Scenario validation

Check:

Scenario inputs are valid.
Do-nothing outcome exists.
Candidate set is complete.
Infeasible reasons are documented.
Expected optimum is feasible.
Provenance is complete.
Validation layer 8: Security and document validation

Check:

Access labels
Expired-document filtering metadata
Prompt-injection markers
No secrets
No private data
No expected-answer leakage
Required result
Plain Text
Errors: 0
Undocumented warnings: 0
Golden mismatches: 0
Checksum mismatches: 0
Deliverables
Plain Text
artifacts/phase-4/validation/
├── file-validation.json
├── schema-validation.json
├── relationship-validation.json
├── temporal-validation.json
├── operational-validation.json
├── financial-validation.json
├── scenario-validation.json
├── evidence-validation.json
└── consolidated-validation-report.md
