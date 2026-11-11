# Phase 3F: Deterministic Generation Architecture

## Generation order

Locations → facilities/warehouses → transfer lanes → suppliers → components →
supplier-component agreements → products → BOM versions/lines → customers →
SLA policies.

## Randomness contract

Each layer receives a deterministic stream derived from the configured seed and
its named stream ID. Master generation uses stream `master`; demand, supply,
inventory, disruption, documents, and benchmarks use independent reserved
streams. A change in one stream must not reorder another stream.

## Generator contract

`load_config(root, scale, seed)` loads only documented YAML configuration.
`generate_master(config)` returns typed entity rows without filesystem side
effects. `write_master(config, entities)` emits canonical CSV files and a
content-hashed manifest. `validate_master(entities)` raises a validation error
for any broken invariant.

The command-line scripts are thin adapters around these functions. They do not
contain business rules.
