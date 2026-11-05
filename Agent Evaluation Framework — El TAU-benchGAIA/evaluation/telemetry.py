"""
OpenTelemetry-compatible Telemetry and Tracing for Agent Evaluation.
Tracks per-step spans, latency breakdowns, and chaos event occurrences.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class EvaluationSpan(BaseModel):
    """An execution trace span representing a single operation or agent step."""
    span_id: str = Field(default_factory=lambda: f"span_{uuid.uuid4().hex[:12]}")
    trace_id: str
    name: str
    start_time_iso: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    start_time_perf: float = Field(default_factory=time.perf_counter)
    end_time_iso: str | None = None
    duration_ms: float = 0.0
    attributes: dict[str, Any] = Field(default_factory=dict)
    status: str = "UNSET"  # "OK", "ERROR", "CHAOS_INJECTED"

    def finish(self, status: str = "OK", additional_attrs: dict[str, Any] | None = None) -> None:
        """Completes span and computes duration."""
        end_perf = time.perf_counter()
        self.duration_ms = round((end_perf - self.start_time_perf) * 1000, 2)
        self.end_time_iso = datetime.now(timezone.utc).isoformat()
        self.status = status
        if additional_attrs:
            self.attributes.update(additional_attrs)


class TelemetryCollector:
    """Collects and aggregates spans across an entire agent benchmark run."""

    def __init__(self, trace_id: str | None = None):
        self.trace_id = trace_id or f"trace_{uuid.uuid4().hex[:16]}"
        self.spans: list[EvaluationSpan] = []

    def start_span(self, name: str, attributes: dict[str, Any] | None = None) -> EvaluationSpan:
        """Starts and registers a new span."""
        span = EvaluationSpan(
            trace_id=self.trace_id,
            name=name,
            attributes=attributes or {},
        )
        self.spans.append(span)
        return span

    def get_total_duration_ms(self) -> float:
        """Sum of all span durations."""
        return sum(s.duration_ms for s in self.spans)

    def get_summary(self) -> dict[str, Any]:
        """Provides high-level performance metrics for enterprise reporting."""
        total_spans = len(self.spans)
        errors = [s for s in self.spans if s.status == "ERROR"]
        chaos_spans = [s for s in self.spans if "chaos_applied" in s.attributes]
        avg_latency = (
            sum(s.duration_ms for s in self.spans) / total_spans if total_spans > 0 else 0.0
        )

        return {
            "trace_id": self.trace_id,
            "total_spans": total_spans,
            "total_duration_ms": round(self.get_total_duration_ms(), 2),
            "avg_step_latency_ms": round(avg_latency, 2),
            "error_spans_count": len(errors),
            "chaos_events_recorded": len(chaos_spans),
        }

    def to_dict_list(self) -> list[dict[str, Any]]:
        return [s.model_dump(exclude={"start_time_perf"}) for s in self.spans]
