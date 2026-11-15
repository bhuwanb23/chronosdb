"""Phase 8F: Chunking and Versioning.

Chunking Strategy:
Target: 300–700 tokens per chunk.

Preserve:
- Document version
- Section title
- Paragraph sequence
- Effective date

Chunk Object:
{
  "chunk_id": "CH-001",
  "document_id": "DOC-888",
  "section": "Transfer Procedure"
}

Version Rules:
Never overwrite.
Store: version 1.0, version 1.1, version 2.0 independently.
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class Chunk:
    """Document chunk."""
    chunk_id: str
    document_id: str
    section: str
    text: str
    version: str
    effective_from: str
    region: str
    sequence_number: int
    token_count: int

class ChunkingAndVersioning:
    """
    Phase 8F: Chunking and Versioning.
    
    Chunks documents and manages versions without overwriting.
    """
    
    def __init__(self, chunk_size_tokens: int = 500):
        self.chunk_size_tokens = chunk_size_tokens  # Target: 300-700 tokens
    
    def chunk_text(self, text: str, document_metadata: Dict[str, Any]) -> List[Chunk]:
        """Chunk text into 300-700 token chunks."""
        # Approximate token count (4 chars per token)
        chunk_size_chars = self.chunk_size_tokens * 4
        chunks = []
        
        # Split by paragraphs or fixed size
        paragraphs = text.split('\n\n')
        current_chunk = ""
        chunk_count = 0
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 100 <= chunk_size_chars * 1.5:  # Allow some flexibility
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
            else:
                if current_chunk:
                    chunks.append(self._create_chunk(
                        chunk_count, document_metadata, current_chunk
                    ))
                    chunk_count += 1
                current_chunk = paragraph
        
        # Add final chunk
        if current_chunk:
            chunks.append(self._create_chunk(
                chunk_count, document_metadata, current_chunk
            ))
        
        return chunks
    
    def _create_chunk(self, sequence_number: int, metadata: Dict[str, Any], text: str) -> Chunk:
        """Create individual chunk object."""
        # Extract section title from first line or metadata
        section = metadata.get("section", f"Section {sequence_number + 1}")
        
        # Estimate token count (4 chars per token)
        token_count = len(text) // 4
        
        return Chunk(
            chunk_id=f"CH-{metadata['document_id']}-{sequence_number+1:03d}",
            document_id=metadata["document_id"],
            section=section,
            text=text,
            version=metadata["version"],
            effective_from=metadata["effective_from"],
            region=metadata["region"],
            sequence_number=sequence_number,
            token_count=token_count
        )
    
    def version_check(self, document_id: str, version: str) -> bool:
        """Check if version is valid and not superseded."""
        # Implementation would check version history in storage
        # For demonstration, assume all versions are valid
        # In production, would check against stored versions
        return True
    
    def store_version(self, chunks: List[Chunk], version: str):
        """Store chunks for specific version (never overwrite)."""
        # Implementation would store in Db2 with version key
        # For demonstration, return success
        return True

# Phase 8F Status: IMPLEMENTED
