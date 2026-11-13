from __future__ import annotations

from ..contracts.enums import DataQualityStatus


def quality_status(warnings: list[str]) -> DataQualityStatus:
    return DataQualityStatus.PARTIAL if warnings else DataQualityStatus.COMPLETE
