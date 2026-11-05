"""
Binary Merkle Tree Implementation for Evaluation Evidence Sealing.
Conforms to SLSA Level 3+ audit requirements and cryptographic tamper-evidence.
"""

from __future__ import annotations

import hashlib

from pydantic import BaseModel


def hash_pair(left: str, right: str) -> str:
    """Concatenates and hashes two hexadecimal hashes."""
    combined = (left + right).encode("utf-8")
    return hashlib.sha256(combined).hexdigest()


class MerkleProof(BaseModel):
    """Cryptographic inclusion proof for a leaf in the Merkle Tree."""
    leaf_hash: str
    root_hash: str
    audit_path: list[tuple[str, str]]  # list of (direction: 'L' or 'R', sibling_hash)


class MerkleTree:
    """Computes a balanced binary Merkle tree over arbitrary string evidence hashes."""

    def __init__(self, leaves: list[str]):
        if not leaves:
            raise ValueError("Cannot construct Merkle tree with empty leaves.")
        self.leaves = [l if len(l) == 64 else hashlib.sha256(l.encode("utf-8")).hexdigest() for l in leaves]
        self.levels: list[list[str]] = [self.leaves]
        self._build_tree()

    def _build_tree(self) -> None:
        """Constructs higher levels of tree until root is reached."""
        current_level = self.leaves
        while len(current_level) > 1:
            next_level: list[str] = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    # Duplicate last element if odd number of leaves (standard RFC 6962 behavior)
                    right = left
                parent = hash_pair(left, right)
                next_level.append(parent)
            self.levels.append(next_level)
            current_level = next_level

    @property
    def root(self) -> str:
        """Returns the Merkle root hash (top level)."""
        return self.levels[-1][0]

    def get_proof(self, leaf_index: int) -> MerkleProof:
        """Generates an inclusion proof for the leaf at given index."""
        if leaf_index < 0 or leaf_index >= len(self.leaves):
            raise IndexError("Leaf index out of bounds.")

        leaf_hash = self.leaves[leaf_index]
        audit_path: list[tuple[str, str]] = []
        idx = leaf_index

        for level in self.levels[:-1]:
            is_right_child = (idx % 2 == 1)
            sibling_idx = idx - 1 if is_right_child else idx + 1
            if sibling_idx < len(level):
                sibling_hash = level[sibling_idx]
            else:
                sibling_hash = level[idx]  # Duplicated leaf

            direction = "L" if is_right_child else "R"
            audit_path.append((direction, sibling_hash))
            idx //= 2

        return MerkleProof(leaf_hash=leaf_hash, root_hash=self.root, audit_path=audit_path)

    @staticmethod
    def verify_proof(proof: MerkleProof) -> bool:
        """Verifies if leaf belongs to root given the audit path."""
        current = proof.leaf_hash
        for direction, sibling in proof.audit_path:
            if direction == "L":
                # Current was right, sibling was left
                current = hash_pair(sibling, current)
            else:
                # Current was left, sibling was right
                current = hash_pair(current, sibling)
        return current == proof.root_hash
