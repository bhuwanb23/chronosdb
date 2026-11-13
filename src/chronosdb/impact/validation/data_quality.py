from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from ..contracts.enums import DataQualityStatus


class QualitySeverity(StrEnum):
    WARNING = "WARNING"
    CRITICAL_FOR_ENTITY = "CRITICAL_FOR_ENTITY"
    CRITICAL_FOR_RUN = "CRITICAL_FOR_RUN"


@dataclass(frozen=True)
class QualityIssue:
    code: str
    severity: QualitySeverity
    entity_type: str
    entity_id: str
    message: str
    affected_outputs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "message": self.message,
            "affected_outputs": list(self.affected_outputs),
        }


def quality_status(warnings: list[str]) -> DataQualityStatus:
    return DataQualityStatus.PARTIAL if warnings else DataQualityStatus.COMPLETE


def classify_issues(issues: list[QualityIssue]) -> DataQualityStatus:
    if any(issue.severity == QualitySeverity.CRITICAL_FOR_RUN for issue in issues):
        return DataQualityStatus.INSUFFICIENT
    if any(issue.severity == QualitySeverity.CRITICAL_FOR_ENTITY for issue in issues):
        return DataQualityStatus.PARTIAL_CRITICAL
    if issues:
        return DataQualityStatus.PARTIAL_NONCRITICAL
    return DataQualityStatus.COMPLETE
