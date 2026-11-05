"""Pareto Cost-Performance Frontier Benchmark Engine.

Evaluates multi-model architectures across three dimensions:
1. EARS Score / Task Reliability (0.0 - 100.0)
2. Average Latency (ms)
3. Inference Cost ($ / 1k input & output tokens via LiteLLM cost model)

Identifies Pareto-optimal models to guide enterprise procurement decisions.
"""

from __future__ import annotations

from pydantic import BaseModel


class ModelBenchmarkPoint(BaseModel):
    model_id: str
    provider: str
    ears_score: float  # 0 to 100
    latency_p95_ms: float
    cost_per_1k_input: float
    cost_per_1k_output: float
    is_pareto_optimal: bool = False


class ParetoAnalysisReport(BaseModel):
    total_evaluated: int
    optimal_count: int
    optimal_models: list[str]
    points: list[ModelBenchmarkPoint]
    recommendation: str


class CostPerformanceFrontier:
    """Computes the Pareto efficiency frontier for agent LLM backends."""

    def __init__(self) -> None:
        # Standard benchmark catalog for frontier analysis
        self.catalog: list[ModelBenchmarkPoint] = [
            ModelBenchmarkPoint(
                model_id="gpt-4o",
                provider="OpenAI",
                ears_score=94.5,
                latency_p95_ms=850.0,
                cost_per_1k_input=0.005,
                cost_per_1k_output=0.015,
            ),
            ModelBenchmarkPoint(
                model_id="claude-3-5-sonnet",
                provider="Anthropic",
                ears_score=96.2,
                latency_p95_ms=920.0,
                cost_per_1k_input=0.003,
                cost_per_1k_output=0.015,
            ),
            ModelBenchmarkPoint(
                model_id="gemini-1.5-pro",
                provider="Google",
                ears_score=92.8,
                latency_p95_ms=640.0,
                cost_per_1k_input=0.00125,
                cost_per_1k_output=0.005,
            ),
            ModelBenchmarkPoint(
                model_id="gpt-4o-mini",
                provider="OpenAI",
                ears_score=86.4,
                latency_p95_ms=320.0,
                cost_per_1k_input=0.00015,
                cost_per_1k_output=0.0006,
            ),
            ModelBenchmarkPoint(
                model_id="deepseek-v3",
                provider="DeepSeek",
                ears_score=89.1,
                latency_p95_ms=480.0,
                cost_per_1k_input=0.00014,
                cost_per_1k_output=0.00028,
            ),
            ModelBenchmarkPoint(
                model_id="legacy-gpt-3.5-turbo",
                provider="OpenAI",
                ears_score=68.0,
                latency_p95_ms=550.0,
                cost_per_1k_input=0.0005,
                cost_per_1k_output=0.0015,
            ),
        ]

    def compute_frontier(self, points: list[ModelBenchmarkPoint] | None = None) -> ParetoAnalysisReport:
        """Finds models on the Pareto frontier (maximizing EARS score while minimizing blended cost)."""
        data = points or self.catalog

        # Calculate blended cost per 1k (assuming 3:1 input:output ratio)
        def blended_cost(pt: ModelBenchmarkPoint) -> float:
            return (pt.cost_per_1k_input * 3 + pt.cost_per_1k_output) / 4.0

        for candidate in data:
            c_cost = blended_cost(candidate)
            c_score = candidate.ears_score

            # Check if any other point strictly dominates candidate
            # Dominates means: other_cost <= c_cost AND other_score >= c_score, with at least one strict inequality
            dominated = False
            for other in data:
                if other.model_id == candidate.model_id:
                    continue
                o_cost = blended_cost(other)
                o_score = other.ears_score

                if o_cost <= c_cost and o_score >= c_score and (o_cost < c_cost or o_score > c_score):
                    dominated = True
                    break

            candidate.is_pareto_optimal = not dominated

        optimal = [p.model_id for p in data if p.is_pareto_optimal]

        rec = (
            f"Pareto Frontier identified {len(optimal)} non-dominated models: {', '.join(optimal)}. "
            f"Recommended Tier-1 for High-Stakes Financial Transactions: {optimal[0] if optimal else 'N/A'}. "
            f"Recommended Tier-2 for High-Throughput Routing: {optimal[-1] if optimal else 'N/A'}."
        )

        return ParetoAnalysisReport(
            total_evaluated=len(data),
            optimal_count=len(optimal),
            optimal_models=optimal,
            points=data,
            recommendation=rec,
        )

    def render_mermaid_chart(self, report: ParetoAnalysisReport) -> str:
        """Renders a Mermaid diagram illustrating the trade-off frontier."""
        lines = ["graph LR", "    subgraph Frontier[Pareto Efficiency Frontier]"]
        for pt in report.points:
            style = ":::optimal" if pt.is_pareto_optimal else ""
            status = " [OPTIMAL]" if pt.is_pareto_optimal else ""
            lines.append(f'        {pt.model_id.replace("-", "_")}["{pt.model_id}{status}<br/>EARS: {pt.ears_score}% | Latency: {pt.latency_p95_ms}ms"]{style}')
        lines.append("    end")
        lines.append("    classDef optimal fill:#00d26a,stroke:#008b44,stroke-width:2px,color:#000;")
        return "\n".join(lines)
