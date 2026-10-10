"""Apex_SpecAgent: Institutional Core Primitives & Data Structures.

Defines formal types for speculative action branching, Radix KV-cache splicing,
asynchronous batch interleaving, Cloudflare Clef edge synchronization,
Hermes Paperclip Company OS governance, and enterprise control plane integrations.
"""

import time
import enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class SpeculativeActionState(enum.Enum):
    """Lifecycle states for speculative agent actions."""
    PREDICTED = "PREDICTED"
    EXECUTING = "EXECUTING"
    COMMITTED = "COMMITTED"
    DISCARDED = "DISCARDED"
    FAILED = "FAILED"


class BatchAgentState(enum.Enum):
    """Runtime execution state for an agent within the async batch scheduler."""
    IDLE = "IDLE"
    DECODING = "DECODING"
    TOOL_WAITING = "TOOL_WAITING"
    SPLICING = "SPLICING"
    COMPLETED = "COMPLETED"


class PaperclipTaskState(enum.Enum):
    """Paperclip Company OS task state machine."""
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    MAX_HEARTBEATS = "MAX_HEARTBEATS"


@dataclass
class SpeculativeAction:
    """Represents a speculatively predicted and executed tool action."""
    action_id: str
    agent_id: str
    tool_name: str
    arguments: Dict[str, Any]
    confidence: float
    status: SpeculativeActionState = SpeculativeActionState.PREDICTED
    result: Optional[Any] = None
    prediction_latency_us: float = 0.0
    execution_latency_us: float = 0.0
    receipt_hash: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class RadixKVNode:
    """Node in the persistent Radix Trie KV-cache prefix structure."""
    prefix_tokens: List[int]
    slot_id: int
    children: Dict[int, "RadixKVNode"] = field(default_factory=dict)
    ref_count: int = 1
    hit_count: int = 0
    is_cmx_tiered: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def token_length(self) -> int:
        return len(self.prefix_tokens)


@dataclass
class BatchInterleavingSlot:
    """Execution context for an agent inside the asynchronous batch interleaver."""
    agent_id: str
    state: BatchAgentState = BatchAgentState.IDLE
    current_turn: int = 0
    context_tokens: int = 0
    parked_timestamp_ns: int = 0
    total_decode_tokens: int = 0
    priority: int = 1


@dataclass
class ClefEdgeLease:
    """Cloudflare Clef distributed edge coordination lease."""
    lease_id: str
    edge_location: str
    token: str
    ttl_seconds: int = 60
    issued_at: float = field(default_factory=time.time)
    is_active: bool = True


@dataclass
class ControlPlaneEconomics:
    """FinOps and observability telemetry for enterprise-ai-production-control-plane."""
    cluster_id: str
    gpu_type: str
    gpu_cost_per_hour: float
    cost_per_million_tokens: float
    cluster_utilization_pct: float
    routed_provider: str
    incident_status: str = "HEALTHY"


@dataclass
class FlowForgeTransaction:
    """Durable enterprise workflow transaction for enterprise-ai-integration-platform."""
    transaction_id: str
    workflow_id: str
    target_system: str  # SAP, Salesforce, Oracle, Payments, Logistics
    idempotent_key: str
    payload: Dict[str, Any]
    committed: bool = False
    receipt_hash: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class PaperclipTask:
    """Hermes Paperclip Company OS autonomous task entity."""
    task_id: str
    goal: str
    max_usd_budget: float
    spent_usd: float = 0.0
    state: PaperclipTaskState = PaperclipTaskState.CREATED
    heartbeat_count: int = 0
    max_heartbeats: int = 25
    action_ledger: List[str] = field(default_factory=list)
