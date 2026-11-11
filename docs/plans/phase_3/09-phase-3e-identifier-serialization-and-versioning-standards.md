9. Phase 3E: Identifier, Serialization and Versioning Standards
Goal

Make generated data human-readable, stable, and safe to load.

Identifier conventions

Use deterministic IDs:

Plain Text
SUP-0001 Supplier
CMP-0001 Component
PRD-0001 Product
BOM-0001-V01 BOM version
WH-PUNE Warehouse
FAC-PUNE Facility
PO-000001 Purchase order
MO-000001 Manufacturing/production order
CO-000001 Customer order
COL-000001-01 Customer-order line
EVT-000001 Event
SCN-0001 Scenario
INT-0001-A Intervention

The Phase 2 golden identifiers may remain as aliases or be normalized consistently. Do not maintain two incompatible identifier systems.

Serialization standards
CSV
UTF-8
Header row required
ISO 8601 timestamps
Decimal point as .
Empty field for nullable value
No formulas
No thousands separators
Explicit booleans, preferably true and false
JSON
UTF-8
Valid JSON Schema where practical
ISO 8601 timestamps
Fixed enum strings
Explicit null
Stable key naming using snake_case
Time

Store:

Plain Text
2026-11-11T02:30:00Z

Display:

Plain Text
2026-11-11 08:00 Asia/Kolkata
Dataset version

Use semantic-like dataset versioning:

Plain Text
chronosdb-dataset-v1.0.0
Major version

Breaking domain or semantic change.

Minor version

Backward-compatible added records or scenarios.

Patch version

Correction that does not change intended benchmark semantics.

If a patch alters expected benchmark outcomes, it is at least a minor change and must be explicitly documented.

Manifest

Every release must contain:

JSON
{
"dataset_name": "chronosdb-synthetic-supply-chain",
"version": "1.0.0",
"generator_version": "1.0.0",
"domain_model_version": "2.0",
"random_seed": 260311,
"generated_at": "ISO-8601 timestamp",
"scale": "standard",
"currency": "INR",
"canonical_timezone": "UTC"
}
Deliverables
Plain Text
docs/data/identifier-and-serialization-standard.md
data/manifest.json
