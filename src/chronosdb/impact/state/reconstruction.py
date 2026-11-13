from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ..contracts.results import StateIdentity
from .hashing import state_hash
from .validation import validate_state_records


def _time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


@dataclass(frozen=True)
class OperationalState:
    identity: StateIdentity
    records: dict[str, tuple[dict[str, str], ...]]
    warnings: tuple[str, ...] = ()

    def get(self, record_set: str) -> tuple[dict[str, str], ...]:
        return self.records.get(record_set, ())


class ReleaseStateReconstructor:
    def __init__(self, root: Path, profile: str = "demo") -> None:
        release = root / "data" / "releases" / "v1.0.0"
        self.release = release if profile == "demo" else release / profile

    def _read_csv(self, relative: str) -> list[dict[str, str]]:
        path = self.release / relative
        if not path.exists():
            return []
        with path.open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))

    def _read_records(self) -> dict[str, list[dict[str, str]]]:
        mapping = {
            "suppliers": "master/suppliers.csv",
            "supplier_component_agreements": "master/supplier_component_agreements.csv",
            "components": "master/components.csv",
            "products": "master/products.csv",
            "bom_versions": "master/bom_versions.csv",
            "bom_lines": "master/bom_lines.csv",
            "warehouses": "master/warehouses.csv",
            "facilities": "master/facilities.csv",
            "transfer_lanes": "master/transfer_lanes.csv",
            "purchase_orders": "operations/purchase_orders.csv",
            "purchase_order_receipts": "operations/purchase_order_receipts.csv",
            "purchase_order_status_history": "operations/purchase_order_status_history.csv",
            "inventory_opening_balances": "inventory/inventory_opening_balances.csv",
            "inventory_transactions": "inventory/inventory_transactions.csv",
            "inventory_reservations": "inventory/inventory_reservations.csv",
            "inventory_snapshots_daily": "inventory/inventory_snapshots_daily.csv",
            "production_orders": "production/production_orders.csv",
            "production_batches": "production/production_batches.csv",
            "production_material_requirements": "production/production_material_requirements.csv",
            "production_material_allocations": "production/production_material_allocations.csv",
            "production_order_status_history": "production/production_order_status_history.csv",
            "customer_orders": "demand/customer_orders.csv",
            "customer_order_lines": "demand/customer_order_lines.csv",
            "customer_order_status_history": "demand/customer_order_status_history.csv",
            "production_customer_allocations": "demand/production_customer_allocations.csv",
            "customer_sla_assignments": "demand/customer_sla_assignments.csv",
            "disruption_events": "disruptions/disruption_events.csv",
            "disruption_scope_components": "disruptions/disruption_scope_components.csv",
            "disruption_scope_purchase_orders": "disruptions/disruption_scope_purchase_orders.csv",
            "facility_capacity_calendar": "production/facility_capacity_calendar.csv",
        }
        return {name: self._read_csv(path) for name, path in mapping.items()}

    @staticmethod
    def _eligible(row: dict[str, str], as_of: datetime) -> bool:
        effective_from = _time(row.get("effective_from", ""))
        effective_to = _time(row.get("effective_to", ""))
        ingested = _time(row.get("ingested_time", ""))
        return (
            (effective_from is None or effective_from <= as_of)
            and (effective_to is None or as_of < effective_to)
            and (ingested is None or ingested <= as_of)
        )

    @staticmethod
    def _historical(rows: list[dict[str, str]], as_of: datetime) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for row in rows:
            event_time = next(
                (
                    _time(row.get(column, ""))
                    for column in ("transaction_time", "receipt_time", "event_time")
                    if row.get(column)
                ),
                None,
            )
            if event_time is None or event_time <= as_of:
                result.append(row)
        return result

    def reconstruct(self, as_of: datetime) -> OperationalState:
        as_of = as_of.astimezone(UTC)
        records = self._read_records()
        warnings = validate_state_records(records)
        filtered: dict[str, list[dict[str, str]]] = {}
        for name, rows in records.items():
            selected = [
                row for row in rows if self._eligible(row, as_of)
            ]
            if name in {
                "inventory_transactions",
                "purchase_order_receipts",
                "production_order_status_history",
                "customer_order_status_history",
            }:
                selected = self._historical(selected, as_of)
            filtered[name] = sorted(
                selected,
                key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")),
            )
        as_of_value = as_of.isoformat().replace("+00:00", "Z")
        payload: dict[str, object] = {
            "dataset_version": "1.0.0",
            "as_of_time": as_of_value,
            "records": filtered,
        }
        identity = StateIdentity(
            dataset_version="1.0.0",
            state_version="STATE-" + state_hash(payload)[:12].upper(),
            state_hash=state_hash(payload),
            as_of_time=as_of_value,
        )
        return OperationalState(
            identity=identity,
            records={name: tuple(rows) for name, rows in filtered.items()},
            warnings=tuple(warnings),
        )
