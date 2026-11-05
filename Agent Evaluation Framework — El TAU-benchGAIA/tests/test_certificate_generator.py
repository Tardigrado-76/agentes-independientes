"""
Unit tests for Official AI Agent Readiness Passport Generator (PDF & JSON).
"""

import os

import pytest
from certification.agent_passport import AgentPassportGenerator
from evaluation.chaos_injector import ChaosConfig
from evaluation.tau_scenarios import ScenarioRunner, create_banking_scenario


@pytest.fixture
def sample_evaluation_result():
    sc = create_banking_scenario()
    config = ChaosConfig()
    return ScenarioRunner.run_benchmark(sc, agent_profile="PERFECT_AGENT", chaos_config=config)


def test_passport_json_generation(sample_evaluation_result):
    json_data = AgentPassportGenerator.generate_json(sample_evaluation_result)
    assert json_data["standard"] == "EU AI Act Art. 15 / Capgemini White Coding Standard"
    assert "ears_scorecard" in json_data
    assert "composite_score" in json_data["ears_scorecard"]
    assert "provenance" in json_data
    assert json_data["provenance"]["merkle_root"]


def test_passport_pdf_generation(sample_evaluation_result, tmp_path):
    pdf_path = str(tmp_path / "test_agent_passport.pdf")
    generated_path = AgentPassportGenerator.generate_pdf(
        evaluation_result=sample_evaluation_result,
        output_filepath=pdf_path,
        organization="Capgemini Test Lab",
    )

    assert os.path.exists(generated_path)
    file_size = os.path.getsize(generated_path)
    assert file_size > 1000  # Valid non-empty ReportLab compiled PDF
