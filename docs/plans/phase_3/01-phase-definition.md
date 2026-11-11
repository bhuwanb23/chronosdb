1. Phase Definition
Phase name

Dataset Engineering and Ground-Truth Construction

Primary goal

Build a reproducible synthetic supply-chain dataset and frozen evaluation suite that:

Conforms to every Phase 2 domain rule.
Supports the locked supplier-outage scenario.
Exercises normal, edge, failure, and adversarial conditions.
Produces independently verifiable expected outcomes.
Can be seeded into IBM Db2 repeatedly.
Supports structured queries and later vector retrieval.
Enables fair comparison between ChronosDB and benchmark baselines.
Contains no private, copyrighted, or real customer information.
Required result

At the end of Phase 3, we must have:

A versioned dataset specification
A deterministic synthetic-data generator
Referentially valid operational data
Historical snapshots and events
Evidence documents for later Db2 vector retrieval
A corrected and frozen golden scenario
A benchmark scenario catalogue
Machine-readable expected outcomes
Negative and adversarial test fixtures
Dataset-quality reports
Dataset cards and limitations
Reproduction commands
Dataset checksums
A clean handoff to Phase 4
