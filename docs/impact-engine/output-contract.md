# Impact Output Contract

Every result contains a stable run identity, scenario identity, status,
data-quality status, rule-set version, input-state hash, result hash, affected
entities, headline metrics, causal traces, warnings, errors, and provenance.

`COMPLETED` means all required stages succeeded. `PARTIALLY_COMPLETED` carries
usable outputs and explicit warnings. `REJECTED` and `FAILED` never present a
recommendation as a completed calculation.
