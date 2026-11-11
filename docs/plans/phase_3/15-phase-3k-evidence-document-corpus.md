15. Phase 3K: Evidence-Document Corpus
Goal

Create an original text corpus for later Db2 vector, semantic, and hybrid retrieval.

Document categories
Supplier notices

Examples:

Full plant shutdown
Partial component interruption
Shipment delay
Recovery update
Capacity limitation
Standard operating procedures
Alternate-supplier approval
Emergency inventory transfer
Purchase-order expedition
Production-priority change
Customer escalation
Historical incident reports

Each should contain:

Incident summary
Affected supplier
Components
Operational impact
Intervention
Outcome
Lessons learned
Policies
Customer SLA definition
Safety-stock protection
Spending approval limits
Supplier qualification requirements
Decision-audit policy
Corpus scale

Recommended:

Document type	Count
Supplier notices	60
Historical incidents	60
Procedures	15
Policies	10
Recovery summaries	30
Total	175

With chunking, this should produce several hundred retrieval units.

Document metadata

Every document must include:

Plain Text
document_id
document_type
title
effective_from
effective_to
status
supplier_id
component_ids
region
incident_type
confidentiality_class
version
created_at
source_type
Retrieval relevance sets

For each retrieval benchmark query, define:

Directly relevant documents
Partially relevant documents
Irrelevant documents
Documents that should be filtered out
Expired documents
Unauthorized documents
Contamination controls

Do not generate documents that state the exact expected recommended intervention for the same benchmark scenario. Otherwise, a RAG system may retrieve the answer rather than reason from operational data.

Evidence may explain policy and historical context, but ground truth must come from structured records and deterministic calculations.

Deliverables
Plain Text
data/generated/documents/
├── supplier_notices/
├── incident_reports/
├── procedures/
├── policies/
├── recovery_summaries/
├── document_metadata.jsonl
└── retrieval_relevance.json
