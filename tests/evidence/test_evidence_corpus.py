from __future__ import annotations

import json
from pathlib import Path

from data_generator.phase4_validation import validate_evidence_release

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "releases" / "v1.0.0" / "evidence"


def test_evidence_corpus_has_required_controls() -> None:
    evidence = {
        "documents": [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((RELEASE / "documents").glob("*.json"))
        ],
        "metadata": [
            json.loads(line)
            for line in (RELEASE / "document_metadata.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ],
    }
    validate_evidence_release(evidence)
    assert len(evidence["documents"]) == 175
    assert any(
        "ignore previous instructions" in row["text"].lower()
        for row in evidence["documents"]
    )
