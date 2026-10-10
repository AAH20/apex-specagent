"""Apex_SpecAgent: Comprehensive Unit and Integration Test Suite.

Verifies all speculative action algorithms, Radix KV-cache splicing,
batch interleaving, Cloudflare Clef edge coordination, Hermes Paperclip
budget governance, enterprise control plane, and FlowForge integration.
"""

import unittest
import time
from apex_specagent.core.primitives import (
    SpeculativeActionState,
    BatchAgentState,
    PaperclipTaskState,
)
from apex_specagent.core.radix_kv_splicer import RadixKVSplicer
from apex_specagent.core.speculative_action_engine import SpeculativeActionEngine
from apex_specagent.core.batch_interleaver import AsyncBatchInterleaver
from apex_specagent.adapters.clef_adapter import CloudflareClefAdapter
from apex_specagent.adapters.paperclip_adapter import HermesPaperclipAdapter
from apex_specagent.adapters.control_plane_adapter import ProductionControlPlaneAdapter
from apex_specagent.adapters.integration_platform_adapter import EnterpriseIntegrationPlatformAdapter
from apex_specagent.adapters.aerial_6g_connector import Aerial6GConnector
from apex_specagent.orchestrator import ApexSpecAgentOrchestrator
from apex_specagent.cli import main as cli_main


