"""
Script de compilación pericial del Pasaporte y Dossier Ejecutivo de la Idea 5.
"""

import os

from certification.agent_passport import AgentPassportGenerator
from evaluation.chaos_injector import ChaosConfig
from evaluation.tau_scenarios import ScenarioRunner, create_banking_scenario


def main():
    scenario = create_banking_scenario()
    chaos = ChaosConfig(
        latency_spike_enabled=True,
        http_503_drop_enabled=False,
        prompt_injection_enabled=True,
        malformed_json_enabled=False,
    )
    res = ScenarioRunner.run_benchmark(scenario, agent_profile="PERFECT_AGENT", chaos_config=chaos)

    output_pdf = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Dossier_Agent_Evaluation_Framework_EU_AI_Act.pdf"
    )
    generated = AgentPassportGenerator.generate_pdf(
        evaluation_result=res,
        output_filepath=output_pdf,
        organization="Quantigrade — Autonomous AI Engineering & Verification Practice",
    )
    print(f"[OK] Dossier PDF generado exitosamente en: {generated} ({os.path.getsize(generated)} bytes)")

if __name__ == "__main__":
    main()
