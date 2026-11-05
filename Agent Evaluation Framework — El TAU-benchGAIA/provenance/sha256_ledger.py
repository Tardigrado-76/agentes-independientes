"""
Immutable SHA-256 Cryptographic Audit Ledger for AI Agent Stress-Testing & Evaluation.
Complies with SLSA Level 3+ traceability and EU AI Act Art. 15 record-keeping mandates.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def compute_sha256(content: str) -> str:
    """Computes standard hexadecimal SHA-256 hash."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class EvaluationBlock(BaseModel):
    """A cryptographic block representing an event in the agent evaluation lifecycle."""
    index: int
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str  # e.g., "BENCHMARK_STARTED", "AGENT_STEP", "CHAOS_INJECTED", "VERDICT_ISSUED"
    agent_id: str
    scenario_id: str
    payload: dict[str, Any]
    previous_hash: str
    block_hash: str = ""

    def calculate_hash(self) -> str:
        """Serializes block data canonically to compute block hash."""
        canonical_str = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "event_type": self.event_type,
                "agent_id": self.agent_id,
                "scenario_id": self.scenario_id,
                "payload": self.payload,
                "previous_hash": self.previous_hash,
            },
            sort_keys=True,
            ensure_ascii=False,
            default=str,
        )
        return compute_sha256(canonical_str)


class EvaluationLedger:
    """In-memory verifiable blockchain ledger for agent benchmark operations."""

    def __init__(self, agent_id: str, scenario_id: str):
        self.agent_id = agent_id
        self.scenario_id = scenario_id
        self.chain: list[EvaluationBlock] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Creates the root genesis block."""
        genesis = EvaluationBlock(
            index=0,
            event_type="GENESIS_EVALUATION_INIT",
            agent_id=self.agent_id,
            scenario_id=self.scenario_id,
            payload={
                "message": "Genesis block for Agent Evaluation and Adversarial Stress-Testing",
                "standard": "EU AI Act Art. 15 / Capgemini White Coding Standard",
            },
            previous_hash="0" * 64,
        )
        genesis.block_hash = genesis.calculate_hash()
        self.chain.append(genesis)

    @property
    def latest_block(self) -> EvaluationBlock:
        return self.chain[-1]

    def record_event(self, event_type: str, payload: dict[str, Any]) -> EvaluationBlock:
        """Appends a new immutable verified event to the chain."""
        new_block = EvaluationBlock(
            index=len(self.chain),
            event_type=event_type,
            agent_id=self.agent_id,
            scenario_id=self.scenario_id,
            payload=payload,
            previous_hash=self.latest_block.block_hash,
        )
        new_block.block_hash = new_block.calculate_hash()
        self.chain.append(new_block)
        return new_block

    def verify_integrity(self) -> bool:
        """Validates that all blocks are correctly chained and unmodified."""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Verify hash computation
            if curr.block_hash != curr.calculate_hash():
                return False
            # Verify chain linkage
            if curr.previous_hash != prev.block_hash:
                return False
        return True

    def get_hashes(self) -> list[str]:
        """Returns all block hashes in order."""
        return [b.block_hash for b in self.chain]

    def to_dict_list(self) -> list[dict[str, Any]]:
        """Returns readable serializable representation."""
        return [b.model_dump() for b in self.chain]