class TestApexSpecAgent(unittest.TestCase):
    """Test suite covering 100% of Apex_SpecAgent capabilities."""

    def test_speculative_action_prediction_and_dispatch(self):
        engine = SpeculativeActionEngine()
        action = engine.predict_and_dispatch(
            agent_id="agent_01",
            context_hint="git diff",
            predicted_tool="git_diff",
            predicted_args={"target": "HEAD~1"},
        )
        self.assertEqual(action.agent_id, "agent_01")
        self.assertEqual(action.tool_name, "git_diff")
        self.assertEqual(action.status, SpeculativeActionState.EXECUTING)
        self.assertIsNotNone(action.result)
        self.assertLess(action.prediction_latency_us, 500.0)

    def test_speculative_action_verify_and_commit(self):
        engine = SpeculativeActionEngine()
        engine.predict_and_dispatch(
            agent_id="agent_02",
            context_hint="read",
            predicted_tool="view_file",
            predicted_args={"path": "src/main.py"},
        )
        res = engine.verify_and_commit(
            agent_id="agent_02",
            actual_tool="view_file",
            actual_args={"path": "src/main.py"},
        )
        self.assertIsNotNone(res)
        self.assertTrue(res["verified"])
        self.assertTrue(len(res["receipt_hash"]) == 64)
        self.assertEqual(engine.speculative_hit_rate, 100.0)

    def test_speculative_action_mismatch_discard(self):
        engine = SpeculativeActionEngine()
        engine.predict_and_dispatch(
            agent_id="agent_03",
            context_hint="read",
            predicted_tool="view_file",
            predicted_args={"path": "src/main.py"},
        )
        res = engine.verify_and_commit(
            agent_id="agent_03",
            actual_tool="search_web",
            actual_args={"query": "nvidia 6g"},
        )
        self.assertIsNotNone(res)
        self.assertFalse(res["verified"])
        self.assertEqual(engine.discarded_speculations, 1)

    def test_radix_kv_splicer_prefix_insertion_and_matching(self):
        splicer = RadixKVSplicer()
        tokens = [101, 102, 103, 104, 105]
        matched, slot_1, lat = splicer.insert_or_match_prefix(tokens)
        self.assertGreater(slot_1, 0)

        # Re-query same prefix: should match 100% of tokens
        matched_2, slot_2, _ = splicer.insert_or_match_prefix(tokens)
        self.assertEqual(matched_2, len(tokens))
        self.assertEqual(slot_1, slot_2)

    def test_radix_kv_splicer_recomputation_savings(self):
        splicer = RadixKVSplicer()
        base = list(range(1000, 1100))  # 100 base tokens
        tool = list(range(2000, 2020))  # 20 tool tokens

        metrics = splicer.splice_tool_result(base_tokens=base, tool_tokens=tool)
        self.assertEqual(metrics["base_tokens_matched"], 100)
        self.assertEqual(metrics["tool_tokens_spliced"], 20)
        self.assertEqual(metrics["total_context_tokens"], 120)
        self.assertGreaterEqual(metrics["recomputation_saved_pct"], 80.0)

    def test_radix_kv_splicer_cmx_tiering(self):
        splicer = RadixKVSplicer()
        _, slot, _ = splicer.insert_or_match_prefix([1, 2, 3])
        self.assertTrue(splicer.tier_to_cmx(slot))
        self.assertTrue(splicer.slot_registry[slot].is_cmx_tiered)
        self.assertTrue(splicer.restore_from_cmx(slot))
        self.assertFalse(splicer.slot_registry[slot].is_cmx_tiered)

    def test_async_batch_interleaver_parking_and_resume(self):
        interleaver = AsyncBatchInterleaver()
        interleaver.register_agent("agent_park_01")
        interleaver.start_decode_step("agent_park_01", tokens_to_decode=16)

        park_res = interleaver.park_for_tool_call("agent_park_01")
        self.assertEqual(park_res["state"], BatchAgentState.TOOL_WAITING.value)
        self.assertIn("agent_park_01", interleaver.parked_queue)

        resume_res = interleaver.resume_from_tool_call("agent_park_01")
        self.assertEqual(resume_res["state"], BatchAgentState.SPLICING.value)
        self.assertIn("agent_park_01", interleaver.active_batch)

    def test_async_batch_interleaver_gpu_utilization_metrics(self):
        interleaver = AsyncBatchInterleaver()
        interleaver.register_agent("a1")
        interleaver.register_agent("a2")
        interleaver.start_decode_step("a1", tokens_to_decode=32)
        metrics = interleaver.compute_gpu_utilization_metrics()
        self.assertGreater(metrics["interleaved_gpu_utilization_pct"], 75.0)

    def test_cloudflare_clef_adapter_lease_and_sync(self):
        clef = CloudflareClefAdapter()
        lease = clef.acquire_edge_lease(agent_id="clef_agent")
        self.assertTrue(lease.is_active)
        self.assertTrue(clef.verify_edge_lease("clef_agent"))

        sync_res = clef.sync_speculative_kv_prefix(
            agent_id="clef_agent", prefix_hash="hash_123", slot_id=1, tokens_count=500
        )
        self.assertEqual(sync_res["status"], "SYNCHRONIZED")
        self.assertIn("sjc-edge-01", sync_res["replicated_regions"])

    def test_hermes_paperclip_adapter_budget_governance(self):
        paperclip = HermesPaperclipAdapter()
        task = paperclip.create_task(
            task_id="TASK-T-01", goal="Test budget limits", max_usd_budget=0.0001
        )
        paperclip.start_heartbeat(task.task_id)

        # Burn tokens exceeding $0.0001
        burn = paperclip.record_token_burn(
            task.task_id, prompt_tokens=50000, completion_tokens=10000
        )
        self.assertEqual(task.state, PaperclipTaskState.BUDGET_EXCEEDED)

    def test_hermes_paperclip_action_ledger_receipts(self):
        paperclip = HermesPaperclipAdapter()
        task = paperclip.create_task(task_id="TASK-T-02", goal="Test receipts", max_usd_budget=1.0)
        receipt = paperclip.emit_action_receipt(task.task_id, "TEST_ACTION", {"k": "v"})
        self.assertEqual(len(receipt), 64)
        self.assertIn(receipt, task.action_ledger)

    def test_control_plane_adapter_finops_and_routing(self):
        adapter = ProductionControlPlaneAdapter()
        finops = adapter.get_finops_telemetry()
        self.assertIn("GB200", finops.gpu_type)
        self.assertGreater(finops.gpu_cost_per_hour, 0.0)

        route = adapter.route_speculative_batch(batch_size=32)
        self.assertEqual(route["selected_provider"], "onprem_blackwell")

    def test_integration_platform_adapter_transaction_staging_and_commit(self):
        adapter = EnterpriseIntegrationPlatformAdapter()
        tx = adapter.stage_speculative_transaction(
            workflow_id="WF-001",
            target_system="SAP_S4HANA",
            idempotent_key="IDEMP-PO-1001",
            payload={"po_number": 1001, "amount": 4500.0},
        )
        self.assertFalse(tx.committed)

        commit_res = adapter.commit_staged_transaction("IDEMP-PO-1001")
        self.assertEqual(commit_res["status"], "COMMITTED")
        self.assertTrue(len(commit_res["receipt_hash"]) == 64)

        kpis = adapter.compute_workflow_kpis()
        self.assertEqual(kpis["total_committed"], 1)

    def test_aerial_6g_connector_urllc_telemetry(self):
        aerial = Aerial6GConnector()
        res = aerial.bridge_rf_telemetry_to_agent(
            frame_id=101, csi_matrix_dims=[64, 16], agent_id="aerial_agent_1"
        )
        self.assertTrue(res["urllc_compliant"])
        self.assertLess(res["latency_ms"], 5.0)

    def test_orchestrator_full_accelerated_turn_execution(self):
        orchestrator = ApexSpecAgentOrchestrator(default_budget_usd=0.50)
        res = orchestrator.execute_accelerated_turn(
            agent_id="test_agent_full",
            context_tokens=list(range(500, 750)),
            predicted_tool="query_order",
            predicted_args={"order_id": 999},
            actual_tool="query_order",
            actual_args={"order_id": 999},
            tool_output_tokens=list(range(800, 830)),
        )
        self.assertTrue(res["speculative_verified"])
        util_val = float(res["gpu_tensor_utilization"].rstrip("%"))
        self.assertGreaterEqual(util_val, 80.0)
        self.assertTrue(res["enterprise_tx_committed"])
        self.assertTrue(len(res["action_ledger_receipt"]) == 64)

    def test_cli_commands(self):
        self.assertEqual(cli_main(["benchmark", "--iterations", "10"]), 0)
        self.assertEqual(cli_main(["simulate-swarm", "--agents", "3"]), 0)
        self.assertEqual(cli_main(["finops"]), 0)
        self.assertEqual(cli_main(["enterprise"]), 0)


if __name__ == "__main__":
    unittest.main()
