"""Phase 4L synthetic evidence corpus and retrieval metadata."""

from __future__ import annotations

import json
from typing import Any

from .release_export import write_release_csv, write_release_json
from .release_profile import ReleaseProfile, release_root

SPECIAL_TEXT = {
    "supplier_notices": (
        "Synthetic supplier notice: supplier SUP-0104 reports a complete "
        "production interruption beginning 11 November 2026. The expected "
        "duration is fourteen days, affected supply is microcontroller material, "
        "and recovery timing remains uncertain."
    ),
    "procedures": (
        "Emergency component transfer procedure: preserve safety stock, obtain "
        "approval before dispatch, attach transfer evidence, and cap transferable "
        "quantity using the active inventory policy."
    ),
    "incident_reports": (
        "Historical microcontroller disruption: a transfer protected one customer "
        "order, alternate supply protected another, and a hybrid plan reduced SLA "
        "exposure in the reviewed incident."
    ),
}


def build_evidence(
    profile: ReleaseProfile,
    aliases: dict[str, str],
) -> dict[str, Any]:
    """Package the fixed 175 synthetic source documents with safe metadata."""
    source = (
        profile.root
        / "data"
        / "generated"
        / "documents"
        / profile.source_scale
        / "documents.jsonl"
    )
    source_rows = [
        json.loads(line)
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    documents: list[dict[str, Any]] = []
    special_indexes: dict[str, int] = {}
    for index, source_row in enumerate(source_rows):
        document_type = source_row["document_type"]
        document_id = source_row["document_id"]
        is_special = False
        if document_type in SPECIAL_TEXT and document_type not in special_indexes:
            special_indexes[document_type] = index
            document_id = f"DOC-GOLD-{document_type.upper()}"
            is_special = True
        supplier_id = aliases.get(source_row["supplier_id"], source_row["supplier_id"])
        component_id = aliases.get(
            source_row["component_ids"], source_row["component_ids"]
        )
        text = SPECIAL_TEXT[document_type] if is_special else source_row["text"]
        text = text.replace("ground-truth", "operational")
        document = {
            "document_id": document_id,
            "document_type": document_type,
            "title": source_row["title"],
            "version": source_row["version"],
            "effective_from": source_row["effective_from"],
            "effective_to": source_row["effective_to"],
            "status": source_row["status"],
            "access_class": (
                "DEMO_INTERNAL"
                if is_special
                else "UNAUTHORIZED"
                if (
                    source_row["confidentiality_class"] == "UNAUTHORIZED"
                    or index == 1
                )
                else "DEMO_INTERNAL"
            ),
            "supplier_id": supplier_id,
            "component_ids": component_id,
            "source_classification": "PROJECT_AUTHORED_SYNTHETIC",
            "synthetic_origin": "true",
            "text": text,
        }
        documents.append(document)
    metadata = [
        {
            key: document[key]
            for key in (
                "document_id",
                "document_type",
                "version",
                "effective_from",
                "effective_to",
                "status",
                "access_class",
                "supplier_id",
                "component_ids",
                "source_classification",
                "synthetic_origin",
            )
        }
        for document in documents
    ]
    labels = [
        {
            "document_id": document["document_id"],
            "access_class": document["access_class"],
            "normal_demo_user_allowed": document["access_class"] != "UNAUTHORIZED",
        }
        for document in documents
    ]
    queries = [
        {
            "query_id": "RET-GOLD-NOTICE",
            "query": "supplier production interruption and recovery uncertainty",
            "required_filters": ["ACTIVE", "DEMO_INTERNAL"],
        },
        {
            "query_id": "RET-GOLD-TRANSFER",
            "query": "emergency component transfer safety stock approval",
            "required_filters": ["ACTIVE", "DEMO_INTERNAL"],
        },
    ]
    relevance = [
        {
            "query_id": query["query_id"],
            "relevant_document_ids": [
                document["document_id"]
                for document in documents
                if (
                    query["query_id"] == "RET-GOLD-NOTICE"
                    and document["document_type"] == "supplier_notices"
                )
                or (
                    query["query_id"] == "RET-GOLD-TRANSFER"
                    and document["document_type"] == "procedures"
                )
            ][:3],
            "filtered_document_ids": [
                document["document_id"]
                for document in documents
                if document["access_class"] == "UNAUTHORIZED"
            ][:3],
        }
        for query in queries
    ]
    output = release_root(profile) / "evidence"
    document_dir = output / "documents"
    document_dir.mkdir(parents=True, exist_ok=True)
    for document in documents:
        write_release_json(document_dir / f"{document['document_id']}.json", document)
    metadata_path = output / "document_metadata.jsonl"
    metadata_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in metadata),
        encoding="utf-8",
    )
    write_release_csv(output / "access_control_labels.csv", labels)
    write_release_json(output / "retrieval_queries.json", queries)
    write_release_json(output / "relevance_labels.json", relevance)
    return {
        "documents": documents,
        "metadata": metadata,
        "access_labels": labels,
        "queries": queries,
        "relevance": relevance,
    }
