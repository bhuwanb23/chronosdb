from __future__ import annotations

import csv
import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

from ..contracts.errors import StateReconstructionError
from ..contracts.results import StateIdentity
from .hashing import state_hash
from .validation import validate_state_records

TEMPORAL_COLUMNS = (
    "actual_arrival_time",
    "actual_completion_time",
    "actual_start_time",
    "confirmed_time",
    "effective_from",
    "effective_time",
    "effective_state_time",
    "effective_to",
    "end_time",
    "event_time",
    "expected_arrival_time",
    "expected_completion_time",
    "expected_end_time",
    "ingested_time",
    "order_time",
    "planned_completion_time",
    "planned_start_time",
    "receipt_time",
    "recorded_at",
    "reported_time",
    "snapshot_time",
    "start_time",
    "transaction_time",
)


class _ImmutableDict(dict[str, Any]):
    """Dict-compatible immutable snapshot value used by the state cache."""

    def _blocked(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("cached operational state is immutable")

    __setitem__ = __delitem__ = clear = pop = popitem = setdefault = update = _blocked  # type: ignore[assignment]
    __ior__ = _blocked  # type: ignore[assignment]

    def __deepcopy__(self, memo: dict[int, Any]) -> _ImmutableDict:
        return self


def _freeze_state(state: OperationalState) -> OperationalState:
    def freeze(value: Any) -> Any:
        if isinstance(value, dict):
            return _ImmutableDict({key: freeze(item) for key, item in value.items()})
        if isinstance(value, list):
            return tuple(freeze(item) for item in value)
        return value

    records = _ImmutableDict(
        {
            name: tuple(_ImmutableDict(row) for row in rows)
            for name, rows in state.records.items()
        }
    )
    return OperationalState(
        identity=state.identity,
        records=records,
        warnings=state.warnings,
        scenario_inputs=tuple(freeze(item) for item in state.scenario_inputs),
    )


def _time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(UTC)
    except ValueError:
        return None


def _validate_temporal_fields(row: dict[str, str]) -> None:
    for column in TEMPORAL_COLUMNS:
        value = row.get(column, "")
        if value and _time(value) is None:
            raise StateReconstructionError(
                f"invalid {column} timestamp in record {row.get('id', '<unknown>')}"
            )


@dataclass(frozen=True)
class OperationalState:
    identity: StateIdentity
    records: dict[str, tuple[dict[str, str], ...]]
    warnings: tuple[str, ...] = ()
    scenario_inputs: tuple[dict[str, Any], ...] = ()

    def get(self, record_set: str) -> tuple[dict[str, str], ...]:
        return self.records.get(record_set, ())


class ReleaseStateReconstructor:
    _record_cache: ClassVar[
        dict[tuple[str, str], dict[str, list[dict[str, str]]]]
    ] = {}
    _state_cache: ClassVar[
        dict[tuple[str, str, str], OperationalState]
    ] = {}
    _max_cache_entries: ClassVar[int] = 16

    def __init__(self, root: Path, profile: str = "demo") -> None:
        release = root / "data" / "releases" / "v1.0.0"
        self.release = release if profile == "demo" else release / profile

    def _read_csv(self, relative: str) -> list[dict[str, str]]:
        path = self.release / relative
        if not path.exists():
            return []
        with path.open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))

    def _source_fingerprint(self) -> str:
        digest = hashlib.sha256()
        for path in sorted(
            path
            for path in self.release.rglob("*")
            if path.is_file()
            and path.suffix in {".csv", ".json"}
            and path.relative_to(self.release).parts[0]
            not in {"tiny", "standard", "stress"}
        ):
            digest.update(path.relative_to(self.release).as_posix().encode("utf-8"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
        return digest.hexdigest()

    def _read_records(self) -> dict[str, list[dict[str, str]]]:
        source_fingerprint = getattr(self, "_active_source_fingerprint", None)
        if source_fingerprint is None:
            source_fingerprint = self._source_fingerprint()
        cache_key = (self.release.as_posix(), source_fingerprint)
        cached = self._record_cache.get(cache_key)
        if cached is not None:
            return deepcopy(cached)
        mapping = {
            "suppliers": "master/suppliers.csv",
            "supplier_component_agreements": "master/supplier_component_agreements.csv",
            "components": "master/components.csv",
            "products": "master/products.csv",
            "bom_versions": "master/bom_versions.csv",
            "bom_lines": "master/bom_lines.csv",
            "warehouses": "master/warehouses.csv",
            "facilities": "master/facilities.csv",
            "warehouse_facility_links": "master/warehouse_facility_links.csv",
            "transfer_lanes": "master/transfer_lanes.csv",
            "purchase_orders": "operations/purchase_orders.csv",
            "purchase_order_receipts": "operations/purchase_order_receipts.csv",
            "purchase_order_status_history": "operations/purchase_order_status_history.csv",
            "inventory_opening_balances": "inventory/inventory_opening_balances.csv",
            "inventory_transactions": "inventory/inventory_transactions.csv",
            "transfer_transactions": "inventory/transfer_transactions.csv",
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
        records = {name: self._read_csv(path) for name, path in mapping.items()}
        self._record_cache[cache_key] = deepcopy(records)
        while len(self._record_cache) > self._max_cache_entries:
            self._record_cache.pop(next(iter(self._record_cache)))
        return records

    @classmethod
    def clear_cache(cls) -> None:
        cls._record_cache.clear()
        cls._state_cache.clear()

    def _read_scenario_inputs(self) -> tuple[dict[str, Any], ...]:
        paths = []
        golden = self.release / "golden" / "scenario.json"
        if golden.exists():
            paths.append(golden)
        benchmark_directory = self.release / "benchmarks" / "scenarios"
        if benchmark_directory.exists():
            paths.extend(sorted(benchmark_directory.glob("*.json")))
        scenarios: list[dict[str, Any]] = []
        for path in paths:
            with path.open(encoding="utf-8") as stream:
                payload = json.load(stream)
            if isinstance(payload, dict):
                scenarios.append(payload)
        return tuple(scenarios)

    @staticmethod
    def _eligible(row: dict[str, str], as_of: datetime) -> bool:
        _validate_temporal_fields(row)
        effective_from = _time(row.get("effective_from", ""))
        effective_time = _time(row.get("effective_time", ""))
        effective_to = _time(row.get("effective_to", ""))
        effective_state = _time(row.get("effective_state_time", ""))
        ingested = _time(row.get("ingested_time", ""))
        order_time = _time(row.get("order_time", ""))
        start_time = _time(row.get("start_time", ""))
        reported_time = _time(row.get("reported_time", ""))
        confirmed_time = _time(row.get("confirmed_time", ""))
        disruption_visible = (
            reported_time is None and (start_time is None or start_time <= as_of)
        ) or (reported_time is not None and (reported_time <= as_of or start_time == as_of))
        return (
            (effective_from is None or effective_from <= as_of)
            and (effective_time is None or effective_time <= as_of)
            and (effective_state is None or effective_state <= as_of)
            and (effective_to is None or as_of < effective_to)
            and (ingested is None or ingested <= as_of)
            and (order_time is None or order_time <= as_of)
            and disruption_visible
            and (confirmed_time is None or confirmed_time <= as_of)
        )

    @staticmethod
    def _historical(rows: list[dict[str, str]], as_of: datetime) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for row in rows:
            _validate_temporal_fields(row)
            event_time = None
            for column in (
                "transaction_time",
                "receipt_time",
                "event_time",
                "snapshot_time",
            ):
                if row.get(column):
                    event_time = _time(row[column])
                    break
            if event_time is None or event_time <= as_of:
                result.append(row)
        return result

    @staticmethod
    def _latest_snapshots(rows: list[dict[str, str]]) -> list[dict[str, str]]:
        latest: dict[tuple[str, str], dict[str, str]] = {}
        for row in rows:
            key = (row.get("warehouse_id", ""), row.get("component_id", ""))
            current = latest.get(key)
            snapshot_time = _time(row.get("snapshot_time", ""))
            current_time = _time(current.get("snapshot_time", "")) if current else None
            candidate_key = (
                snapshot_time or datetime.min.replace(tzinfo=UTC),
                row.get("id", ""),
            )
            current_key = (
                current_time or datetime.min.replace(tzinfo=UTC),
                current.get("id", "") if current else "",
            )
            if current is None or candidate_key > current_key:
                latest[key] = row
        return list(latest.values())

    @staticmethod
    def _reconcile_statuses(
        filtered: dict[str, list[dict[str, str]]],
    ) -> None:
        reconciliations = (
            ("purchase_orders", "purchase_order_status_history", "id", "purchase_order_id"),
            (
                "production_orders",
                "production_order_status_history",
                "id",
                "production_order_id",
            ),
            (
                "customer_orders",
                "customer_order_status_history",
                "customer_order_id",
                "customer_order_id",
            ),
        )
        for base_name, history_name, base_id, history_id in reconciliations:
            latest: dict[str, tuple[datetime, str, str]] = {}
            for event in filtered[history_name]:
                event_time = _time(event.get("event_time", ""))
                record_id = event.get(history_id, "")
                if event_time is None or not record_id:
                    continue
                candidate = (
                    event_time,
                    event.get("id", ""),
                    event.get("status", ""),
                )
                current = latest.get(record_id)
                if current is None or candidate[:2] > current[:2]:
                    latest[record_id] = candidate
            filtered[base_name] = [
                {
                    **row,
                    "status": latest[row[base_id]][2],
                }
                if row.get(base_id) in latest
                else row
                for row in filtered[base_name]
            ]

    def reconstruct(self, as_of: datetime) -> OperationalState:
        if as_of.tzinfo is None:
            raise StateReconstructionError("as_of timestamp must include timezone")
        as_of = as_of.astimezone(UTC)
        standard_reader = (
            getattr(self._read_records, "__func__", None)
            is ReleaseStateReconstructor._read_records
        )
        source_fingerprint = self._source_fingerprint()
        cache_key = (
            self.release.as_posix(),
            source_fingerprint,
            as_of.isoformat(),
        )
        if standard_reader and cache_key in self._state_cache:
            # Release snapshots are immutable inputs; sharing the cached state
            # avoids re-copying the full snapshot on every deterministic replay.
            return self._state_cache[cache_key]
        self._active_source_fingerprint = source_fingerprint
        try:
            records = self._read_records()
        finally:
            del self._active_source_fingerprint
        filtered: dict[str, list[dict[str, str]]] = {}
        for name, rows in records.items():
            selected = [row for row in rows if self._eligible(row, as_of)]
            if name in {
                "inventory_transactions",
                "transfer_transactions",
                "inventory_opening_balances",
                "inventory_snapshots_daily",
                "purchase_order_receipts",
                "purchase_order_status_history",
                "production_order_status_history",
                "customer_order_status_history",
            }:
                selected = self._historical(selected, as_of)
            if name == "inventory_snapshots_daily":
                selected = self._latest_snapshots(selected)
            filtered[name] = sorted(
                selected,
                key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")),
            )
        self._reconcile_statuses(filtered)
        warnings = validate_state_records(filtered)
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
        state = OperationalState(
            identity=identity,
            records={name: tuple(rows) for name, rows in filtered.items()},
            warnings=tuple(warnings),
            scenario_inputs=self._read_scenario_inputs(),
        )
        if standard_reader:
            self._state_cache[cache_key] = _freeze_state(state)
            while len(self._state_cache) > self._max_cache_entries:
                self._state_cache.pop(next(iter(self._state_cache)))
        return state
