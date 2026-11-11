27. Required Phase 3 Repository Structure
Plain Text
config/
├── enterprise.yaml
├── generation.yaml
├── scales/
│ ├── tiny.yaml
│ ├── standard.yaml
│ └── stress.yaml
└── scenarios/
 
src/
├── data_generator/
│ ├── config.py
│ ├── random_streams.py
│ ├── master_data.py
│ ├── demand.py
│ ├── procurement.py
│ ├── production.py
│ ├── inventory.py
│ ├── history.py
│ ├── disruptions.py
│ ├── documents.py
│ └── export.py
└── ground_truth/
├── state.py
├── disruption.py
├── inventory.py
├── scheduling.py
├── customer_impact.py
├── interventions.py
├── ranking.py
└── provenance.py
 
schemas/
├── csv/
├── json/
└── validation/
 
data/
├── README.md
├── manifest.json
├── checksums.sha256
├── generated/
├── golden/
├── benchmarks/
├── fixtures/
└── reports/
 
tests/
├── data_generator/
├── ground_truth/
├── invariants/
└── reproducibility/
 
docs/data/
├── phase-2-handoff-review.md
├── dataset-and-benchmark-contract.md
├── synthetic-enterprise-blueprint.md
├── scale-and-distribution-specification.md
├── identifier-and-serialization-standard.md
├── DATASET_CARD.md
├── privacy-and-licensing-review.md
├── release-notes-v1.0.0.md
├── review-signoff.md
├── phase-3-traceability-matrix.csv
└── phase-3-completion-report.md
 
artifacts/
├── data-validation-report.json
├── dataset-statistics.json
├── distribution-checks.json
├── ground-truth-review.json
└── phase-3-release-manifest.json
