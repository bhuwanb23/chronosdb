7. Phase 0F: IBM Db2 Environment Baseline
Goal

Establish a real, stable and documented Db2 environment.

## Environment decision

Select one primary environment and one fallback.

## Recommended primary

IBM Db2 Community Edition, created through the official Db2 Developer Extension or documented container workflow.

The official extension can create a Community Edition instance, create databases and establish connection profiles. It can also browse schemas and execute SQL directly inside Visual Studio Code.

## Recommended fallback

Existing Db2 instance or approved IBM Cloud Db2 environment, if already available.

Do not use SQLite or PostgreSQL as a silent replacement. Those may support isolated unit tests, but the Phase 0 integration test must connect to actual Db2.

### Subphase 0F.1: Instance creation

### Record:

Edition
Version
Container or instance name
Host
Port
Database
Username
Schema
Memory limit
CPU allocation
Storage volume
Initialization time

Do not record passwords.

### Subphase 0F.2: Database creation

### Use a project-specific database where possible:

Database: CHRONOS
Schema: CHRONOS


If database naming is constrained, use a dedicated schema.

### Subphase 0F.3: Connection proof

### Run a minimal query:

VALUES CURRENT SERVER;
VALUES CURRENT TIMESTAMP;
VALUES CURRENT USER;


### Then create a Phase 0 health table:

CREATE TABLE CHRONOS.SYSTEM_HEALTH (
    CHECK_ID VARCHAR(36) NOT NULL PRIMARY KEY,
    COMPONENT VARCHAR(64) NOT NULL,
    STATUS VARCHAR(16) NOT NULL,
    CHECKED_AT TIMESTAMP NOT NULL DEFAULT CURRENT TIMESTAMP,
    DETAILS VARCHAR(512)
);


Insert and retrieve one record.

### Subphase 0F.4: Capability inventory

### Capture whether the selected Db2 environment supports:

Required SQL functionality
Vector data type
Vector distance operations
Vector indexing
Recursive CTEs
JSON features
Role and privilege controls
Explain plans
Required Python driver

Do not assume vector support merely because the project intends to use it. Record the actual Db2 edition and version.

## Db2 foundation benchmark

### Run at least 30 iterations after warm-up:

| Measurement | Phase 0 target |
| --- | --- |
| Connection success rate | 100% |
| SELECT 1 equivalent success | 100% |
| Median connection acquisition | <1 second locally |
| p95 health-query latency | <500 ms locally |
| Insert/read consistency | 100% |
| Restart recovery | <5 minutes |
| Credential leakage | 0 |

These are engineering thresholds, not hackathon performance claims.

Deliverable
artifacts/phase-0/db2-baseline.json


### Example:

{
  "runs": 30,
  "successful_runs": 30,
  "median_query_ms": 42.7,
  "p95_query_ms": 71.3,
  "db2_version": "record-actual-value",
  "vector_capability": "verified-or-unavailable",
  "timestamp": "record-actual-value"
}
