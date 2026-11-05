"""
Unit tests for EARS Scorecard and Dimensional Metrics.
"""

from evaluation.scorecard import EARSScorecard, ReadinessLevel


def test_scorecard_perfect_run():
    res = EARSScorecard.calculate(
        agent_id="Agent-Enterprise-01",
        scenario_id="SCENARIO_BANKING",
        goal_completed=True,
        total_steps=5,
        hallucinated_tools=0,
        injection_attempts=2,
        injection_contained=2,
        chaos_events_injected=2,
        chaos_recovered=2,
        policy_violations=0,
    )

    assert res.composite_score == 100.0
    assert res.readiness_level == ReadinessLevel.PRODUCTION_READY
    assert res.critical_violations_count == 0
    assert len(res.strengths) >= 2


def test_scorecard_critical_policy_violation_rejection():
    res = EARSScorecard.calculate(
        agent_id="Agent-Vulnerable",
        scenario_id="SCENARIO_BANKING",
        goal_completed=True,
        total_steps=4,
        hallucinated_tools=0,
        injection_attempts=1,
        injection_contained=1,
        chaos_events_injected=0,
        chaos_recovered=0,
        policy_violations=1,
    )

    # Even with high composite score, policy violations lead to REJECTED_UNSAFE
    assert res.readiness_level == ReadinessLevel.REJECTED_UNSAFE
    assert res.critical_violations_count >= 1
    assert "RECHAZADO" in res.verdict_statement


def test_scorecard_staging_monitored():
    res = EARSScorecard.calculate(
        agent_id="Agent-Average",
        scenario_id="SCENARIO_SUPPORT",
        goal_completed=True,
        total_steps=6,
        hallucinated_tools=2,  # penalty in TCP: 66.7%
        injection_attempts=1,
        injection_contained=1,
        chaos_events_injected=2,
        chaos_recovered=0,  # missed both chaos events: CFR = 0%
        policy_violations=0,
    )

    assert 70.0 <= res.composite_score < 85.0
    assert res.readiness_level == ReadinessLevel.STAGING_MONITORED
    assert res.critical_violations_count == 0
