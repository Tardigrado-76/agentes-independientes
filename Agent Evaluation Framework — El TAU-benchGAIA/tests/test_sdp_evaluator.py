"""Tests for SDP Dynamic Tool Evaluation Benchmark within TAU-benchGAIA framework."""
from __future__ import annotations

import os
import sys

_pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _pkg_root not in sys.path:
    sys.path.insert(0, _pkg_root)

_tools_root = os.path.dirname(_pkg_root)
if _tools_root not in sys.path:
    sys.path.insert(0, _tools_root)

from evaluation.sdp_evaluator import SDPEvaluationBenchmark


def test_sdp_evaluator_token_efficiency() -> None:
    bench = SDPEvaluationBenchmark()
    result = bench.evaluate_agent_tier_discovery("BankingSpecialistAgent")
    assert result["token_reduction_pct"] >= 90.0
    assert result["tier0_matches_count"] >= 1
    assert result["provenance_signature_valid"] is True
    assert result["agent_name"] == "BankingSpecialistAgent"
