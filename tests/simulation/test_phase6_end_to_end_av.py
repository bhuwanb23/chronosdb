"""Phase 6 End-to-End Validation (A-V)."""

import unittest
from chronosdb.simulation.phase6a_handoff import Phase5Baseline, validate_phase5_handoff_check
from chronosdb.simulation.phase6b_contract import InterventionOverlay
from chronosdb.simulation.phase6e_baseline import construct_baseline
from chronosdb.simulation.phase6f_transfer import simulate_inventory_transfer
from chronosdb.simulation.phase6g_expedition import simulate_expedition
from chronosdb.simulation.phase6h_alternate_supplier import simulate_alternate_supplier
from chronosdb.simulation.phase6i_production_rescheduling import simulate_production_rescheduling
from chronosdb.simulation.phase6j_hybrid_intervention import simulate_hybrid_intervention
from chronosdb.simulation.phase6k_overlay_engine import OverlayApplicationEngine
from chronosdb.simulation.phase6l_execution_engine import SimulationExecutionEngine
from chronosdb.simulation.phase6m_delta_computation import compute_delta
from chronosdb.simulation.phase6n_counterfactual_causality import CounterfactualCausalityEngine
from chronosdb.simulation.phase6o_ledger import ScenarioLedger, SimulationRun, SimulationInput, SimulationAction, SimulationResult, SimulationDelta
from chronosdb.simulation.phase6p_determinism_replay import DeterminismAndReplayEngine
from chronosdb.simulation.phase6q_golden_scenarios import GoldenInterventionScenarios
from chronosdb.simulation.phase6r_benchmark_evaluation import BenchmarkEvaluationEngine
from chronosdb.simulation.phase6s_performance import PerformanceEngine
from chronosdb.simulation.phase6t_adversarial_tests import AdversarialTestEngine
from chronosdb.simulation.phase6v_release_gate import ReleaseGateEngine
from chronosdb.config.interventions.registry import get_intervention, InterventionType

