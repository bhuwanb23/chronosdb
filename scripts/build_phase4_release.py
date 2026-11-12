"""Build one deterministic Phase 4A–4G release profile."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_generator.inventory_ledger import build_inventory
from data_generator.manufacturing import build_manufacturing
from data_generator.phase4_validation import (
    validate_capacity,
    validate_inventory_release,
    validate_manufacturing_release,
    validate_master_release,
    validate_procurement,
)
from data_generator.procurement import build_procurement
from data_generator.release_export import write_release_json
from data_generator.release_profile import load_release_profile, profile_payload, release_root
from data_generator.release_projection import write_master_release


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("tiny", "demo", "standard", "stress"), default="demo")
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    profile = load_release_profile(args.root, args.profile, args.version)
    master, aliases = write_master_release(profile)
    validate_master_release(master, require_full_network=profile.profile != "tiny")
    procurement = build_procurement(profile, aliases, master)
    validate_procurement(
        procurement["purchase_orders"],
        procurement["status_history"],
        procurement["receipts"],
        procurement["capacity"],
    )
    manufacturing = build_manufacturing(profile, aliases)
    validate_capacity(manufacturing["batches"], manufacturing["capacity"])
    inventory = build_inventory(
        profile,
        aliases,
        procurement,
        manufacturing["batches"],
    )
    validate_inventory_release(inventory)
    validate_manufacturing_release(
        manufacturing["production_orders"],
        manufacturing["requirements"],
        manufacturing["batches"],
        manufacturing["allocations"],
    )
    output = release_root(profile)
    write_release_json(output / "metadata" / "release_profile.json", profile_payload(profile))
    write_release_json(
        output / "metadata" / "build_summary.json",
        {
            "profile": profile.profile,
            "version": profile.version,
            "master_rows": {key: len(value) for key, value in master.items()},
            "procurement_rows": {
                key: len(value) for key, value in procurement.items()
            },
            "inventory_rows": {
                key: len(value)
                for key, value in inventory.items()
                if isinstance(value, list)
            },
            "manufacturing_rows": {
                key: len(value) for key, value in manufacturing.items()
            },
        },
    )
    print(f"Built Phase 4 {profile.profile} release at {output}")


if __name__ == "__main__":
    main()
