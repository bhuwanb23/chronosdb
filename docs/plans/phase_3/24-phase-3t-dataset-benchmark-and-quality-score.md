24. Phase 3T: Dataset Benchmark and Quality Score
Goal

Quantify whether the dataset is suitable for implementation and evaluation.

24.1 Referential integrity
RI=valid foreign referencesall foreign referencesRI = \frac{\text{valid foreign references}} {\text{all foreign references}}RI=all foreign referencesvalid foreign references​

Target:

Plain Text
100%
24.2 Domain validity
DV=records satisfying domain rulesrecords subject to domain rulesDV = \frac{\text{records satisfying domain rules}} {\text{records subject to domain rules}}DV=records subject to domain rulesrecords satisfying domain rules​

Target:

Plain Text
100%
24.3 Temporal validity
TV=valid temporal relationshipsall checked temporal relationshipsTV = \frac{\text{valid temporal relationships}} {\text{all checked temporal relationships}}TV=all checked temporal relationshipsvalid temporal relationships​

Target:

Plain Text
100%
24.4 Ground-truth coverage
GTC=frozen scenarios with complete expected outcomesall frozen scenariosGTC = \frac{\text{frozen scenarios with complete expected outcomes}} {\text{all frozen scenarios}}GTC=all frozen scenariosfrozen scenarios with complete expected outcomes​

Target:

Plain Text
100%
24.5 Provenance coverage
PC=expected key outputs with complete provenanceall expected key outputsPC = \frac{\text{expected key outputs with complete provenance}} {\text{all expected key outputs}}PC=all expected key outputsexpected key outputs with complete provenance​

Target:

Plain Text
100%
24.6 Reproducibility
Reproducibility=matching deterministic filesall deterministic output filesReproducibility = \frac{\text{matching deterministic files}} {\text{all deterministic output files}}Reproducibility=all deterministic output filesmatching deterministic files​

Target:

Plain Text
100%
24.7 Partition integrity

Target:

Scenario in multiple exclusive partitions: 0
Test answer leakage into input corpus: 0
Test case used for parameter tuning: 0 documented instances
24.8 Retrieval benchmark readiness

Target:

Queries with relevance labels: at least 50
Relevant documents per query: at least one, except explicit no-match tests
Expired-document filter tests: at least 10
Unauthorized-document filter tests: at least 10
Prompt-injection document tests: at least five
Phase 3 scorecard
Category	Weight
Domain-model conformity	15
Referential and temporal integrity	15
Generator determinism	12
Operational realism	10
Golden scenario correctness	15
Benchmark breadth	10
Ground-truth quality	10
Evidence corpus quality	5
Privacy and licensing	4
Packaging and reproducibility	4
Total	100
Passing threshold
Plain Text
95–100: Pass
90–94: Conditional pass
Below 90: Fail
Automatic failures

Phase 3 fails regardless of score if:

Golden outputs disagree between reviewers.
Inventory conservation fails.
A benchmark recommendation violates a hard constraint.
Expected outcomes are missing.
Generated data contains real private information.
The generator is nondeterministic.
Test-answer leakage is found.
Missing values are silently converted to zero.
Referential-integrity errors remain.
Phase 4 would require manual repair.
Expected outputs are copied into evidence documents.
Dataset version and checksum manifest are absent.
