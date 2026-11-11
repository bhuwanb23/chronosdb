26. Phase 3 Execution Order

Follow this order. Do not generate large datasets before validating tiny examples and the golden scenario.

Work Block 1: Handoff and contracts
Plain Text
3A. Validate Phase 2 artifacts
3A. Resolve remaining domain decisions
3B. Freeze dataset objectives
3B. Freeze benchmark partitions
3B. Define leakage controls
Work Block 2: Enterprise and scale
Plain Text
3C. Define synthetic organization
3C. Define network and product families
3D. Define entity counts
3D. Define distributions
3D. Define tiny, standard and stress scales
Work Block 3: Standards and generator
Plain Text
3E. Lock identifiers
3E. Lock file formats
3E. Lock versioning
3F. Design generation stages
3F. Isolate random streams
3F. Implement deterministic configuration
Work Block 4: Tiny dataset first
Plain Text
3G. Generate tiny master data
3H. Generate tiny operational data
3I. Generate short history
3P. Validate all invariants

Do not proceed until tiny-scale validation has zero errors.

Work Block 5: Golden scenario
Plain Text
3L. Encode the corrected golden scenario
3N. Implement the transparent oracle
3L. Calculate baseline
3L. Calculate do-nothing
3L. Calculate each intervention
3L. Independently review results
3L. Freeze expected outputs
Work Block 6: Standard dataset
Plain Text
3G. Generate standard master data
3H. Generate operations
3I. Build temporal history
3J. Generate disruptions and interventions
3K. Generate the evidence corpus
Work Block 7: Benchmarks
Plain Text
3M. Construct 60 scenarios
3M. Assign difficulty levels
3M. Freeze partitions
3N. Calculate ground truth
3N. Generate causal traces
3O. Add invalid and adversarial fixtures
Work Block 8: Validation and realism
Plain Text
3P. Run schema validation
3P. Run referential validation
3P. Run domain invariants
3P. Run temporal validation
3P. Run conservation checks
3Q. Calculate descriptive statistics
3Q. Compare observed and target distributions
3Q. Correct generator configuration

Do not manually edit generated records to make statistics appear better. Correct the generator or configuration.

Work Block 9: Safety and packaging
Plain Text
3R. Run privacy review
3R. Run licensing review
3R. Check benchmark leakage
3S. Package files
3S. Generate manifests
3S. Generate checksums
3S. Run clean reproducibility drill
Work Block 10: Freeze and handoff
Plain Text
3T. Calculate Phase 3 score
3U. Run independent review
3U. Resolve release-blocking defects
3U. Freeze dataset v1.0.0
3V. Prepare Phase 4 load contract
