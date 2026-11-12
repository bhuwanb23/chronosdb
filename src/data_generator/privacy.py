"""Privacy, licensing, and retrieval-contamination checks for Phase 3R."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCALES = ("tiny", "standard", "stress")

EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)")
SECRET_PATTERN = re.compile(
    r"(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9._-]{8,}",
    re.IGNORECASE,
)
LEAKAGE_TOKENS = (
    "expected_recommendation",
    "expected_revenue",
    "revenue_at_risk",
    "ground_truth",
    "optimal_set",
    "ignore previous instructions",
)


def scan_documents(root: Path, scale: str | None = None) -> dict[str, Any]:
    """Scan project-authored documents for privacy and answer leakage."""
    scales = (scale,) if scale else SCALES
    documents: list[dict[str, Any]] = []
    for current_scale in scales:
        path = root / "data" / "generated" / "documents" / current_scale / "documents.jsonl"
        documents.extend(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    findings: list[dict[str, str]] = []
    for document in documents:
        text = str(document.get("text", ""))
        document_id = str(document.get("document_id", ""))
        checks = (
            ("PERSONAL_EMAIL", EMAIL_PATTERN.search(text)),
            ("PERSONAL_PHONE", PHONE_PATTERN.search(text)),
            ("SECRET_PATTERN", SECRET_PATTERN.search(text)),
            (
                "ANSWER_LEAKAGE",
                any(token in text.lower() for token in LEAKAGE_TOKENS[:-1]),
            ),
            ("SCENARIO_ID_LEAKAGE", bool(re.search(r"\bSCN-\d{4}\b", text))),
            ("CANDIDATE_ID_LEAKAGE", bool(re.search(r"\bINT-[A-Z0-9-]+\b", text))),
        )
        for code, matched in checks:
            if matched:
                findings.append(
                    {
                        "code": code,
                        "document_id": document_id,
                        "message": f"{code} detected in {document_id}",
                    }
                )
    counts = {
        "documents": len(documents),
        "expired": sum(row.get("status") == "EXPIRED" for row in documents),
        "unauthorized": sum(
            row.get("confidentiality_class") == "UNAUTHORIZED" for row in documents
        ),
        "prompt_injection": sum(
            "ignore previous instructions" in str(row.get("text", "")).lower() for row in documents
        ),
        "project_authored": sum(row.get("source_type") == "PROJECT_AUTHORED" for row in documents),
    }
    return {
        "report_version": "1.0.0",
        "phase": "3R",
        "scales": list(scales),
        "counts": counts,
        "findings": findings,
        "license": {
            "corpus_origin": "PROJECT_AUTHORED",
            "external_corpus_copied": False,
            "repository_license_applies": True,
        },
        "status": "PASS"
        if not findings and counts["project_authored"] == counts["documents"]
        else "FAIL",
    }


def render_privacy_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 3R Privacy and Contamination Review",
        "",
        f"Status: **{report['status']}**",
        "",
        "All evidence documents are project-authored synthetic records. "
        "No personal data, secrets, or expected-answer payloads are permitted.",
        "",
        "## Counts",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in report["counts"].items())
    if report["findings"]:
        lines.extend(["", "## Findings", ""])
        lines.extend(
            f"- `{finding['code']}`: {finding['message']}" for finding in report["findings"]
        )
    else:
        lines.extend(["", "No privacy or contamination findings were detected."])
    return "\n".join(lines) + "\n"
