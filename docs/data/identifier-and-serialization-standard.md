# Phase 3E: Identifier, Serialization, and Versioning Standard

## Identifiers

IDs are immutable, uppercase, ASCII, hyphen-delimited, and scoped by entity
family: `SUP-000001`, `CMP-000001`, `PRD-000001`, `BOM-000001`,
`CUS-000001`, `LOC-000001`, `FAC-000001`, and `WH-000001`. Human-readable
golden aliases remain explicitly mapped and are never silently reused.

## Serialization

- CSV is UTF-8, comma-delimited, with a header and stable column order.
- JSON is UTF-8, object keys are snake_case and sorted in canonical output.
- Timestamps are ISO-8601 UTC with `Z`.
- Booleans are JSON booleans; missing values are explicit `null`.
- Decimal money and quantities are serialized with fixed decimal precision.
- Rows are sorted by primary key before export.

## Versioning

`dataset_version` is semantic (`MAJOR.MINOR.PATCH`); a changed business
meaning increments MAJOR, a compatible schema/config change increments MINOR,
and a reproducibility or documentation fix increments PATCH. Every manifest
records generator version, config hash, seed, scale, and file hashes.
