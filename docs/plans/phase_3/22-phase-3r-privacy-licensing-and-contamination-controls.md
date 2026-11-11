22. Phase 3R: Privacy, Licensing and Contamination Controls
Goal

Ensure the dataset is safe to publish and evaluate.

Privacy rules
No real people
No real customer records
No personal email addresses
No phone numbers
No addresses tied to individuals
No employer-confidential information
No private procurement data
No private pricing
No copied incident reports
Naming rules

All organization, supplier, and customer names must be:

Artificially generated
Clearly fictional
Reviewed for accidental real-company collision where practical
Document licensing

Preferred approach:

Generate all documents specifically for the project.
License project-authored dataset and documents consistently with repository policy.
Include attribution only for external standards or public references actually used.
Do not copy IBM documentation into the corpus.
Contamination controls

Prevent:

Expected-answer text inside evidence documents
Scenario IDs inside unrelated documents
Recommendation labels leaking into raw inputs
Test expected outputs appearing in development prompts
Ground-truth JSON being loaded into application retrieval
Dataset declaration

Create a dataset card stating:

Synthetic origin
Intended use
Prohibited interpretation
Known limitations
Generation method
Version
Benchmark partitions
No claim of representing real enterprise performance
Deliverable
Plain Text
docs/data/DATASET_CARD.md
docs/data/privacy-and-licensing-review.md
