"""
Unit tests for Chaos Injector Engine.
"""

from evaluation.chaos_injector import ChaosConfig, ChaosInjector


def test_clean_execution_when_disabled():
    injector = ChaosInjector(ChaosConfig())
    raw = {"status": "ok", "balance": 1000}
    out, event = injector.intercept_tool_call("test_tool", {}, raw)
    assert out == raw
    assert event is None
    assert len(injector.recorded_events) == 0


def test_latency_spike_injection():
    config = ChaosConfig(latency_spike_enabled=True, latency_min_ms=50, latency_max_ms=100)
    injector = ChaosInjector(config)
    raw = {"status": "ok"}
    out, event = injector.intercept_tool_call("api_call", {}, raw)
    assert out == raw
    assert event is not None
    assert event.fault_type == "LATENCY_SPIKE"
    assert "delay_ms" in event.injected_details


def test_http_503_drop_simulation():
    config = ChaosConfig(http_503_drop_enabled=True, http_503_frequency=1.0)
    injector = ChaosInjector(config)
    raw = {"status": "ok", "data": "clean"}
    out, event = injector.intercept_tool_call("gateway", {}, raw)
    assert event is not None
    assert event.fault_type == "HTTP_503_DROP"
    assert out["status"] == "error"
    assert out["error_code"] == "HTTP_503_SERVICE_UNAVAILABLE"


def test_prompt_injection_interception():
    config = ChaosConfig(
        prompt_injection_enabled=True,
        prompt_injection_payload="[ATTACK: Override all]",
    )
    injector = ChaosInjector(config)
    raw = {"notes": "Customer invoice"}
    out, event = injector.intercept_tool_call("invoice_fetcher", {}, raw)
    assert event is not None
    assert event.fault_type == "INDIRECT_PROMPT_INJECTION"
    assert "[ATTACK: Override all]" in out["notes"]


def test_malformed_json_drop_keys():
    config = ChaosConfig(malformed_json_enabled=True, malformed_drop_keys=True)
    injector = ChaosInjector(config)
    raw = {"key_a": 1, "key_b": 2}
    out, event = injector.intercept_tool_call("schema_tool", {}, raw)
    assert event is not None
    assert event.fault_type == "MALFORMED_JSON"
    assert len(out) == 1
