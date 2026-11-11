29. Required Phase 4 Repository Structure
Plain Text
config/releases/
├── tiny-v1.0.0.yaml
├── demo-v1.0.0.yaml
├── standard-v1.0.0.yaml
└── stress-v1.0.0.yaml
 
data/releases/
└── chronosdb-demo-dataset-v1.0.0/
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
 
docs/dataset-release/
├── phase-3-intake-report.md
├── demo-story-contract.md
├── dataset-load-contract.md
├── validation-methodology.md
├── golden-scenario-review.md
├── benchmark-freeze-report.md
├── privacy-and-leakage-review.md
├── release-notes-v1.0.0.md
├── reproduction-report.md
├── phase-4-traceability-matrix.csv
└── phase-4-completion-report.md
 
artifacts/phase-4/
├── validation/
├── ground-truth/
├── realism/
├── governance/
├── demo-readiness/
└── phase-4-release-manifest.json
