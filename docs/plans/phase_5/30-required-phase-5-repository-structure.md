30. Required Phase 5 Repository Structure
Plain Text
src/backend/chronosdb/impact/
├── __init__.py
├── contracts/
│ ├── requests.py
│ ├── results.py
│ ├── errors.py
│ └── enums.py
├── rules/
│ ├── registry.py
│ ├── loader.py
│ └── versions.py
├── state/
│ ├── reconstruction.py
│ ├── canonicalization.py
│ ├── hashing.py
│ └── validation.py
├── disruption/
│ ├── validation.py
│ ├── scope.py
│ └── supplier_outage.py
├── supply/
│ ├── outstanding.py
│ ├── receipts.py
│ └── projection.py
├── inventory/
│ ├── events.py
│ ├── timeline.py
│ ├── allocation.py
│ ├── shortage.py
│ └── reconciliation.py
├── materials/
│ ├── bom.py
│ ├── requirements.py
│ └── allocation.py
├── production/
│ ├── batches.py
│ ├── capacity.py
│ ├── priority.py
│ └── scheduler.py
├── fulfilment/
│ ├── product_availability.py
│ ├── allocation.py
│ ├── delivery.py
│ └── sla.py
├── financial/
│ ├── revenue.py
│ ├── delay.py
│ └── metrics.py
├── causality/
│ ├── nodes.py
│ ├── edges.py
│ ├── builder.py
│ └── attribution.py
├── provenance/
│ ├── calculation_trace.py
│ ├── evidence.py
│ └── serializer.py
├── validation/
│ ├── input.py
│ ├── data_quality.py
│ └── invariants.py
├── persistence/
│ ├── repository.py
│ ├── run_store.py
│ └── result_store.py
└── orchestration/
├── pipeline.py
├── stages.py
└── service.py
 
config/rules/
└── impact-rules-v1.0.0.yaml
 
schemas/
├── impact-request.schema.json
├── impact-result.schema.json
└── causal-trace.schema.json
 
tests/impact/
├── unit/
├── property/
├── integration/
├── temporal/
├── golden/
├── benchmark/
└── adversarial/
 
benchmarks/impact/
├── run_impact_benchmark.py
├── compare_ground_truth.py
└── benchmark_config.yaml
 
docs/impact-engine/
├── phase-4-handoff-review.md
├── engine-contract.md
├── input-contract.md
├── output-contract.md
├── rule-catalogue.md
├── state-reconstruction.md
├── disruption-resolution.md
├── inbound-supply-projection.md
├── inventory-timeline.md
├── material-allocation.md
├── shortage-calculation.md
├── production-scheduling.md
├── customer-fulfilment.md
├── sla-and-financial-impact.md
├── causality-and-provenance.md
├── data-quality-and-partial-results.md
├── determinism-contract.md
├── execution-ledger.md
├── observability.md
├── review-signoff.md
├── phase-5-traceability-matrix.csv
└── phase-5-completion-report.md
 
artifacts/phase-5/
├── golden-impact-result.json
├── golden-comparison-report.md
├── impact-benchmark-results.json
├── impact-benchmark-report.md
├── determinism-report.json
└── performance/
