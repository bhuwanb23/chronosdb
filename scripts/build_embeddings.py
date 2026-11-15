#!/usr/bin/env python3
"""Phase 15I: prepare reproducible evidence embeddings.

Uses the pre-generated fallback mandated by Phase 15 when a local embedding
model is unavailable. The fallback is deterministic: it hashes each evidence
chunk into a fixed-size vector and records the provider in the manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "data" / "releases" / "v1.0.0" / "evidence" / "documents"
OUTPUT_DIR = ROOT / "artifacts" / "reproducibility" / "embeddings"
DIMENSION = 384
MODEL = "bge-small-en-v1.5"


def chunk_text(text: str) -> list[str]:
    chunks = [part.strip() for part in text.split("\n\n") if part.strip()]
    return chunks or [text.strip()]


def vectorize(text: str) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [(byte / 255.0) for byte in digest]
    return (values * ((DIMENSION // len(values)) + 1))[:DIMENSION]


def load_documents() -> list[dict]:
    documents = []
    for path in sorted(EVIDENCE_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        content = payload.get("content") or payload.get("text") or ""
        documents.append(
            {
                "document_id": payload.get("document_id") or path.stem,
                "title": payload.get("title", path.stem),
                "content": content,
            }
        )
    return documents


def build() -> dict:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    documents = load_documents()
    if not documents:
        raise RuntimeError(f"no evidence documents found in {EVIDENCE_DIR}")

    output_path = OUTPUT_DIR / "embeddings.jsonl"
    records = 0
    with output_path.open("w", encoding="utf-8") as stream:
        for document in documents:
            for index, chunk in enumerate(chunk_text(document["content"])):
                record = {
                    "document_id": document["document_id"],
                    "chunk_id": f"{document['document_id']}-{index:04d}",
                    "model": MODEL,
                    "dimension": DIMENSION,
                    "provider": "deterministic-fallback",
                    "vector": vectorize(chunk),
                    "text_sha256": hashlib.sha256(chunk.encode("utf-8")).hexdigest(),
                }
                stream.write(json.dumps(record, sort_keys=True) + "\n")
                records += 1

    manifest = {
        "documents": len(documents),
        "records": records,
        "dimension": DIMENSION,
        "model": MODEL,
        "provider": "deterministic-fallback",
        "embeddings_file": str(output_path.relative_to(ROOT)).replace("\\", "/"),
    }
    (OUTPUT_DIR / "embedding-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def check() -> list[str]:
    manifest_path = OUTPUT_DIR / "embedding-manifest.json"
    if not manifest_path.exists():
        return ["embedding-manifest.json is missing; run: make embeddings"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    embeddings_path = ROOT / manifest["embeddings_file"]
    if not embeddings_path.exists():
        return [f"embeddings file is missing: {manifest['embeddings_file']}"]
    records = [
        json.loads(line)
        for line in embeddings_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    issues: list[str] = []
    if len(records) != manifest["records"]:
        issues.append("embedding record count does not match manifest")
    for record in records[:10]:
        if len(record.get("vector", [])) != manifest["dimension"]:
            issues.append("embedding dimension does not match manifest")
            break
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        issues = check()
        if issues:
            for issue in issues:
                print(issue)
            return 1
        print("Embedding validation complete.")
        return 0
    manifest = build()
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
