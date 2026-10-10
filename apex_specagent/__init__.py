"""Apex_SpecAgent: Sovereign Speculative Tool Execution & Persistent KV-Cache Engine.

Engineered for NVIDIA TensorRT-LLM, NIM, and Blackwell Clusters with Cloudflare Clef,
Hermes Paperclip Adapter, enterprise-ai-production-control-plane, and
enterprise-ai-integration-platform.
"""

__version__ = "1.0.0"

from apex_specagent.orchestrator import ApexSpecAgentOrchestrator
from apex_specagent.core.radix_kv_splicer import RadixKVSplicer
from apex_specagent.core.speculative_action_engine import SpeculativeActionEngine
from apex_specagent.core.batch_interleaver import AsyncBatchInterleaver

__all__ = [
    "ApexSpecAgentOrchestrator",
    "RadixKVSplicer",
    "SpeculativeActionEngine",
    "AsyncBatchInterleaver",
]
