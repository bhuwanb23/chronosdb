from __future__ import annotations

from pathlib import Path

from data_generator.privacy import scan_documents

ROOT = Path(__file__).resolve().parents[2]


def test_project_authored_documents_have_no_privacy_or_answer_leakage() -> None:
    report = scan_documents(ROOT)
    assert report["status"] == "PASS"
    assert report["findings"] == []
    assert report["counts"]["documents"] == 525
    assert report["counts"]["expired"] >= 10
    assert report["counts"]["unauthorized"] >= 10
    assert report["counts"]["prompt_injection"] >= 5
