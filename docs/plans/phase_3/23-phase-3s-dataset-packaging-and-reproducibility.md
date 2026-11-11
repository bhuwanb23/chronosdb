23. Phase 3S: Dataset Packaging and Reproducibility
Goal

Deliver data in a stable structure ready for Db2 ingestion.

Recommended structure
Plain Text
data/
├── README.md
├── manifest.json
├── checksums.sha256
├── generated/
│ ├── master/
│ ├── operational/
│ ├── history/
│ ├── scenarios/
│ └── documents/
├── golden/
├── benchmarks/
├── fixtures/
└── reports/
Required commands
Shell
make data-clean
make data-generate SCALE=standard SEED=260311
make data-validate
make ground-truth
make data-report
make data-checksums
make data-all

make data-all should:

Remove previous generated output safely.
Generate the dataset.
Generate the evidence corpus.
Build benchmark scenarios.
Calculate expected outcomes.
Validate all records.
Produce statistics.
Generate checksums.
Exit non-zero if any required check fails.
Build isolation

Do not overwrite:

Manually curated configuration
Frozen benchmark definitions
Golden manual calculations
Review signoff

Generated artifacts and curated source inputs must live separately.

Provenance manifest

For every generated file, record:

Plain Text
path
record_count
sha256
generator_stage
configuration
random_seed
schema_version
Reproducibility drill

On a clean checkout:

Install dependencies.
Run make data-all.
Compare checksums.
Run validation.
Compare golden outputs.
Record runtime and hardware.
Targets
Metric	Target
Clean generation success	100%
Validation errors	0
Checksum mismatch	0
Manual edits to generated files	0
Undocumented build step	0
Golden output mismatch	0
