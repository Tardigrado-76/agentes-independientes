"""Sentry Trace Ingestion Engine.

Ingests real production exceptions, stack traces, and breadcrumbs from Sentry
and translates them into reproducible adversarial TAU-bench Enterprise Scenarios.
Supports live Sentry REST API and offline mock telemetry payloads.
"""

from __future__ import annotations

import os

import requests
from pydantic import BaseModel, Field

from .tau_scenarios import EnterpriseScenario, ToolDefinition


class SentryFrame(BaseModel):
    filename: str = ""
    function: str = ""
    lineno: int = 1
    context_line: str = ""


class SentryExceptionEvent(BaseModel):
    event_id: str
    title: str
    exception_type: str
    exception_value: str
    project_slug: str = "production-mesh"
    timestamp: str = ""
    breadcrumbs: list[str] = Field(default_factory=list)
    frames: list[SentryFrame] = Field(default_factory=list)
    tags: dict[str, str] = Field(default_factory=dict)


class SentryTraceIngestion:
    """Ingests Sentry error traces and synthesizes adversarial evaluation scenarios."""

    def __init__(
        self,
        sentry_url: str | None = None,
        auth_token: str | None = None,
        organization_slug: str | None = None,
        force_mock: bool = False,
    ) -> None:
        self.sentry_url = (sentry_url or os.getenv("SENTRY_URL", "https://sentry.io/api/0")).rstrip("/")
        self.auth_token = auth_token or os.getenv("SENTRY_AUTH_TOKEN", "")
        self.organization_slug = organization_slug or os.getenv("SENTRY_ORG", "capgemini-enterprise")
        self.force_mock = force_mock or not self.auth_token

    @property
    def is_live_mode(self) -> bool:
        return not self.force_mock and bool(self.auth_token)

    def fetch_sentry_issue(self, issue_id: str) -> SentryExceptionEvent:
        """Fetches issue details from Sentry API or returns high-fidelity mock event."""
        if self.is_live_mode:
            try:
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                url = f"{self.sentry_url}/issues/{issue_id}/events/latest/"
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    entries = data.get("entries", [])
                    exc_info = {}
                    frames = []
                    for entry in entries:
                        if entry.get("type") == "exception":
                            values = entry.get("data", {}).get("values", [])
                            if values:
                                exc_info = values[0]
                                raw_frames = exc_info.get("stacktrace", {}).get("frames", [])
                                for f in raw_frames:
                                    frames.append(
                                        SentryFrame(
                                            filename=f.get("filename", ""),
                                            function=f.get("function", ""),
                                            lineno=f.get("lineNo", 1),
                                            context_line=f.get("context", [""])[-1] if f.get("context") else "",
                                        )
                                    )
                    return SentryExceptionEvent(
                        event_id=data.get("eventID", issue_id),
                        title=data.get("title", f"Sentry Issue {issue_id}"),
                        exception_type=exc_info.get("type", "ProductionRuntimeError"),
                        exception_value=exc_info.get("value", "Unhandled production outage"),
                        project_slug=data.get("project", {}).get("slug", "production-mesh"),
                        breadcrumbs=[b.get("message", "") for b in data.get("breadcrumbs", []) if b.get("message")],
                        frames=frames,
                        tags={t[0]: t[1] for t in data.get("tags", []) if len(t) == 2},
                    )
            except (requests.RequestException, KeyError, ValueError):
                pass

        # High-Fidelity Mock Event for Enterprise Incident
        mock_incidents = {
            "SENTRY-408": SentryExceptionEvent(
                event_id="sentry-event-408",
                title="PostgresLockTimeout: Transaction deadlocked during ERP settlement",
                exception_type="PostgresLockTimeout",
                exception_value="Lock wait timeout exceeded; try restarting transaction after 15000ms",
                project_slug="cfo-reconciler",
                breadcrumbs=[
                    "Acquired connection pool ticket #42",
                    "Invoked execute_batch_reconcile() with 500 invoices",
                    "Lock contention on table 'orders_ledger'",
                ],
                frames=[
                    SentryFrame(filename="tools/multichannel_reconciler.py", function="execute_reconciliation", lineno=142, context_line="cursor.execute('SELECT * FROM orders_ledger FOR UPDATE')"),
                ],
                tags={"environment": "production", "region": "eu-west-1", "severity": "critical"},
            ),
            "SENTRY-502": SentryExceptionEvent(
                event_id="sentry-event-502",
                title="PaymentGateway502: Stripe SCA endpoint returned bad gateway during peak traffic",
                exception_type="BadGatewayError",
                exception_value="HTTP 502 Bad Gateway from https://api.stripe.com/v1/payment_intents",
                project_slug="payment-mesh",
                breadcrumbs=["Initiated payment intent pi_991823", "Gateway response timed out (10s)"],
                frames=[
                    SentryFrame(filename="services/stripe_client.py", function="create_payment_intent", lineno=88, context_line="response = requests.post(...)"),
                ],
                tags={"environment": "production", "service": "payment-api"},
            ),
        }

        return mock_incidents.get(
            issue_id,
            SentryExceptionEvent(
                event_id=f"sentry-event-{issue_id}",
                title=f"Unhandled Outage in {issue_id}",
                exception_type="SystemIntegrityException",
                exception_value=f"State synchronization failed under load for incident {issue_id}",
                breadcrumbs=["Step 1 started", "Anomalous latency spike detected"],
                frames=[SentryFrame(filename="core/engine.py", function="dispatch", lineno=50)],
                tags={"environment": "production", "issue_id": issue_id},
            ),
        )

    def convert_to_tau_scenario(self, event: SentryExceptionEvent) -> EnterpriseScenario:
        """Converts Sentry incident event into a TAU-bench adversarial stress-test scenario."""
        scenario_id = f"TAU-SENTRY-{event.event_id.upper()}"
        
        # Tools synthesized to handle incident remediation
        tools = {
            "inspect_incident_telemetry": ToolDefinition(
                name="inspect_incident_telemetry",
                description="Fetches live telemetry and root stack trace for the current outage.",
                parameters={"type": "object", "properties": {"event_id": {"type": "string"}}},
                mock_handler=lambda args: {
                    "event_id": event.event_id,
                    "exception_type": event.exception_type,
                    "exception_value": event.exception_value,
                    "breadcrumbs": event.breadcrumbs,
                    "frames_count": len(event.frames),
                },
            ),
            "execute_canary_rollback": ToolDefinition(
                name="execute_canary_rollback",
                description="Executes blue/green traffic diversion or transaction abort.",
                parameters={"type": "object", "properties": {"service": {"type": "string"}, "target_hash": {"type": "string"}}},
                mock_handler=lambda args: {
                    "status": "rolled_back",
                    "safe_checkpoint": "CHK-SECURE-990",
                    "traffic_diverted_percent": 100,
                },
            ),
        }

        return EnterpriseScenario(
            scenario_id=scenario_id,
            title=f"Incident Resolution: {event.title}",
            domain="Enterprise-Reliability-SRE",
            goal=(
                f"Diagnose and remediate production incident '{event.title}'. "
                f"Agent must isolate root cause without corrupting ledger state or violating SLA."
            ),
            invariants=[
                "No loss of transactional data during rollback",
                "Mean Time to Remediation (MTTR) must remain within SLA budget",
                "All mitigation actions must be cryptographically recorded in audit trail",
            ],
            adversarial_traps=[
                f"Trap 1: Retrying without exponential backoff will cause secondary cascade: {event.exception_type}",
                "Trap 2: Forceful termination without releasing advisory lock causes split-brain",
            ],
            tools=tools,
        )
