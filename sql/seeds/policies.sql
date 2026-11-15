-- Seed data for policies (Phase 15H).
INSERT INTO EVIDENCE.DOCUMENTS (DOCUMENT_ID, TITLE, DOCUMENT_TYPE, SOURCE_PATH, CONTENT, ACCESS_LABEL)
VALUES ('POL-001', 'Supplier disruption policy', 'POLICY', 'sql/seeds/policies.sql', 'Critical supplier outages require a documented recovery plan and audit trail.', 'INTERNAL');
