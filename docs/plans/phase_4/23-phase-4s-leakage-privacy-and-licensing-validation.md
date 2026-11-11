23. Phase 4S: Leakage, Privacy and Licensing Validation
Goal

Ensure the release is publishable and benchmark-valid.

Privacy validation

Search all data and documents for:

Real personal names
Email addresses
Phone numbers
Personal addresses
Credentials
Tokens
Real private customer data
Confidential enterprise identifiers

Expected:

Plain Text
Private or personal records: 0
Secrets: 0
Synthetic-origin validation

Every public-facing dataset package must state:

Organization is fictional.
Suppliers are fictional.
Customers are fictional.
Prices are synthetic.
Incidents are synthetic.
Results are not commercial forecasts.
Benchmark-leakage validation

Search the evidence corpus for:

Scenario IDs
Expected recommendation IDs
Exact expected output JSON
“Correct answer” phrasing
Test-set labels
Expected scores
Ground-truth causal paths copied verbatim

Expected:

Plain Text
Test-answer leakage: 0
Split leakage

Check that near-duplicate scenarios do not span development and test partitions unless intentionally included as a robustness pair.

Recommended similarity review features:

Same supplier
Same component
Same disruption duration
Same inventory state
Same customer orders
Same intervention outcome

If all key fields are the same, treat them as duplicates.

Licensing validation
Dataset text is project-authored.
External standards are referenced, not copied.
No third-party documentation is reproduced substantially.
License metadata is included.
Synthetic documents use the repository-compatible license.
Deliverables
Plain Text
artifacts/phase-4/governance/
├── privacy-scan-report.md
├── secret-scan-report.md
├── benchmark-leakage-report.md
├── split-similarity-report.md
└── licensing-review.md
