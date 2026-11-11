10. Phase 3F: Deterministic Generation Architecture
Goal

Ensure the same inputs always generate the same records.

Generation contract

The generator must be controlled by:

Generator version
Configuration files
Random seed
Domain-model version
Scale selection

Recommended primary seed:

Plain Text
260311

Meaning can be documented as an arbitrary project seed. Do not derive it from sensitive information.

Required generation stages
Plain Text
1. Load configuration
2. Initialize deterministic random generators
3. Generate locations
4. Generate facilities and warehouses
5. Generate suppliers
6. Generate components
7. Generate supplier-component agreements
8. Generate products and BOMs
9. Generate customers
10. Generate historical demand
11. Generate purchase orders
12. Generate production orders
13. Generate customer orders
14. Generate inventory events
15. Derive inventory snapshots
16. Generate historical disruptions
17. Generate evidence documents
18. Inject benchmark scenarios
19. Calculate expected outcomes
20. Validate all invariants
21. Export datasets
22. Generate checksums and statistics
Randomness isolation

Use separate deterministic random streams:

Plain Text
master_data_seed
demand_seed
supply_seed
inventory_seed
disruption_seed
document_seed
benchmark_seed

This prevents a small change in supplier generation from unexpectedly changing every customer order.

Generator requirements
No network access
No system-time-dependent record values except release metadata
No unseeded randomness
Stable ordering before export
Explicit precision and rounding
Fail-fast validation
Actionable error messages
Non-zero exit on failure
Recommended command contract
Shell
make data-generate SCALE=standard SEED=260311
make data-validate
make ground-truth
make data-report
make data-checksums
Reproducibility test

Generate the dataset twice in separate directories.

After excluding permitted volatile metadata:

Plain Text
SHA-256 checksums must match for every data file.
Deliverables
Plain Text
src/data_generator/
config/generation.yaml
scripts/generate_dataset.py
scripts/validate_dataset.py
scripts/build_ground_truth.py
