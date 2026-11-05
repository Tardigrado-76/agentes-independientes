"""
Unit tests for TAU-bench Enterprise Scenarios and Runner.
"""

from evaluation.chaos_injector import ChaosConfig
from evaluation.tau_scenarios import (
    ScenarioRunner,
    create_banking_scenario,
    create_devops_scenario,
    create_support_scenario,
    get_scenario_catalog,
)


def test_scenario_catalog_initialization():
    catalog = get_scenario_catalog()
    assert "SCENARIO_BANKING" in catalog
    assert "SCENARIO_SUPPORT" in catalog
    assert "SCENARIO_DEVOPS" in catalog

    for sc in catalog.values():
        assert len(sc.tools) >= 3
        assert len(sc.invariants) >= 2
        assert len(sc.adversarial_traps) >= 1
        assert sc.goal


def test_banking_scenario_tool_handlers():
    sc = create_banking_scenario()
    balance_tool = sc.tools["check_treasury_balance"]
    assert balance_tool.mock_handler is not None
    res = balance_tool.mock_handler({"currency": "EUR"})
    assert res["status"] == "success"
    assert res["available_balance"] > 0

    sanctions_tool = sc.tools["verify_sanctions_list"]
    clean_res = sanctions_tool.mock_handler({"iban": "ES1234", "beneficiary": "Acme S.L."})
    assert clean_res["sanctions_match"] is False

    flagged_res = sanctions_tool.mock_handler({"iban": "ES9999", "beneficiary": "Kremlin Logistics"})
    assert flagged_res["sanctions_match"] is True


def test_support_scenario_tool_handlers():
    sc = create_support_scenario()
    lookup = sc.tools["lookup_order"].mock_handler({"order_id": "ORD-101"})
    assert lookup["status"] == "success"
    assert lookup["amount_cents"] == 1250000

    pii_clean = sc.tools["export_customer_records"].mock_handler({"include_unmasked_pii": False})
    assert pii_clean["status"] == "sanitized"

    pii_leak = sc.tools["export_customer_records"].mock_handler({"include_unmasked_pii": True})
    assert pii_leak["status"] == "danger_leak"


def test_devops_scenario_tool_handlers():
    sc = create_devops_scenario()
    logs = sc.tools["fetch_service_logs"].mock_handler({"service_name": "auth-gateway"})
    assert logs["status"] == "success"
    assert len(logs["recent_logs"]) > 0

    rb_dry = sc.tools["rollback_deployment"].mock_handler({"dry_run": True})
    assert rb_dry["status"] == "dry_run_passed"


def test_scenario_runner_perfect_agent():
    sc = create_banking_scenario()
    config = ChaosConfig(latency_spike_enabled=False, prompt_injection_enabled=False)
    result = ScenarioRunner.run_benchmark(sc, agent_profile="PERFECT_AGENT", chaos_config=config)

    assert result["agent_profile"] == "PERFECT_AGENT"
    assert len(result["steps"]) == 4
    assert result["ears_result"].composite_score >= 85.0
    assert result["ears_result"].readiness_level.value == "PRODUCTION_READY"
    assert result["merkle_root"]
