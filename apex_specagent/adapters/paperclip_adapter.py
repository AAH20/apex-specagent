"""Apex_SpecAgent: Hermes Paperclip Company OS Adapter.

Integrates with @paperclipai/hermes-paperclip-adapter for enterprise governance.
Enforces real-time USD budget ceilings across primary and speculative agent branches,
manages discrete heartbeat lifecycles, and emits immutable SHA-256 ActionLedger receipts.
"""

import time
import hashlib
from typing import Dict, Any, List, Optional
from apex_specagent.core.primitives import (
    PaperclipTask,
    PaperclipTaskState,
)


class HermesPaperclipAdapter:
    """Manages Company OS multi-heartbeat lifecycles and USD financial accounting."""

    # Frontier pricing calibration ($3.00/M prompt, $15.00/M completion)
    PRICE_PER_PROMPT_TOKEN = 3.0 / 1_000_000.0
    PRICE_PER_COMPLETION_TOKEN = 15.0 / 1_000_000.0

    def __init__(self):
        self.tasks: Dict[str, PaperclipTask] = {}

    def create_task(
        self,
        task_id: str,
        goal: str,
        max_usd_budget: float = 0.05,
        max_heartbeats: int = 25,
    ) -> PaperclipTask:
        """Initialize a new Company OS governed autonomous task."""
        task = PaperclipTask(
            task_id=task_id,
            goal=goal,
            max_usd_budget=max_usd_budget,
            max_heartbeats=max_heartbeats,
            state=PaperclipTaskState.CREATED,
        )
        self.tasks[task_id] = task
        return task

    def start_heartbeat(self, task_id: str) -> PaperclipTask:
        """Start a new execution heartbeat cycle."""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        if task.state == PaperclipTaskState.BUDGET_EXCEEDED:
            raise PermissionError(f"Task {task_id} cannot proceed: budget exceeded")

        task.heartbeat_count += 1
        if task.heartbeat_count > task.max_heartbeats:
            task.state = PaperclipTaskState.MAX_HEARTBEATS
            raise TimeoutError(f"Task {task_id} exceeded maximum allowed heartbeats")

        task.state = PaperclipTaskState.RUNNING
        return task

    def record_token_burn(
        self,
        task_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        is_speculative: bool = False,
    ) -> Dict[str, Any]:
        """Record token consumption and enforce real-time USD budget constraints."""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        cost = (prompt_tokens * self.PRICE_PER_PROMPT_TOKEN) + (
            completion_tokens * self.PRICE_PER_COMPLETION_TOKEN
        )

        task.spent_usd += cost

        if task.spent_usd > task.max_usd_budget:
            task.state = PaperclipTaskState.BUDGET_EXCEEDED

        return {
            "task_id": task_id,
            "cost_usd": round(cost, 6),
            "total_spent_usd": round(task.spent_usd, 6),
            "remaining_budget_usd": round(max(0.0, task.max_usd_budget - task.spent_usd), 6),
            "state": task.state.value,
            "is_speculative": is_speculative,
        }

    def emit_action_receipt(
        self, task_id: str, action_type: str, details: Dict[str, Any]
    ) -> str:
        """Emit an immutable cryptographic SHA-256 ActionLedger receipt."""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        raw = f"{task_id}:{action_type}:{sorted(str(details.items()))}:{time.time()}"
        receipt = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        task.action_ledger.append(receipt)
        return receipt

    def complete_task(self, task_id: str) -> PaperclipTask:
        """Mark Company OS task as successfully completed."""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        if task.state != PaperclipTaskState.BUDGET_EXCEEDED:
            task.state = PaperclipTaskState.COMPLETED
        return task
