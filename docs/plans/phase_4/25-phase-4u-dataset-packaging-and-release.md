25. Phase 4U: Dataset Packaging and Release
Goal

Publish one immutable, documented dataset release.

Final release structure
Plain Text
data/releases/chronosdb-demo-dataset-v1.0.0/
├── README.md
├── DATASET_CARD.md
├── manifest.json
├── checksums.sha256
├── load-order.json
├── master/
├── operations/
├── inventory/
├── production/
├── demand/
├── history/
├── disruptions/
├── interventions/
├── evidence/
├── golden/
├── demo-scenarios/
├── benchmarks/
├── fixtures/
├── expected/
└── reports/
Release manifest

The manifest must include:

Plain Text
dataset name
dataset version
generator version
domain-model version
seed
generation configuration hash
source commit
generation time
release scale
file paths
row counts
checksums
partitions
currency
canonical timezone
license
validation status
Load-order manifest

Example:

JSON
{
"load_order": [
"warehouses",
"facilities",
"suppliers",
"components",
"supplier_component_agreements",
"products",
"bom_versions",
"bom_lines",
"customers",
"sla_policies",
"transfer_lanes",
"purchase_orders",
"production_orders",
"customer_orders",
"customer_order_lines",
"inventory_transactions",
"inventory_snapshots",
"disruption_events",
"evidence_documents",
"benchmark_scenarios"
]
}

The exact order must satisfy all later Db2 foreign-key dependencies.

Release commands
Shell
make dataset-clean
make dataset-build RELEASE=demo VERSION=1.0.0
make dataset-validate RELEASE=demo VERSION=1.0.0
make dataset-ground-truth VERSION=1.0.0
make dataset-package VERSION=1.0.0
make dataset-verify VERSION=1.0.0
Clean-room reproduction

A second clean environment must:

Check out the release commit.
Install locked dependencies.
Generate the dataset.
Produce the same deterministic artifacts.
Validate all files.
Produce the same expected outcomes.
Match checksums.
Package the release.
Version freeze

After release:

Do not modify files in place.
Corrections produce a new version.
Expected-outcome changes require release notes.
The source commit remains recorded.
The benchmark test partition remains frozen.
Deliverables
Plain Text
artifacts/phase-4-release-manifest.json
docs/dataset-release/release-notes-v1.0.0.md
docs/dataset-release/reproduction-report.md
