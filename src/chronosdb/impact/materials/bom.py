from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from ..contracts.requests import parse_time
from ..state.reconstruction import OperationalState


@dataclass(frozen=True)
class BOMVersion:
    bom_version_id: str
    product_id: str
    effective_from: datetime
    effective_to: datetime | None
    version: str


@dataclass(frozen=True)
class BOMLine:
    bom_version_id: str
    line_id: str
    component_id: str
    quantity_per: Decimal
    scrap_factor: Decimal
    mandatory: bool


def select_bom_version(
    state: OperationalState,
    product_id: str,
    planned_start: datetime,
) -> tuple[BOMVersion, tuple[BOMLine, ...]]:
    candidates: list[BOMVersion] = []
    for row in state.get("bom_versions"):
        if row.get("product_id") != product_id:
            continue
        effective_from = parse_time(row["effective_from"])
        effective_to = parse_time(row["effective_to"]) if row.get("effective_to") else None
        if effective_from <= planned_start and (
            effective_to is None or planned_start < effective_to
        ):
            candidates.append(
                BOMVersion(
                    bom_version_id=row["id"],
                    product_id=product_id,
                    effective_from=effective_from,
                    effective_to=effective_to,
                    version=row.get("version", ""),
                )
            )
    if not candidates:
        raise KeyError(f"no BOM active at planned start for {product_id}")
    selected = max(
        candidates,
        key=lambda item: (item.effective_from, item.version, item.bom_version_id),
    )
    lines = tuple(
        sorted(
            (
                BOMLine(
                    bom_version_id=row["bom_version_id"],
                    line_id=row["id"],
                    component_id=row["component_id"],
                    quantity_per=Decimal(row["quantity_per"]),
                    scrap_factor=Decimal(row.get("scrap_factor", "0")),
                    mandatory=row.get("mandatory", "true").lower() == "true",
                )
                for row in state.get("bom_lines")
                if row.get("bom_version_id") == selected.bom_version_id
            ),
            key=lambda item: item.line_id,
        )
    )
    return selected, lines
