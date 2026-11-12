"""Phase 4F event-sourced inventory ledger generation and replay."""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from .release_export import write_release_csv
from .release_profile import ReleaseProfile, release_root

SIGNS = {
    "OPENING_BALANCE": 1,
    "PURCHASE_RECEIPT": 1,
    "PRODUCTION_RESERVATION": 0,
    "PRODUCTION_ISSUE": -1,
    "PRODUCTION_RETURN": 1,
    "TRANSFER_RESERVATION": 0,
    "TRANSFER_DISPATCH": -1,
    "TRANSFER_RECEIPT": 1,
    "QUARANTINE": -1,
    "RELEASE_FROM_QUARANTINE": 1,
    "POSITIVE_ADJUSTMENT": 1,
    "NEGATIVE_ADJUSTMENT": -1,
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _map(value: str, aliases: dict[str, str]) -> str:
    return aliases.get(value, value)


def replay_ledger(
    opening: list[dict[str, Any]],
    transactions: list[dict[str, Any]],
) -> dict[tuple[str, str], Decimal]:
    balances = {
        (row["warehouse_id"], row["component_id"]): Decimal(str(row["on_hand_quantity"]))
        for row in opening
    }
    for row in sorted(transactions, key=lambda item: (item["event_time"], item["id"])):
        key = (row["warehouse_id"], row["component_id"])
        if row["transaction_type"] not in SIGNS:
            raise ValueError(f"unknown inventory event: {row['transaction_type']}")
        balances.setdefault(key, Decimal("0"))
        balances[key] += Decimal(str(row["quantity"])) * SIGNS[row["transaction_type"]]
    return balances


def build_inventory(
    profile: ReleaseProfile,
    aliases: dict[str, str],
    procurement: dict[str, list[dict[str, Any]]],
    production_batches: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    master_root = profile.root / "data" / "generated" / "master" / profile.source_scale
    source_root = profile.root / "data" / "generated" / "operational" / profile.source_scale
    source_opening = _read_csv(source_root / "inventory_transactions.csv")
    source_master_components = _read_csv(master_root / "components.csv")
    source_master_warehouses = _read_csv(master_root / "warehouses.csv")
    component_ids = [_map(row["id"], aliases) for row in source_master_components]
    warehouse_ids = [_map(row["id"], aliases) for row in source_master_warehouses]
    opening_by_key: dict[tuple[str, str], Decimal] = {}
    for row in source_opening:
        if row["transaction_type"] != "OPENING_BALANCE":
            continue
        key = (_map(row["warehouse_id"], aliases), _map(row["component_id"], aliases))
        opening_by_key[key] = Decimal(row["quantity"])
    opening_by_key[("WH-PUNE", "CMP-MCU-42")] = Decimal("400")
    opening_by_key[("WH-CHENNAI", "CMP-MCU-42")] = Decimal("700")
    opening = [
        {
            "id": f"OPEN-{index:06d}",
            "warehouse_id": warehouse_id,
            "component_id": component_id,
            "on_hand_quantity": str(opening_by_key.get((warehouse_id, component_id), 0)),
            "reserved_quantity": "0",
            "quarantined_quantity": "0",
            "safety_stock_quantity": "120" if component_id == "CMP-MCU-42" and warehouse_id == "WH-CHENNAI" else "100" if component_id == "CMP-MCU-42" else "10",
            "snapshot_time": "2026-11-11T02:30:00Z",
        }
        for index, (warehouse_id, component_id) in enumerate(
            (key for key in sorted(opening_by_key)), start=1
        )
    ]
    transactions = [
        {
            "id": row["id"],
            "warehouse_id": row["warehouse_id"],
            "component_id": row["component_id"],
            "event_time": row["snapshot_time"],
            "transaction_type": "OPENING_BALANCE",
            "quantity": row["on_hand_quantity"],
            "reference_id": row["id"],
        }
        for row in opening
    ]
    reservations = [
        {
            "id": "RES-GOLD-CHENNAI",
            "warehouse_id": "WH-CHENNAI",
            "component_id": "CMP-MCU-42",
            "reserved_quantity": "180",
            "reason": "COMMITTED_LOCAL_DEMAND",
            "effective_time": "2026-11-11T02:30:00Z",
        }
    ]
    transfer_transactions = [
        {
            "id": "TRANSFER-GOLD-001-DISPATCH",
            "transfer_id": "TRANSFER-GOLD-001",
            "source_warehouse_id": "WH-CHENNAI",
            "destination_warehouse_id": "WH-PUNE",
            "component_id": "CMP-MCU-42",
            "transaction_type": "TRANSFER_DISPATCH",
            "quantity": "400",
            "event_time": "2026-11-12T02:30:00Z",
        },
        {
            "id": "TRANSFER-GOLD-001-RECEIPT",
            "transfer_id": "TRANSFER-GOLD-001",
            "source_warehouse_id": "WH-CHENNAI",
            "destination_warehouse_id": "WH-PUNE",
            "component_id": "CMP-MCU-42",
            "transaction_type": "TRANSFER_RECEIPT",
            "quantity": "400",
            "event_time": "2026-11-14T02:30:00Z",
        },
    ]
    for transfer in transfer_transactions:
        warehouse_id = (
            transfer["source_warehouse_id"]
            if transfer["transaction_type"] == "TRANSFER_DISPATCH"
            else transfer["destination_warehouse_id"]
        )
        transactions.append(
            {
                "id": transfer["id"],
                "warehouse_id": warehouse_id,
                "component_id": transfer["component_id"],
                "event_time": transfer["event_time"],
                "transaction_type": transfer["transaction_type"],
                "quantity": transfer["quantity"],
                "reference_id": transfer["transfer_id"],
            }
        )
    for receipt in procurement["receipts"]:
        transactions.append(
            {
                "id": f"INV-{receipt['id']}",
                "warehouse_id": receipt["warehouse_id"],
                "component_id": receipt["component_id"],
                "event_time": receipt["receipt_time"],
                "transaction_type": "PURCHASE_RECEIPT",
                "quantity": receipt["quantity"],
                "reference_id": receipt["purchase_order_id"],
            }
        )
    for batch in production_batches or []:
        if Decimal(str(batch["material_quantity"])) <= 0:
            continue
        transactions.append(
            {
                "id": f"INV-{batch['id']}",
                "warehouse_id": batch["warehouse_id"],
                "component_id": batch["component_id"],
                "event_time": batch["batch_start_time"],
                "transaction_type": "PRODUCTION_ISSUE",
                "quantity": batch["material_quantity"],
                "reference_id": batch["production_order_id"],
            }
        )
    transaction_balances = replay_ledger(opening, transactions)
    snapshots: list[dict[str, Any]] = []
    start = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)
    transactions_by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for transaction in transactions:
        transactions_by_key[
            (transaction["warehouse_id"], transaction["component_id"])
        ].append(transaction)
    for rows in transactions_by_key.values():
        rows.sort(key=lambda row: (row["event_time"], row["id"]))
    snapshot_keys = sorted(opening_by_key)
    if profile.profile == "stress":
        active_components = set(component_ids[:100])
        snapshot_keys = [
            key for key in snapshot_keys if key[1] in active_components
        ]
    for day in range(profile.snapshot_days):
        timestamp = start + timedelta(days=day)
        for warehouse_id, component_id in snapshot_keys:
            key = (warehouse_id, component_id)
            cutoff = timestamp.isoformat().replace("+00:00", "Z")
            on_hand = Decimal("0")
            for transaction in transactions_by_key[key]:
                if transaction["event_time"] > cutoff:
                    break
                on_hand += Decimal(str(transaction["quantity"])) * SIGNS[
                    transaction["transaction_type"]
                ]
            reserved = Decimal("180") if (
                warehouse_id == "WH-CHENNAI" and component_id == "CMP-MCU-42"
            ) else Decimal("0")
            quarantined = Decimal("0")
            available = max(Decimal("0"), on_hand - reserved - quarantined)
            safety = next(
                Decimal(row["safety_stock_quantity"])
                for row in opening
                if row["warehouse_id"] == warehouse_id and row["component_id"] == component_id
            )
            snapshots.append(
                {
                    "id": f"SNAP-P4-{day:03d}-{warehouse_id}-{component_id}",
                    "snapshot_time": timestamp.isoformat().replace("+00:00", "Z"),
                    "warehouse_id": warehouse_id,
                    "component_id": component_id,
                    "on_hand_quantity": str(on_hand),
                    "reserved_quantity": str(reserved),
                    "quarantined_quantity": str(quarantined),
                    "available_quantity": str(available),
                    "safety_stock_quantity": str(safety),
                    "transferable_quantity": str(max(Decimal("0"), available - safety)),
                }
            )
    benchmark_snapshots = snapshots[:: max(1, len(snapshots) // 10)][:10]
    output = release_root(profile) / "inventory"
    write_release_csv(output / "inventory_opening_balances.csv", opening)
    write_release_csv(output / "inventory_transactions.csv", transactions)
    write_release_csv(output / "inventory_reservations.csv", reservations)
    write_release_csv(output / "inventory_snapshots_daily.csv", snapshots)
    write_release_csv(output / "inventory_snapshots_benchmark.csv", benchmark_snapshots)
    write_release_csv(output / "transfer_transactions.csv", transfer_transactions)
    return {
        "opening": opening,
        "transactions": transactions,
        "reservations": reservations,
        "snapshots": snapshots,
        "benchmark_snapshots": benchmark_snapshots,
        "transfer_transactions": transfer_transactions,
        "ending_balances": [
            {
                "warehouse_id": key[0],
                "component_id": key[1],
                "on_hand_quantity": str(value),
            }
            for key, value in sorted(transaction_balances.items())
        ],
        "component_ids": component_ids,
        "warehouse_ids": warehouse_ids,
    }
