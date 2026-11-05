"""
Unit tests for Cryptographic Ledger and Merkle Sealer.
"""

from provenance.merkle_sealer import MerkleTree
from provenance.sha256_ledger import EvaluationLedger


def test_ledger_genesis_and_chaining():
    ledger = EvaluationLedger(agent_id="Agent-007", scenario_id="SCENARIO_BANKING")
    assert len(ledger.chain) == 1
    assert ledger.chain[0].event_type == "GENESIS_EVALUATION_INIT"

    b1 = ledger.record_event("TEST_EVENT", {"param": 123})
    assert len(ledger.chain) == 2
    assert b1.previous_hash == ledger.chain[0].block_hash
    assert ledger.verify_integrity() is True


def test_ledger_tampering_detection():
    ledger = EvaluationLedger(agent_id="Agent-007", scenario_id="SCENARIO_BANKING")
    ledger.record_event("EVENT_A", {"data": "authentic"})
    ledger.record_event("EVENT_B", {"data": "authentic"})

    assert ledger.verify_integrity() is True

    # Tamper with block payload
    ledger.chain[1].payload["data"] = "tampered"
    assert ledger.verify_integrity() is False


def test_merkle_tree_construction_and_proof():
    leaves = [
        "hash_alpha",
        "hash_beta",
        "hash_gamma",
        "hash_delta",
    ]
    tree = MerkleTree(leaves)
    assert tree.root is not None
    assert len(tree.root) == 64

    # Verify inclusion proof for leaf 2 ("hash_gamma")
    proof = tree.get_proof(2)
    assert proof.root_hash == tree.root
    assert MerkleTree.verify_proof(proof) is True

    # Check invalid proof fails
    proof.root_hash = "f" * 64
    assert MerkleTree.verify_proof(proof) is False


def test_merkle_tree_odd_number_of_leaves():
    leaves = ["leaf1", "leaf2", "leaf3"]
    tree = MerkleTree(leaves)
    assert tree.root is not None
    proof = tree.get_proof(1)
    assert MerkleTree.verify_proof(proof) is True
