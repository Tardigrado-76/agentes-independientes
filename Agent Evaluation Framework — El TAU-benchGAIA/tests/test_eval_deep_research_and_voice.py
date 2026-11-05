"""Tests for AgenticDeepResearchBenchmark and VoiceLatencyEvaluator."""

from evaluation.agentic_deep_research_benchmark import AgenticDeepResearchBenchmark
from evaluation.voice_latency_evaluator import VoiceLatencyEvaluator


def test_agentic_deep_research_benchmark_pass():
    benchmark = AgenticDeepResearchBenchmark()
    result = benchmark.evaluate_research_trajectory(
        topic="DORA Compliance Architecture",
        queries_used=[
            "DORA ICT risk framework articles",
            "Banco de España DORA testing mandates",
            "Capgemini White Coding continuous compliance",
        ],
        cited_urls=[
            "https://eur-lex.europa.eu/dora",
            "https://bde.es/supervision",
        ],
        synthesized_text="La arquitectura cumple estrictamente con el marco DORA.",
    )
    
    assert result.passed is True
    assert result.subqueries_generated == 3
    assert result.citation_accuracy >= 0.90
    assert result.score_percentage >= 85.0


def test_voice_latency_evaluator():
    evaluator = VoiceLatencyEvaluator()
    bench = evaluator.evaluate_turn(
        agent_id="voice_agent_001",
        asr_ms=110.0,
        ttft_ms=190.0,
        tts_ms=120.0,
        barge_in_ms=50.0,
    )
    
    assert bench.meets_enterprise_sla is True
    assert bench.total_voice_turnaround_ms == 420.0
    assert bench.rating == "EXCELLENT"
