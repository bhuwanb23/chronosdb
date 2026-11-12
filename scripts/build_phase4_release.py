"""Build one deterministic Phase 4A–4G release profile."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_generator.benchmarks import build_benchmarks
from data_generator.demand import build_demand
from data_generator.disruptions import build_disruptions
from data_generator.evidence import build_evidence
from data_generator.golden import build_golden
from data_generator.history import build_history
from data_generator.interventions import build_interventions
from data_generator.inventory_ledger import build_inventory
from data_generator.manufacturing import build_manufacturing
from data_generator.phase4_validation import (
    validate_benchmark_release,
    validate_capacity,
    validate_demand_release,
    validate_disruptions_release,
    validate_evidence_release,
    validate_golden_release,
    validate_history_release,
    validate_interventions_release,
    validate_inventory_release,
    validate_manufacturing_release,
    validate_master_release,
    validate_procurement,
    validate_supporting_demos_release,
)
from data_generator.procurement import build_procurement
from data_generator.release_export import write_release_json
from data_generator.release_profile import load_release_profile, profile_payload, release_root
from data_generator.release_projection import write_master_release
from data_generator.supporting_demos import build_supporting_demos


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
    manufacturing = build_manufacturing(profile, aliases, master)
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
        master,
    )
    demand = build_demand(profile, aliases, master, manufacturing)
    validate_demand_release(
        demand,
        master,
        manufacturing["production_orders"],
    )
    history = build_history(profile, master, procurement, inventory, demand)
    validate_history_release(history, inventory)
    disruptions = build_disruptions(profile, procurement)
    validate_disruptions_release(disruptions, procurement["purchase_orders"])
    interventions = build_interventions(
        profile,
        inventory,
        procurement,
        manufacturing,
        demand,
        disruptions,
    )
    validate_interventions_release(interventions)
    evidence = build_evidence(profile, aliases)
    validate_evidence_release(evidence)
    golden = build_golden(
        profile,
        master,
        procurement,
        inventory,
        manufacturing,
        demand,
        history,
        disruptions,
        interventions,
        evidence,
    )
    validate_golden_release(golden, evidence)
    demos = build_supporting_demos(profile)
    validate_supporting_demos_release(demos)
    benchmarks = build_benchmarks(
        profile,
        master=master,
        procurement=procurement,
        demand=demand,
        evidence=evidence,
    )
    validate_benchmark_release(
        benchmarks,
        master,
        procurement["purchase_orders"],
        demand,
        history,
        evidence,
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
            "demand_rows": {
                key: len(value) for key, value in demand.items()
            },
            "history_rows": {
                key: len(value)
                for key, value in history.items()
                if isinstance(value, list)
            },
            "disruption_rows": {
                key: len(value) for key, value in disruptions.items()
            },
            "intervention_rows": {
                key: len(value) for key, value in interventions.items()
            },
            "evidence_rows": {
                key: len(value) for key, value in evidence.items()
            },
            "golden_rows": {
                key: len(value) for key, value in golden.items()
                if isinstance(value, list)
            },
            "supporting_demo_rows": {
                key: len(value) for key, value in demos.items()
            },
            "benchmark_rows": {
                key: len(value)
                for key, value in benchmarks.items()
                if isinstance(value, list)
            },
        },
    )
    print(f"Built Phase 4 {profile.profile} release at {output}")


if __name__ == "__main__":
    main()
