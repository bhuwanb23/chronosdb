9. Phase 8E: Document Ingestion Pipeline
Pipeline
Load Document
↓
Validate
↓
Extract Metadata
↓
Version Check
↓
Chunk
↓
Embed
↓
Store In Db2

Metadata
{
  "document_id":"DOC-230",
  "type":"SOP",
  "region":"INDIA",
  "effective_from":"2026-01-01",
  "version":"1.2"
}

Deliverables
src/backend/chronosdb/evidence/ingestion/

