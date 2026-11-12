# Phase 3 Dataset Package

This directory contains the frozen ChronosDB synthetic supply-chain dataset
and its release metadata.

- `generated/`: deterministic master, operational, history, scenario, and
  evidence exports for tiny, standard, and stress scales.
- `golden/`: curated `SCN-GOLD-001` input and frozen expected outputs.
- `benchmarks/`: the 60-scenario catalogue, partitions, and expected outcomes.
- `fixtures/`: invalid, boundary, contradiction, optimization, and retrieval
  fixtures with expected error labels.
- `manifest.json`: package metadata and per-file provenance.
- `checksums.sha256`: global integrity checksums.
- `phase4_load_contract.json`: executable Phase 4 ingestion metadata.

The package is generated with seed `260311`, dataset version `1.0.0`, and UTC
storage timestamps. Generated records must not be manually edited. Use the
repository Make targets or `scripts/data_pipeline.py` to regenerate a new
release candidate.
