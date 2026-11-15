8. Phase 10D: Identity and Access Control
Principle

No component should have more access than required.

Roles
READ_ONLY_APP

Can:

Read operational records


Cannot:

Write operational records

SIMULATION_WRITER

Can:

Write simulation outputs


Cannot:

Modify source data

AUDIT_WRITER

Can:

Write audit logs


Cannot:

Delete audit logs

ADMIN_MIGRATION

Can:

Schema upgrades


Cannot:

Run application workflows

Deliverable
sql/security/roles.sql

