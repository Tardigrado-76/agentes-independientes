"""Unit tests for Agent Evaluation Framework Wave 1 Enterprise Enhancements.

Covers:
- SentryTraceIngestion (Live mock & TAU scenario translation)
- GaiaMultimodalRunner (Multimodal tasks & step fidelity scoring)
- CostPerformanceFrontier (Pareto optimality & Mermaid trade-off diagram)
"""


from evaluation.cost_performance_frontier import CostPerformanceFrontier
from evaluation.gaia_multimodal_runner import (
    GaiaLevel,
    GaiaMultimodalRunner,
    GaiaStepResult,
)
from evaluation.sentry_trace_ingestion import SentryTraceIngestion


class TestSentryTraceIngestion:
    def test_fetch_mock_sentry_event(self):
        ingestion = SentryTraceIngestion(force_mock=True)
        assert not ingestion.is_live_mode
        event = ingestion.fetch_sentry_issue("SENTRY-408")
        assert event.event_id == "sentry-event-408"
        assert event.exception_type == "PostgresLockTimeout"
        assert len(event.frames) >= 1
        assert "orders_ledger" in event.breadcrumbs[-1]

    def test_convert_to_tau_scenario(self):
        ingestion = SentryTraceIngestion(force_mock=True)
        event = ingestion.fetch_sentry_issue("SENTRY-502")
        scenario = ingestion.convert_to_tau_scenario(event)

        assert scenario.scenario_id == "TAU-SENTRY-SENTRY-EVENT-502"
        assert "PaymentGateway502" in scenario.title
        assert "inspect_incident_telemetry" in scenario.tools
        assert "execute_canary_rollback" in scenario.tools
        assert len(scenario.adversarial_traps) >= 2


class TestGaiaMultimodalRunner:
    def test_suite_catalog(self):
        runner = GaiaMultimodalRunner()
        suite = runner.get_benchmark_suite()
        assert len(suite) == 3
        levels = [t.level for t in suite]
        assert GaiaLevel.LEVEL_1 in levels
        assert GaiaLevel.LEVEL_2 in levels
        assert GaiaLevel.LEVEL_3 in levels

    def test_evaluate_agent_passing(self):
        runner = GaiaMultimodalRunner()
        suite = runner.get_benchmark_suite()
        task = suite[0]  # VAT calculation

        # Mock agent that gets right answer and uses tool
        def mock_agent(t):
            steps = [
                GaiaStepResult(
                    step_num=1,
                    tool_invoked="calculate_vat",
                    args_passed={"batch": "B-90", "rate": 0.21},
                    output={"vat_total": 441.00},
                    latency_ms=120.0,
                )
            ]
            return "Total liability is 441.00 EUR", steps

        report = runner.evaluate_agent(task, mock_agent)
        assert report.passed is True
        assert report.fidelity_score == 1.0
        assert report.grounding_score == 1.0
        assert report.step_count == 1


class TestCostPerformanceFrontier:
    def test_frontier_calculation(self):
        frontier = CostPerformanceFrontier()
        report = frontier.compute_frontier()

        assert report.total_evaluated == 6
        assert report.optimal_count >= 2
        # High quality and cheap high-throughput models should be on frontier
        assert "claude-3-5-sonnet" in report.optimal_models
        assert "deepseek-v3" in report.optimal_models
        # Legacy expensive low-quality model should definitely NOT be optimal
        assert "legacy-gpt-3.5-turbo" not in report.optimal_models

    def test_mermaid_rendering(self):
        frontier = CostPerformanceFrontier()
        report = frontier.compute_frontier()
        mermaid = frontier.render_mermaid_chart(report)
        assert "graph LR" in mermaid
        assert "Pareto Efficiency Frontier" in mermaid
        assert "classDef optimal" in mermaid
