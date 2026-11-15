6. Phase 13B: Benchmark Architecture

Benchmark system must be independent.

Principle

Benchmark code must never:

Read expected answers during execution


Correct Flow

Run ChronosDB
↓
Produce Output
↓
Compare With Ground Truth
↓
Generate Metrics


Not:

Read Ground Truth
↓
Generate Output

Deliverable
docs/benchmark/architecture.md