class TestPhase6EndToEndAV(unittest.TestCase):
    
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
        
        # Setup engines
        self.execution_engine = SimulationExecutionEngine()
        self.overlay_engine = OverlayApplicationEngine()
        self.causality_engine = CounterfactualCausalityEngine()
        self.ledger = ScenarioLedger()
        self.determinism_engine = DeterminismAndReplayEngine(self.execution_engine)
        self.golden_scenarios = GoldenInterventionScenarios()
        self.benchmark_engine = BenchmarkEvaluationEngine()
        self.performance_engine = PerformanceEngine(self.execution_engine)
        self.adversarial_engine = AdversarialTestEngine(self.execution_engine)
        self.release_gate_engine = ReleaseGateEngine()

    def test_phase6a_handoff_validation(self):
        """Test Phase 6A: Verify frozen deterministic baseline."""
        result = validate_phase5_handoff_check(self.phase5_baseline)
        self.assertTrue(result["status"] == "pass")
        self.assertEqual(result["baseline_id"], "BASE-HASH-1234")

    def test_phase6b_c_contract_and_overlay(self):
        """Test Phase 6B/C: Simulation Contract and Overlay Model."""
        overlay_f = InterventionOverlay(
            overlay_id="OVL-TRANSFER-001",
            action="TRANSFER_INVENTORY",
            parameters={"component_id": "CMP-MCU-42", "quantity": "320", "from_warehouse": "WH-CHENNAI", "to_warehouse": "WH-PUNE"}
        )
        self.assertEqual(overlay_f.action, "TRANSFER_INVENTORY")
        
        overlay_g = InterventionOverlay(
            overlay_id="OVL-EXPEDITE-001",
            action="EXPEDITE_PO",
            parameters={"purchase_order_id": "PO-2208", "lead_time_reduction_days": 5}
        )
        self.assertEqual(overlay_g.action, "EXPEDITE_PO")
        
        # Phase 6H Overlay
        overlay_h = InterventionOverlay(
            overlay_id="OVL-SUPPLIER-001",
            action="ALTERNATE_SUPPLIER",
            parameters={"component_id": "CMP-MCU-42", "quantity": "300", "supplier_id": "SUP-0208", "lead_time_days": 3}
        )
        self.assertEqual(overlay_h.action, "ALTERNATE_SUPPLIER")
        
        # Phase 6I Overlay
        overlay_i = InterventionOverlay(
            overlay_id="OVL-RESCHEDULE-001",
            action="RESCHEDULE_PRODUCTION",
            parameters={"manufacturing_orders": ["MO-0876", "MO-0882", "MO-0889"], "new_sequence": ["MO-0882", "MO-0876", "MO-0889"]}
        )
        self.assertEqual(overlay_i.action, "RESCHEDULE_PRODUCTION")

    def test_phase6d_intervention_registry(self):
        """Test Phase 6D: Intervention Registry."""
        reg_transfer = get_intervention(InterventionType.INT_TRANSFER)
        self.assertEqual(reg_transfer.version, "1.0.0")
        
        reg_supplier = get_intervention(InterventionType.INT_SUPPLIER)
        self.assertEqual(reg_supplier.version, "1.0.0")
        
        reg_expedite = get_intervention(InterventionType.INT_EXPEDITE)
        self.assertEqual(reg_expedite.version, "1.0.0")
        
        reg_reschedule = get_intervention(InterventionType.INT_RESCHEDULE)
        self.assertEqual(reg_reschedule.version, "1.0.0")

    def test_phase6e_baseline_identity(self):
        """Test Phase 6E: Identity Rule."""
        baseline2 = construct_baseline(
            phase5_state_hash="HASH-12345678",
            phase5_disruption={"type": "SUPPLIER_OUTAGE", "id": "SUP-01"},
            impact_run_id="IR-002",
            revenue_at_risk=1600000.0,
            sla_breaches=2,
            rule_version="1.0.0",
            horizon={"start_time": "2026-11-14T00:00:00Z", "end_time": "2026-11-21T00:00:00Z"}
        )
        self.assertTrue(self.baseline.identity_check(baseline2))

    def test_phase6f_inventory_transfer_simulator(self):
        """Test Phase 6F: Inventory Transfer Simulator."""
        overlay = InterventionOverlay(
            overlay_id="OVL-TRANSFER-001",
            action="TRANSFER_INVENTORY",
            parameters={"component_id": "CMP-MCU-42", "quantity": "320", "from_warehouse": "WH-CHENNAI", "to_warehouse": "WH-PUNE"}
        )
        rules = type('Rules', (), {'version': '1.0.0'})()
        result = simulate_inventory_transfer(self.baseline, overlay, rules)
        self.assertEqual(result.baseline_id, self.baseline.baseline_id)
        self.assertEqual(result.overlay_id, "OVL-TRANSFER-001")

    def test_phase6g_expedition_simulator(self):
        """Test Phase 6G: Expedition Simulator."""
        overlay = InterventionOverlay(
            overlay_id="OVL-EXPEDITE-001",
            action="EXPEDITE_PO",
            parameters={"purchase_order_id": "PO-2208", "lead_time_reduction_days": 5}
        )
        rules = type('Rules', (), {'version': '1.0.0'})()
        result = simulate_expedition(self.baseline, overlay, rules)
        self.assertEqual(result.baseline_id, self.baseline.baseline_id)
        self.assertEqual(result.overlay_id, "OVL-EXPEDITE-001")

    def test_phase6h_alternate_supplier_simulator(self):
        """Test Phase 6H: Alternate Supplier Simulator."""
        from chronosdb.simulation.phase6h_alternate_supplier import simulate_alternate_supplier
        overlay = InterventionOverlay(
            overlay_id="OVL-SUPPLIER-001",
            action="ALTERNATE_SUPPLIER",
            parameters={"component_id": "CMP-MCU-42", "quantity": "300", "supplier_id": "SUP-0208", "lead_time_days": 3}
        )
        result = simulate_alternate_supplier(self.baseline, overlay, None)
        self.assertEqual(result.baseline_id, self.baseline.baseline_id)
        self.assertEqual(result.overlay_id, "OVL-SUPPLIER-001")
        self.assertEqual(result.modified_supply["event"]["event_type"], "SIM_ALT_SUPPLIER_RECEIPT")

    def test_phase6i_production_rescheduling(self):
        """Test Phase 6I: Production Rescheduling."""
        from chronosdb.simulation.phase6i_production_rescheduling import simulate_production_rescheduling
        overlay = InterventionOverlay(
            overlay_id="OVL-RESCHEDULE-001",
            action="RESCHEDULE_PRODUCTION",
            parameters={"manufacturing_orders": ["MO-0876", "MO-0882", "MO-0889"], "new_sequence": ["MO-0882", "MO-0876", "MO-0889"]}
        )
        result = simulate_production_rescheduling(self.baseline, overlay, None)
        self.assertEqual(result.baseline_id, self.baseline.baseline_id)
        self.assertEqual(result.overlay_id, "OVL-RESCHEDULE-001")

    def test_phase6j_hybrid_intervention_simulator(self):
        """Test Phase 6J: Hybrid Intervention Simulator."""
        from chronosdb.simulation.phase6j_hybrid_intervention import simulate_hybrid_intervention
        overlays = [
            InterventionOverlay(overlay_id="OVL-TRANSFER-001", action="TRANSFER_INVENTORY", parameters={"component_id": "CMP-MCU-42", "quantity": "320", "from_warehouse": "WH-CHENNAI", "to_warehouse": "WH-PUNE"}),
            InterventionOverlay(overlay_id="OVL-SUPPLIER-001", action="ALTERNATE_SUPPLIER", parameters={"component_id": "CMP-MCU-42", "quantity": "300", "supplier_id": "SUP-0208", "lead_time_days": 3}),
            InterventionOverlay(overlay_id="OVL-EXPEDITE-001", action="EXPEDITE_PO", parameters={"purchase_order_id": "PO-2208", "lead_time_reduction_days": 5}),
            InterventionOverlay(overlay_id="OVL-RESCHEDULE-001", action="RESCHEDULE_PRODUCTION", parameters={"manufacturing_orders": ["MO-0876", "MO-0882", "MO-0889"], "new_sequence": ["MO-0882", "MO-0876", "MO-0889"]})
        ]
        result = simulate_hybrid_intervention(self.baseline, overlays, None)
        self.assertEqual(result.baseline_id, self.baseline.baseline_id)
        self.assertEqual(len(result.overlay_ids), 4)
        self.assertEqual(len(result.execution_order), 4)

    def test_phase6k_overlay_application_engine(self):
        """Test Phase 6K: Overlay Application Engine."""
        overlays = [
            InterventionOverlay(overlay_id="OVL-TRANSFER-001", action="TRANSFER_INVENTORY", parameters={"component_id": "CMP-MCU-42", "quantity": "320", "from_warehouse": "WH-CHENNAI", "to_warehouse": "WH-PUNE"})
        ]
        state = self.overlay_engine.apply_overlays(self.baseline, overlays)
        self.assertEqual(state.baseline_id, self.baseline.baseline_id)
        self.assertEqual(len(state.generated_events), 1)
        self.assertIn("revenue_protected", state.derived_state)

    def test_phase6l_execution_engine(self):
        """Test Phase 6L: Simulation Execution Engine."""
        overlays = [
            InterventionOverlay(overlay_id="OVL-TRANSFER-001", action="TRANSFER_INVENTORY", parameters={"component_id": "CMP-MCU-42", "quantity": "320", "from_warehouse": "WH-CHENNAI", "to_warehouse": "WH-PUNE"})
        ]
        result = self.execution_engine.execute_simulation(self.baseline, overlays, "SIM-001")
        self.assertEqual(result.simulation_run_id, "SIM-001")
        self.assertEqual(result.baseline_run_id, "IR-001")
        self.assertIn("revenue_protected", result.simulation_state.derived_state)

    def test_phase6m_delta_computation(self):
        """Test Phase 6M: Delta Computation Engine."""
        from chronosdb.simulation.phase6m_delta_computation import compute_delta
        baseline_metrics = {"revenue_risk": 1600000.0, "breaches": 2, "delay_hours": 288}
        scenario_metrics = {"revenue_risk": 800000.0, "breaches": 1, "delay_hours": 120}
        delta = compute_delta(baseline_metrics, scenario_metrics)
        self.assertEqual(delta["revenue_protected"], 800000.0)
        self.assertEqual(delta["breaches_avoided"], 1)
        self.assertEqual(delta["delay_reduction_hours"], 168)

    def test_phase6n_counterfactual_causality(self):
        """Test Phase 6N: Counterfactual Causality."""
        engine = CounterfactualCausalityEngine()
        baseline_state = {"state_hash": "HASH-12345678", "revenue_risk": 1600000.0, "breaches": 2, "delay_hours": 288}
        scenario_state = {"state_hash": "HASH-12345678", "revenue_risk": 800000.0, "breaches": 1, "delay_hours": 120}
        events = [{"event_type": "SIM_TRANSFER_RECEIPT", "component_id": "CMP-MCU-42"}]
        
        causality = engine.trace_causality(baseline_state, scenario_state, events)
        self.assertIn("causal_chain", causality)
        self.assertIn("evidence_edges", causality)
        self.assertEqual(causality["impact_reduction"]["revenue_protected"], 800000.0)

    def test_phase6o_persistence_and_ledger(self):
        """Test Phase 6O: Persistence and Scenario Ledger."""
        run = SimulationRun("SIM-001", "IR-001", "HASH-123", "RESULT-456", 945)
        input_rec = SimulationInput("BASE-HASH-1234", 1, "5.3.2")
        action = SimulationAction(1, 2)
        result = SimulationResult(800000.0, 1, 168, 755000.0)
        delta = SimulationDelta(800000.0, 1, 168, 1600000.0, 800000.0, 2, 1, 288, 120, 45000.0)
        
        entry_hash = self.ledger.record_simulation(run, input_rec, action, result, delta)
        self.assertIsNotNone(entry_hash)
        
        summary = self.ledger.get_ledger_summary()
        self.assertEqual(summary["total_runs"], 1)

    def test_phase6p_determinism_and_replay(self):
        """Test Phase 6P: Determinism and Replay."""
        overlays = [
            InterventionOverlay(overlay_id="OVL-TRANSFER-001", action="TRANSFER_INVENTORY", parameters={"component_id": "CMP-MCU-42", "quantity": "320", "from_warehouse": "WH-CHENNAI", "to_warehouse": "WH-PUNE"})
        ]
        
        # Determinism test (run 10 times for speed)
        determinism_result = self.determinism_engine.run_determinism_test(self.baseline, overlays, runs=10)
        self.assertTrue(determinism_result["is_deterministic"])
        
        # Replay test
        replay_result = self.determinism_engine.run_replay_test(self.baseline, overlays, "SIM-REPLAY-001")
        self.assertTrue(replay_result["hashes_match"])
        self.assertTrue(replay_result["derived_states_match"])

    def test_phase6q_golden_scenarios(self):
        """Test Phase 6Q: Golden Intervention Scenarios."""
        scenarios = self.golden_scenarios.list_scenarios()
        self.assertGreater(len(scenarios), 0)
        
        scenario1 = self.golden_scenarios.get_scenario("GOLD-TRANSFER-001")
        self.assertEqual(scenario1.scenario_id, "GOLD-TRANSFER-001")
        self.assertEqual(scenario1.expected_revenue_protected, 800000.0)

    def test_phase6r_benchmark_evaluation(self):
        """Test Phase 6R: Benchmark Evaluation."""
        from chronosdb.simulation.phase6l_execution_engine import ExecutionResult
        from chronosdb.simulation.phase6k_overlay_engine import SimulationState
        
        # Mock execution result
        state = SimulationState(
            baseline_id="BASE-HASH-1234",
            overlay_hashes=["OVL-TRANSFER-001"],
            generated_events=[{"event_type": "SIM_TRANSFER_RECEIPT"}],
            derived_state={"revenue_protected": 800000.0, "breaches_avoided": 1, "delay_reduction_hours": 168, "intervention_cost": 0.0, "event_count": 1},
            causal_evidence=["TRANSFER_COMPLETED"],
            runtime_ms=100,
            result_hash="RESULT-456"
        )
        
        result = ExecutionResult(
            simulation_run_id="SIM-001",
            baseline_run_id="IR-001",
            overlay_hash="HASH-123",
            result_hash="RESULT-456",
            runtime_ms=100,
            simulation_state=state,
            persisted_outcomes={}
        )
        
        evaluation = self.benchmark_engine.evaluate_execution(result)
        self.assertTrue(evaluation["passes"])
        self.assertEqual(evaluation["overall_score"], 1.0)

    def test_phase6s_performance(self):
        """Test Phase 6S: Performance."""
        overlays = [
            InterventionOverlay(overlay_id="OVL-TRANSFER-001", action="TRANSFER_INVENTORY", parameters={"component_id": "CMP-MCU-42", "quantity": "320", "from_warehouse": "WH-CHENNAI", "to_warehouse": "WH-PUNE"})
        ]
        
        # Run performance measurement (small number of runs for speed)
        performance = self.performance_engine.measure_performance(self.baseline, overlays, runs=3)
        self.assertTrue(performance["overall_passes"])

    def test_phase6t_adversarial_tests(self):
        """Test Phase 6T: Adversarial Tests."""
        adversarial_results = self.adversarial_engine.run_adversarial_tests(self.baseline)
        self.assertTrue(adversarial_results["all_passed"])
        self.assertEqual(adversarial_results["total_tests"], 10)

    def test_phase6v_release_gate(self):
        """Test Phase 6V: Release Gate."""
        # Mock evaluation results
        evaluation_results = {
            "scores": self.benchmark_engine.targets,
            "targets": self.benchmark_engine.targets,
            "overall_score": 1.0,
            "passes": True,
            "evaluation_timestamp": "2026-11-14T00:00:00Z"
        }
        
        # Mock performance results
        performance_results = {
            "p95_times_ms": self.performance_engine.targets_p95,
            "targets_ms": self.performance_engine.targets_p95,
            "passes": {k: True for k in self.performance_engine.targets_p95.keys()},
            "overall_passes": True,
            "runs_measured": 3,
            "measurement_timestamp": "2026-11-14T00:00:00Z"
        }
        
        # Mock adversarial results
        adversarial_results = {
            "test_results": {},
            "all_passed": True,
            "total_tests": 10,
            "passed_tests": 10,
            "failed_tests": 0,
            "evaluation_timestamp": "2026-11-14T00:00:00Z"
        }
        
        release_gate_result = self.release_gate_engine.evaluate_release_gate(
            evaluation_results, performance_results, adversarial_results
        )
        
        self.assertTrue(release_gate_result["overall_pass"])

if __name__ == "__main__":
    unittest.main()
