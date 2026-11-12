# ChronosDB Synthetic Supply-Chain Dataset Card

## Identity

- Dataset: `chronosdb-synthetic-supply-chain`
- Version: `1.0.0`
- Seed: `260311`
- Domain model: `2.0`
- Currency: INR
- Storage timezone: UTC

## Origin and intended use

This is a project-authored synthetic dataset generated deterministically for
ChronosDB development, validation, counterfactual simulation, and benchmark
evaluation. It is not a sample of any real enterprise or customer.

The dataset may be used to test referential integrity, temporal reasoning,
inventory conservation, disruption analysis, evidence filtering, and
ground-truth comparison.

## Prohibited interpretation

The records do not represent real supplier performance, market prices,
customer behaviour, operational risk, or enterprise capacity. They must not be
used for production planning, credit decisions, or claims about real
organizations.

## Generation and reproducibility

Master, operational, historical, scenario, and document layers are generated
from the versioned configuration under `config/` with isolated deterministic
random streams. The frozen golden scenario, benchmark catalogue, expected
outputs, fixtures, reports, and checksums are release assets.

## Benchmark partitions

The 60-scenario catalogue is partitioned into development, validation, test,
review-holdout, and adversarial sets. `SCN-GOLD-001` is maintained separately
as the corrected golden scenario and is not silently mixed into the broad
catalogue.

## Limitations and safety

Evidence documents are project-authored synthetic text. Privacy and
contamination scans reject personal-data patterns, secrets, expected-answer
text, candidate recommendation leakage, and scenario identifiers in evidence.
The corpus includes deliberately labelled expired, unauthorized, and
prompt-injection fixtures for retrieval safety testing.

## License and attribution

The dataset and project-authored documents follow the repository license.
External standards are referenced only as domain guidance; no external
incident-report corpus or private procurement data is included.
