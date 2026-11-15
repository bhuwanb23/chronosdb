# Phase 8C: Evidence Domain Model

## Evidence Categories

### Operational Evidence
- Purchase Orders
- Inventory Records
- Transfers
- Production Records
- Customer Orders

### Procedural Evidence
- Warehouse SOPs
- Recovery Playbooks
- Expediting Procedures
- Allocation Policies

### Historical Evidence
- Previous Supplier Incidents
- Prior Disruptions
- Recovery Reports

### Governance Evidence
- SLA Policies
- Supplier Contracts
- Approval Rules
- Risk Guidelines

## Evidence Identity Example
```json
{
  "evidence_id": "EVD-001",
  "type": "PROCEDURAL",
  "source_document": "Warehouse Recovery SOP",
  "version": "1.0",
  "metadata": {
    "document_id": "DOC-230",
    "chunk_id": "CH-012",
    "embedding_model": "bge-small-en-v1.5",
    "dimension": 384,
    "retrieval_score": 0.92,
    "scenario_id": "SCENARIO-GOLD-001",
    "retrieval_run_id": "RUN-20261114-001",
    "region": "INDIA",
    "effective_from": "2026-01-01",
    "version": "1.2"
  }
}
```

## Deliverables
- schemas/evidence.schema.json
- docs/evidence/domain-model.md

## Phase 8C Status: IMPLEMENTED
