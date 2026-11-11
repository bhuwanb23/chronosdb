13. Phase 0L: Failure Recovery and Backup
Goal

Make sure a machine, database or branch failure cannot destroy the project.

Required recovery controls
Source control
Push foundation branch to remote.
Confirm remote branch contains all committed files.
Record the foundation commit hash.
Do not depend on uncommitted local changes.
Database

## Phase 0 database contains little data, but validate:

Schema recreation script
Seed script
Health-table recreation
Database reset procedure

The system must be reconstructible from code. A database backup alone is not enough.

## Configuration

### Store:

.env.example
Configuration documentation
No real credentials
Recovery drill

### Simulate:

New project directory
Clean clone
Checkout foundation commit
Install dependencies
Configure from .env.example
Start or connect to Db2
Apply Phase 0 SQL
Run health check
Run tests
Run official validator
Target
Full foundation recovery: <30 minutes after dependencies/Db2 image are available
Data required outside repository: 0, apart from credentials
Unrecorded commands: 0
