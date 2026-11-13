Phase 5 Deep Dive: Deterministic Impact Engine
Calculate the Cascading Impact of Supply-Chain Disruptions

Phase 4 produced the coherent demonstration dataset and frozen ground truth. Phase 5 now builds the first major computational core of ChronosDB: a deterministic engine that traces a disruption from delayed supply through inventory, manufacturing, customer commitments, SLA exposure, and revenue at risk.

This engine must function without an LLM. Given the same state, disruption, horizon, and rule version, it must always produce exactly the same result, including its intermediate calculations and causal evidence.

