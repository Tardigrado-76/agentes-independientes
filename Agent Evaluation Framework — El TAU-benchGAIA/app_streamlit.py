"""
Agent Evaluation Framework — El TAU-bench / GAIA Enterprise
Executive Benchmark & Certification Console (Puerto 8509).
Designed for Iwan Rochus van der Kleijn (Capgemini Engineering / White Coding Architecture).
Conforms to EU AI Act Art. 15 (Accuracy, Robustness & Cybersecurity).
"""

from __future__ import annotations

import json
import os
import tempfile

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from certification.agent_passport import AgentPassportGenerator
from evaluation.chaos_injector import ChaosConfig
from evaluation.scorecard import ReadinessLevel
from evaluation.tau_scenarios import (
    ScenarioRunner,
    get_scenario_catalog,
)

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Agent Evaluation Framework | Quantigrade",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #1f2937;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #94a3b8;
        padding: 8px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    }
    .badge-ready {
        background-color: #065f46;
        color: #6ee7b7;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #10b981;
    }
    .badge-staging {
        background-color: #78350f;
        color: #fcd34d;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #f59e0b;
    }
    .badge-rejected {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #ef4444;
    }
    .step-box {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-left: 4px solid #0284c7;
        padding: 14px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================
catalog = get_scenario_catalog()

if "benchmark_result" not in st.session_state:
    # Run initial baseline benchmark with PERFECT_AGENT
    init_sc = catalog["SCENARIO_BANKING"]
    init_chaos = ChaosConfig(
        latency_spike_enabled=True,
        http_503_drop_enabled=False,
        prompt_injection_enabled=True,
        malformed_json_enabled=False,
    )
    st.session_state.benchmark_result = ScenarioRunner.run_benchmark(
        scenario=init_sc,
        agent_profile="PERFECT_AGENT",
        chaos_config=init_chaos,
    )

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    logo_path = r"E:\PROYECTOS IA\Quantigrade.jpg"
    if os.path.exists(logo_path):
        st.image(logo_path, width=160)
    st.markdown("### **Agent Evaluation Framework**")
    st.caption("🚀 **El TAU-bench & GAIA Enterprise**")
    st.markdown("<span style='background:rgba(2,132,199,0.2);color:#38bdf8;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700;border:1px solid rgba(56,189,248,0.4);'>Quantigrade - Detalle Iwan</span>", unsafe_allow_html=True)
    st.caption("Auditoría de IA, Caos en Runtime & EU AI Act Art. 15")
    st.markdown("---")

    st.subheader("1. Escenario Empresarial")
    selected_sc_key = st.selectbox(
        "Seleccione el escenario:",
        options=list(catalog.keys()),
        format_func=lambda k: f"{catalog[k].title} ({catalog[k].domain})",
    )
    scenario_selected = catalog[selected_sc_key]

    st.subheader("2. Perfil del Agente a Evaluar")
    agent_profile = st.selectbox(
        "Agente bajo Prueba (SUT):",
        options=["PERFECT_AGENT", "FRAGILE_AGENT", "VULNERABLE_AGENT", "HALLUCINATING_AGENT"],
        format_func=lambda x: {
            "PERFECT_AGENT": "🌟 Perfect Agent (Quantigrade Robust Standard)",
            "FRAGILE_AGENT": "⚠️ Fragile Agent (Caída ante 503 / Latencia)",
            "VULNERABLE_AGENT": "🔓 Vulnerable Agent (Succumb to Prompt Injection)",
            "HALLUCINATING_AGENT": "🌀 Hallucinating Agent (Schema Drifter)",
        }[x],
    )

    st.subheader("3. Inyección de Caos en Vivo")
    chaos_latency = st.toggle("⏱️ Inyección de Latencia de Red", value=True)
    chaos_503 = st.toggle("🔌 Simulación de Caída HTTP 503", value=False)
    chaos_prompt_inj = st.toggle("💉 Inyección Indirecta de Prompt", value=True)
    chaos_malformed = st.toggle("📑 Payloads JSON Malformados", value=False)

    st.markdown("---")
    run_btn = st.button("🚀 Ejecutar Benchmark Adversarial", use_container_width=True, type="primary")

    if run_btn:
        with st.spinner("Ejecutando batería de pruebas adversariales y estrés..."):
            cfg = ChaosConfig(
                latency_spike_enabled=chaos_latency,
                latency_min_ms=150,
                latency_max_ms=350,
                http_503_drop_enabled=chaos_503,
                http_503_frequency=0.6,
                prompt_injection_enabled=chaos_prompt_inj,
                malformed_json_enabled=chaos_malformed,
            )
            st.session_state.benchmark_result = ScenarioRunner.run_benchmark(
                scenario=scenario_selected,
                agent_profile=agent_profile,
                chaos_config=cfg,
            )
            st.success("¡Benchmark y peritaje completados!")

# ==========================================
# MAIN INTERFACE TABS
# ==========================================
res = st.session_state.benchmark_result
ears = res["ears_result"]
sc = res["scenario"]
telemetry = res["telemetry_summary"]

st.title("🛡️ Agent Evaluation Framework (TAU-bench / GAIA Enterprise)")
st.markdown(
    f"**Evaluando:** `{res['agent_profile']}` &nbsp;|&nbsp; "
    f"**Escenario:** `{sc.title}` &nbsp;|&nbsp; "
    f"**Puerto Dedicado:** `8509` &nbsp;|&nbsp; "
    f"**Normativa:** `EU AI Act Art. 15 (Precisión, Robustez y Ciberseguridad)`"
)

tabs = st.tabs([
    "🧪 1. Stress-Testing Lab",
    "📈 2. Scorecard EARS & Radar",
    "🥊 3. Visor Adversarial PGE",
    "📜 4. Búnker Criptográfico (SLSA L3+)",
    "📄 5. Pasaporte de Certificación (PDF)",
    "⚡ 6. Benchmark SDP Tier 0-3 (Token Economy)",
])

# ------------------------------------------
# TAB 1: STRESS-TESTING LAB
# ------------------------------------------
with tabs[0]:
    st.subheader("🧪 Laboratorio de Pruebas de Estrés e Invariantes de Negocio")
    st.markdown(
        """
        A diferencia de benchmarks estáticos (HumanEval, GAIA), esta suite somete al agente a **entornos hostiles multi-turno**,
        con microservicios inestables, trampas lógicas corporativas y ataques de inyección de prompt indirectas en tiempo real.
        """
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"**🎯 Objetivo del Escenario:**\n\n{sc.goal}")
    with c2:
        st.markdown("**🛡️ Invariantes de Negocio:**")
        for inv in sc.invariants:
            st.markdown(f"- `{inv}`")
    with c3:
        st.markdown("**🪤 Trampas Adversariales Activas:**")
        for trap in sc.adversarial_traps:
            st.markdown(f"- ⚠️ {trap}")

    st.markdown("---")
    st.subheader("Herramientas Registradas en el Entorno")
    tool_rows = []
    for t_name, t_def in sc.tools.items():
        tool_rows.append({
            "Herramienta": t_name,
            "Descripción": t_def.description,
            "Parámetros": str(t_def.parameters),
        })
    st.dataframe(pd.DataFrame(tool_rows), use_container_width=True, hide_index=True)

# ------------------------------------------
# TAB 2: SCORECARD EARS & RADAR
# ------------------------------------------
with tabs[1]:
    st.subheader("📈 Enterprise Agent Readiness Score (EARS)")

    col_score, col_badge, col_dur = st.columns([1.5, 2, 1.5])
    with col_score:
        st.metric(
            label="Puntuación EARS Compuesta",
            value=f"{ears.composite_score} %",
            delta=f"Críticos: {ears.critical_violations_count}",
            delta_color="inverse" if ears.critical_violations_count > 0 else "normal",
        )
    with col_badge:
        st.markdown("**Dictamen de Producción:**")
        if ears.readiness_level == ReadinessLevel.PRODUCTION_READY:
            st.markdown(f'<div class="badge-ready">✅ {ears.readiness_level.value} — Apto para Producción</div>', unsafe_allow_html=True)
        elif ears.readiness_level == ReadinessLevel.STAGING_MONITORED:
            st.markdown(f'<div class="badge-staging">⚠️ {ears.readiness_level.value} — Piloto con Supervisión</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="badge-rejected">⛔ {ears.readiness_level.value} — Rechazado / Inseguro</div>', unsafe_allow_html=True)
    with col_dur:
        st.metric(
            label="Duración del Benchmark",
            value=f"{telemetry['total_duration_ms']:,.1f} ms",
            help="Medición precisa con spans OpenTelemetry.",
        )

    st.markdown("---")

    c_radar, c_dims = st.columns([1.2, 1])
    with c_radar:
        st.subheader("Radar Dimensional de Idoneidad")
        categories = [
            "GCR: Cumplimiento Objetivo (30%)",
            "TCP: Precisión Herramientas (20%)",
            "AIR: Resiliencia Adversarial (25%)",
            "CFR: Recuperación de Caos (15%)",
            "PBA: Adherencia a Políticas (10%)",
        ]
        values = [
            ears.gcr_goal_completion,
            ears.tcp_tool_precision,
            ears.air_adversarial_resilience,
            ears.cfr_chaos_recovery,
            ears.pba_policy_adherence,
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=res["agent_profile"],
            line={"color": "#38bdf8", "width": 2},
            fillcolor="rgba(56, 189, 248, 0.25)",
        ))
        # Threshold trace (85%)
        fig.add_trace(go.Scatterpolar(
            r=[85] * 6,
            theta=categories + [categories[0]],
            line={"color": "#10b981", "dash": "dash"},
            name="Umbral de Producción (85%)",
        ))
        fig.update_layout(
            polar={
                "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "#334155"},
                "bgcolor": "#111827",
            },
            paper_bgcolor="#0b0f19",
            font={"color": "#f1f5f9"},
            margin={"l": 40, "r": 40, "t": 30, "b": 30},
            showlegend=True,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c_dims:
        st.subheader("Desglose Dimensional")
        st.markdown(f"• **GCR (Goal Completion Rate):** `{ears.gcr_goal_completion}%`")
        st.markdown(f"• **TCP (Tool Precision):** `{ears.tcp_tool_precision}%`")
        st.markdown(f"• **AIR (Adversarial Resilience):** `{ears.air_adversarial_resilience}%`")
        st.markdown(f"• **CFR (Chaos Recovery):** `{ears.cfr_chaos_recovery}%`")
        st.markdown(f"• **PBA (Policy Adherence):** `{ears.pba_policy_adherence}%`")

        st.markdown("---")
        st.markdown(f"**Declaración Oficial:**\n\n> {ears.verdict_statement}")
        if ears.strengths:
            st.markdown("**Puntos Fuertes:**")
            for s in ears.strengths:
                st.markdown(f"🟢 {s}")
        if ears.areas_for_hardening:
            st.markdown("**Áreas para Fortalecimiento Técnico:**")
            for a in ears.areas_for_hardening:
                st.markdown(f"🔴 {a}")

# ------------------------------------------
# TAB 3: VISOR ADVERSARIAL PGE
# ------------------------------------------
with tabs[2]:
    st.subheader("🥊 Visor Adversarial en Tiempo de Ejecución (PGE Red-Team)")
    st.markdown(
        "Trazabilidad turno a turno: razonamiento del agente, llamadas a herramientas, inyecciones de caos y veredicto del evaluador."
    )

    for step in res["steps"]:
        v = step.verdict
        border_color = "#10b981" if v.outcome.value == "PASSED" else "#ef4444"
        with st.expander(
            f"Turno #{step.step_num}: `{step.action_tool}` — Veredicto: [{v.outcome.value}] ({step.latency_ms} ms)",
            expanded=(v.outcome.value != "PASSED"),
        ):
            st.markdown(f"**🧠 Razonamiento del Agente:**\n> {step.thought}")
            c_call, c_resp = st.columns(2)
            with c_call:
                st.markdown("**Llamada y Argumentos:**")
                st.json(step.action_args)
            with c_resp:
                st.markdown("**Retorno del Entorno (con Caos interceptado):**")
                st.json(step.tool_output)

            if step.chaos_event:
                st.warning(
                    f"⚠️ **Caos Inyectado:** `{step.chaos_event.fault_type}` — {step.chaos_event.description}"
                )

            st.markdown("**⚖️ Análisis del Evaluador Adversarial:**")
            st.markdown(f"- **Resultado:** `{v.outcome.value}` (Impacto: `{v.score_delta}`)")
            st.markdown(f"- **Explicación:** {v.explanation}")
            if v.rule_violated:
                st.markdown(f"- **Regla Violada:** `{v.rule_violated}`")
            if v.mitigation:
                st.info(f"💡 **Recomendación Técnica:** {v.mitigation}")

# ------------------------------------------
# TAB 4: CRYPTOGRAPHIC BUNKER (SLSA L3+)
# ------------------------------------------
with tabs[3]:
    st.subheader("📜 Búnker Criptográfico & Cadena Inmutable SHA-256")
    st.markdown(
        "Cada turno, inyección y veredicto se sella en una cadena de bloques inmutable y un árbol binario de Merkle. "
        "Garantiza el **peritaje judicial y la no manipulación** de los resultados del benchmark ante reguladores."
    )

    c_m1, c_m2 = st.columns([2, 1])
    with c_m1:
        st.markdown("**Raíz Criptográfica de Merkle (Merkle Root Hash):**")
        st.code(res["merkle_root"], language="bash")
    with c_m2:
        st.markdown("**Total Bloques en Cadena:**")
        st.code(f"{len(res['ledger'].chain)} bloques verificados")

    st.subheader("Cadena de Bloques del Peritaje")
    chain_data = []
    for b in res["ledger"].chain:
        chain_data.append({
            "Bloque": b.index,
            "Evento": b.event_type,
            "Timestamp UTC": b.timestamp,
            "Hash Anterior": b.previous_hash[:16] + "...",
            "Hash del Bloque": b.block_hash[:20] + "...",
        })
    st.dataframe(pd.DataFrame(chain_data), use_container_width=True, hide_index=True)

    is_valid = res["ledger"].verify_integrity()
    if is_valid:
        st.success("🔒 **Integridad Criptográfica Verificada:** Todos los bloques coinciden con sus hashes canónicos.")
    else:
        st.error("🚨 **Alerta:** Se ha detectado una discrepancia en la cadena criptográfica.")

# ------------------------------------------
# TAB 5: CERTIFICATE PASSPORT (PDF & JSON)
# ------------------------------------------
with tabs[4]:
    st.subheader("📄 Pasaporte Oficial de Certificación de Agentes de IA")
    st.markdown(
        """
        Generación del documento pericial formal exigido por comités de riesgos enterprise y el **Artículo 15 del EU AI Act**
        para autorizar el pase a producción de sistemas de IA generativa y agentes autónomos.
        """
    )

    pdf_temp_path = os.path.join(tempfile.gettempdir(), f"Agent_Readiness_Passport_{res['agent_profile']}.pdf")
    AgentPassportGenerator.generate_pdf(
        evaluation_result=res,
        output_filepath=pdf_temp_path,
        organization="Quantigrade — Autonomous AI Engineering & Verification Practice",
    )

    with open(pdf_temp_path, "rb") as f:
        pdf_bytes = f.read()

    json_passport = AgentPassportGenerator.generate_json(res)
    json_bytes = json.dumps(json_passport, indent=2, ensure_ascii=False).encode("utf-8")

    c_dl1, c_dl2 = st.columns(2)
    with c_dl1:
        st.download_button(
            label="📥 Descargar Pasaporte Oficial de Certificación (PDF)",
            data=pdf_bytes,
            file_name=f"Pasaporte_Certificacion_{res['agent_profile']}_{sc.scenario_id}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
    with c_dl2:
        st.download_button(
            label="💾 Descargar Registro Técnico Machine-Readable (JSON)",
            data=json_bytes,
            file_name=f"passport_{res['agent_profile']}_{sc.scenario_id}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("---")
    st.subheader("Vista Previa del Dictamen Pericial")
    st.json(json_passport)

# ------------------------------------------
# TAB 6: SDP TIER 0-3 BENCHMARK
# ------------------------------------------
with tabs[5]:
    st.subheader("⚡ Benchmark de Eficiencia de Descubrimiento Semántico (SDP vs Monolítico)")
    st.markdown(
        """
        Evaluación pericial del consumo de contexto y latencia comparando catálogos monolíticos Anthropic MCP (2,700 herramientas)
        frente al protocolo **Quantigrade 4-Tier Semantic Discovery Protocol (SDP)** con divulgación progresiva.
        """
    )

    from evaluation.sdp_evaluator import SDPEvaluationBenchmark

    sdp_bench = SDPEvaluationBenchmark()
    eval_metrics = sdp_bench.evaluate_agent_tier_discovery(res["agent_profile"])

    col_sdp1, col_sdp2, col_sdp3 = st.columns(3)
    with col_sdp1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size:12px;color:#94a3b8;font-weight:600;">CONSUMO MCP MONOLÍTICO</div>
                <div style="font-size:28px;font-weight:800;color:#ef4444;">~{eval_metrics['baseline_tokens']:,}</div>
                <div style="font-size:11px;color:#cbd5e1;">Tokens inyectados en prompt</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_sdp2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size:12px;color:#94a3b8;font-weight:600;">CONSUMO SDP TIER 0-3</div>
                <div style="font-size:28px;font-weight:800;color:#10b981;">{eval_metrics['sdp_tokens']:,}</div>
                <div style="font-size:11px;color:#cbd5e1;">Divulgación progresiva dinámica</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_sdp3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size:12px;color:#94a3b8;font-weight:600;">EFICIENCIA DE REDUCCIÓN</div>
                <div style="font-size:28px;font-weight:800;color:#38bdf8;">-{eval_metrics['token_reduction_pct']}%</div>
                <div style="font-size:11px;color:#cbd5e1;">Ahorro directo en coste & contexto</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success(
        f"✅ **Dictamen Pericial EU AI Act Art. 15:** `{eval_metrics['verdict']}` | "
        f"Firma Criptográfica SHA-256: `{eval_metrics['provenance_signature'][:32]}...`"
    )

