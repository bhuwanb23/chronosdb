"""Phase 6 End-to-End Validation (A-G)."""

import unittest
from chronosdb.simulation.phase6a_handoff import Phase5Baseline, validate_phase5_handoff_check
from chronosdb.simulation.phase6b_contract import InterventionOverlay
from chronosdb.simulation.phase6e_baseline import construct_baseline
from chronosdb.simulation.phase6f_transfer import simulate_inventory_transfer
from chronosdb.simulation.phase6g_expedition import simulate_expedition
from chronosdb.config.interventions.registry import get_intervention, InterventionType

class TestPhase6EndToEnd(unittest.TestCase):
    
    def setUp(self):
        # Phase 6A: Handoff Baseline
        self.phase5_baseline = Phase5Baseline(
            state_hash="HASH-12345678",
            impact_run_id="IR-001",
            rule_version="1.0.0",
            golden_result_hash="GOLD-HASH-999",
            golden_revenue_at_risk=1600000.0,
            golden_sla_breaches=2,
            causal_trace_schema="schema-v1",
            determinism_report_hash="DET-HASH-111",
            benchmark_report_hash="BENCH-HASH-222",
            rule_manifest_hash="MANIFEST-HASH-333"
        )
        
        # Phase 6E: Baseline Construction
        self.baseline = construct_baseline(
            phase5_state_hash=self.phase5_baseline.state_hash,
            phase5_disruption={"type": "SUPPLIER_OUTAGE", "id": "SUP-01"},
            impact_run_id=self.phase5_baseline.impact_run_id,
            revenue_at_risk=self.phase5_baseline.golden_revenue_at_risk,
            sla_breaches=self.phase5_baseline.golden_sla_breaches,
            rule_version=self.phase5_baseline.rule_version,
            horizon={"start_time": "2026-11-14T00:00:00Z", "end_time": "2026-11-21T00:00:00Z"}
        )

    def test_phase6a_handoff_validation(self):
        """Test Phase 6A: Verify frozen deterministic baseline."""
        result = validate_phase5_handoff_check(self.phase5_baseline)
        self.assertTrue(result["status"] == "pass")
        self.assertEqual(result["baseline_id"], "BASE-HASH-1234")

    def test_phase6b_c_contract_and_overlay(self):
        """Test Phase 6B/C: Simulation Contract and Overlay Model."""
        # Inventory Transfer Overlay (Phase 6C)
        overlay_f = InterventionOverlay(
            overlay_id="OVL-TRANSFER-001",
            action="TRANSFER_INVENTORY",
            parameters={
                "component_id": "CMP-MCU-42",
                "quantity": "320",
                "from_warehouse": "WH-CHENNAI",
                "to_warehouse": "WH-PUNE"
            }
        )
        self.assertEqual(overlay_f.action, "TRANSFER_INVENTORY")
        
        # Expedition Overlay (Phase 6C)
        overlay_g = InterventionOverlay(
            overlay_id="OVL-EXPEDITE-001",
            action="EXPEDITE_PO",
            parameters={
                "purchase_order_id": "PO-2208",
                "lead_time_reduction_days": 5
            }
        )
        self.assertEqual(overlay_g.action, "EXPEDITE_PO")

    def test_phase6f_inventory_transfer_simulator(self):
        """Test Phase 6F: Inventory Transfer Simulator."""
        overlay = InterventionOverlay(
            overlay_id="OVL-TRANSFER-001",
            action="TRANSFER_INVENTORY",
            parameters={
                "component_id": "CMP-MCU-42",
                "quantity": "320",
                "from_warehouse": "WH-CHENNAI",
                "to_warehouse": "WH-PUNE"
            }
        )
        # Mock rules
        rules = type('Rules', (), {'version': '1.0.0'})()
        
        result = simulate_inventory_transfer(self.baseline, overlay, rules)
        
        self.assertEqual(result.baseline_id, self.baseline.baseline_id)
        self.assertEqual(result.overlay_id, "OVL-TRANSFER-001")
        self.assertEqual(result.modified_supply["event"]["event_type"], "SIM_TRANSFER_RECEIPT")
        self.assertEqual(result.modified_supply["event"]["component_id"], "CMP-MCU-42")
        self.assertEqual(result.modified_supply["event"]["quantity"], "320")

    def test_phase6g_expedition_simulator(self):
        """Test Phase 6G: Expedition Simulator."""
        overlay = InterventionOverlay(
            overlay_id="OVL-EXPEDITE-001",
            action="EXPEDITE_PO",
            parameters={
                "purchase_order_id": "PO-2208",
                "lead_time_reduction_days": 5
            }
        )
        # Mock rules
        rules = type('Rules', (), {'version': '1.0.0'})()
        
        result = simulate_expedition(self.baseline, overlay, rules)
        
        self.assertEqual(result.baseline_id, self.baseline.baseline_id)
        self.assertEqual(result.overlay_id, "OVL-EXPEDITE-001")
        self.assertEqual(result.modified_supply["po_id"], "PO-2208")
        self.assertEqual(result.modified_supply["new_arrival"], "2026-11-22T00:00:00Z")
        self.assertGreater(result.intervention_cost, 0)

    def test_phase6d_intervention_registry(self):
        """Test Phase 6D: Intervention Registry."""
        reg_transfer = get_intervention(InterventionType.INT_TRANSFER)
        self.assertEqual(reg_transfer.version, "1.0.0")
        self.assertIn("component_id", reg_transfer.inputs)
        
        reg_expedite = get_intervention(InterventionType.INT_EXPEDITE)
        self.assertEqual(reg_expedite.version, "1.0.0")
        self.assertIn("purchase_order_id", reg_expedite.inputs)

    def test_phase6e_baseline_identity(self):
        """Test Phase 6E: Identity Rule (Same state/disruption/horizon/rules)."""
        baseline2 = construct_baseline(
            phase5_state_hash="HASH-12345678",  # Same
            phase5_disruption={"type": "SUPPLIER_OUTAGE", "id": "SUP-01"},  # Same
            impact_run_id="IR-002",  # Different run ID is fine as long as state/disruption/horizon/rules match
            revenue_at_risk=1600000.0,
            sla_breaches=2,
            rule_version="1.0.0",
            horizon={"start_time": "2026-11-14T00:00:00Z", "end_time": "2026-11-21T00:00:00Z"}
        )
        self.assertTrue(self.baseline.identity_check(baseline2))

if __name__ == "__main__":
    unittest.main()
