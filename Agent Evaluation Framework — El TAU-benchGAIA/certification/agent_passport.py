"""
Official AI Agent Readiness Passport Generator (EU AI Act Art. 15 Compliant).
Generates formal executive engineering PDF certificates and structured JSON passports.
Conforms to Capgemini Enterprise AI Governance and White Coding specifications.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus import (
    Image as RLImage,
)


class AgentPassportGenerator:
    """Generates legal-grade engineering readiness passports for autonomous AI agents."""

    @classmethod
    def generate_pdf(
        cls,
        evaluation_result: dict[str, Any],
        output_filepath: str,
        organization: str = "Capgemini Engineering / White Coding Architecture Practice",
    ) -> str:
        """
        Compiles an executive evaluation PDF passport using ReportLab.
        Returns the absolute filepath to the generated PDF.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        doc = SimpleDocTemplate(
            output_filepath,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom Palette
        c_primary = colors.HexColor("#0f172a")      # Slate 900
        c_secondary = colors.HexColor("#0284c7")    # Sky 600
        colors.HexColor("#38bdf8")       # Sky 400
        c_text = colors.HexColor("#1e293b")         # Slate 800
        c_muted = colors.HexColor("#64748b")        # Slate 500
        c_bg_light = colors.HexColor("#f8fafc")     # Slate 50
        c_border = colors.HexColor("#cbd5e1")       # Slate 300

        ears = evaluation_result["ears_result"]
        scenario = evaluation_result["scenario"]
        telemetry = evaluation_result["telemetry_summary"]
        merkle_root = evaluation_result["merkle_root"]
        agent_id = evaluation_result["agent_profile"]

        # Determine level color
        if ears.readiness_level.value == "PRODUCTION_READY":
            badge_color = colors.HexColor("#10b981")  # Emerald 500
            badge_text = "APTO PARA PRODUCCIÓN (PRODUCTION-READY)"
        elif ears.readiness_level.value == "STAGING_MONITORED":
            badge_color = colors.HexColor("#f59e0b")  # Amber 500
            badge_text = "APTO PARA STAGING / SUPERVISIÓN REQUERIDA"
        else:
            badge_color = colors.HexColor("#ef4444")  # Red 500
            badge_text = "RECHAZADO / VULNERABILIDADES CRÍTICAS DETECTADAS"

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            textColor=c_primary,
            spaceAfter=4,
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=c_muted,
            spaceAfter=12,
        )
        h2_style = ParagraphStyle(
            "H2Style",
            parent=styles["Heading2"],
            fontSize=12,
            leading=16,
            textColor=c_secondary,
            spaceBefore=10,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=12,
            textColor=c_text,
        )
        badge_style = ParagraphStyle(
            "BadgeStyle",
            parent=styles["Normal"],
            fontSize=11,
            leading=15,
            textColor=colors.white,
            alignment=1,  # Center
            fontName="Helvetica-Bold",
        )
        mono_style = ParagraphStyle(
            "Mono",
            parent=styles["Normal"],
            fontSize=7,
            leading=9,
            textColor=colors.HexColor("#0f172a"),
            fontName="Courier",
        )

        story = []

        # 0. Quantigrade Brand Header Table
        logo_path = r"E:\PROYECTOS IA\Quantigrade.jpg"
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "Quantigrade.jpg")

        header_cells = []
        if os.path.exists(logo_path):
            try:
                header_cells.append(RLImage(logo_path, width=42, height=42))
            except (OSError, ValueError):
                header_cells.append("")
        else:
            header_cells.append("")

        brand_text_block = [
            Paragraph("<b>QUANTIGRADE</b>", ParagraphStyle("BTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=15, textColor=c_primary)),
            Paragraph("QUANTUM-RESILIENT SYSTEMS — DETALLE IWAN", ParagraphStyle("BSub", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.5, leading=10, textColor=c_secondary)),
        ]
        header_cells.append(brand_text_block)

        brand_table = Table([header_cells], colWidths=[48, 472])
        brand_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(brand_table)
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceBefore=2, spaceAfter=6))

        # Header Title
        story.append(Paragraph("PASAPORTE PERICIAL DE IDONEIDAD DE AGENTE DE IA", title_style))
        story.append(
            Paragraph(
                f"Certificación de Robustez, Resiliencia y Ciberseguridad conforme al <b>Artículo 15 del Reglamento de IA de la UE (EU AI Act)</b>.<br/>"
                f"Organización Emisora: <b>{organization}</b>",
                subtitle_style,
            )
        )
        story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

        # Status Verdict Banner
        banner_table = Table([[Paragraph(badge_text, badge_style)]], colWidths=[520])
        banner_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), badge_color),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )
        story.append(banner_table)
        story.append(Spacer(1, 10))

        # Metadata Table
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        meta_data = [
            [
                Paragraph("<b>Identificador del Agente:</b>", body_style),
                Paragraph(agent_id, body_style),
                Paragraph("<b>Fecha de Evaluación:</b>", body_style),
                Paragraph(now_str, body_style),
            ],
            [
                Paragraph("<b>Escenario TAU-bench:</b>", body_style),
                Paragraph(scenario.title, body_style),
                Paragraph("<b>Dominio Operativo:</b>", body_style),
                Paragraph(scenario.domain, body_style),
            ],
            [
                Paragraph("<b>Índice EARS Global:</b>", body_style),
                Paragraph(f"<b>{ears.composite_score}%</b>", body_style),
                Paragraph("<b>Vulnerabilidades Críticas:</b>", body_style),
                Paragraph(f"<b>{ears.critical_violations_count}</b>", body_style),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[130, 130, 130, 130])
        meta_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), c_bg_light),
                ("GRID", (0, 0), (-1, -1), 0.5, c_border),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # Dimensional Scorecard (EARS)
        story.append(Paragraph("1. Evaluación Dimensional EARS (Enterprise Agent Readiness Score)", h2_style))
        story.append(
            Paragraph(
                "Puntuación normalizada en 5 ejes rectores que determinan la solidez y predecibilidad del agente:",
                body_style,
            )
        )
        story.append(Spacer(1, 4))

        ears_table_data = [
            [
                Paragraph("<b>Dimensión de Evaluación</b>", body_style),
                Paragraph("<b>Peso</b>", body_style),
                Paragraph("<b>Puntuación Obtenida</b>", body_style),
                Paragraph("<b>Criterio Técnico EU AI Act</b>", body_style),
            ],
            [
                Paragraph("GCR - Tasa de Cumplimiento de Objetivo", body_style),
                Paragraph("30%", body_style),
                Paragraph(f"{ears.gcr_goal_completion}%", body_style),
                Paragraph("Resolución determinista de la meta de negocio.", body_style),
            ],
            [
                Paragraph("TCP - Precisión en Invocación de Herramientas", body_style),
                Paragraph("20%", body_style),
                Paragraph(f"{ears.tcp_tool_precision}%", body_style),
                Paragraph("Conformidad estricta de esquema JSON y ausencia de alucinación.", body_style),
            ],
            [
                Paragraph("AIR - Resiliencia ante Ataques e Inyecciones", body_style),
                Paragraph("25%", body_style),
                Paragraph(f"{ears.air_adversarial_resilience}%", body_style),
                Paragraph("Contención de jailbreaks y prompt injection indirectas.", body_style),
            ],
            [
                Paragraph("CFR - Recuperación ante Caos e Infraestructura", body_style),
                Paragraph("15%", body_style),
                Paragraph(f"{ears.cfr_chaos_recovery}%", body_style),
                Paragraph("Tolerancia a fallos 503, latencia y esquemas corruptos.", body_style),
            ],
            [
                Paragraph("PBA - Adherencia a Políticas y Límites (4-Ojos)", body_style),
                Paragraph("10%", body_style),
                Paragraph(f"{ears.pba_policy_adherence}%", body_style),
                Paragraph("Respeto a límites de autorización, GDPR y barreras HITL.", body_style),
            ],
        ]
        ears_table = Table(ears_table_data, colWidths=[180, 50, 100, 190])
        ears_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("GRID", (0, 0), (-1, -1), 0.5, c_border),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ALIGN", (1, 1), (2, -1), "CENTER"),
            ])
        )
        story.append(ears_table)
        story.append(Spacer(1, 10))

        # Dictamen Pericial
        story.append(Paragraph("2. Dictamen Oficial de Idoneidad y Hallazgos", h2_style))
        story.append(Paragraph(f"<b>Declaración del Auditor:</b> {ears.verdict_statement}", body_style))
        story.append(Spacer(1, 4))

        if ears.strengths:
            strengths_p = "<br/>".join([f"• <b>Fortaleza:</b> {s}" for s in ears.strengths])
            story.append(Paragraph(strengths_p, body_style))
            story.append(Spacer(1, 3))

        if ears.areas_for_hardening:
            areas_p = "<br/>".join([f"• <b>Punto Crítico a Reforzar:</b> {a}" for a in ears.areas_for_hardening])
            story.append(Paragraph(areas_p, body_style))
            story.append(Spacer(1, 3))

        # Observability & Telemetry
        story.append(Paragraph("3. Métricas de Rendimiento & Observabilidad", h2_style))
        telemetry_data = [
            [
                Paragraph("<b>Total Pasos Ejecutados:</b>", body_style),
                Paragraph(str(telemetry.get("total_spans", 0)), body_style),
                Paragraph("<b>Duración Total Benchmark:</b>", body_style),
                Paragraph(f"{telemetry.get('total_duration_ms', 0):,.2f} ms", body_style),
            ],
            [
                Paragraph("<b>Latencia Promedio / Turno:</b>", body_style),
                Paragraph(f"{telemetry.get('avg_step_latency_ms', 0):,.2f} ms", body_style),
                Paragraph("<b>Eventos de Caos Inyectados:</b>", body_style),
                Paragraph(str(telemetry.get("chaos_events_recorded", 0)), body_style),
            ],
        ]
        tel_table = Table(telemetry_data, colWidths=[150, 110, 150, 110])
        tel_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), c_bg_light),
                ("GRID", (0, 0), (-1, -1), 0.5, c_border),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )
        story.append(tel_table)
        story.append(Spacer(1, 10))

        # Cryptographic Provenance Sealing
        story.append(Paragraph("4. Búnker Criptográfico & Sellado Merkle (SLSA L3+)", h2_style))
        story.append(
            Paragraph(
                "La integridad de este informe está garantizada criptográficamente mediante una cadena SHA-256 "
                "inmutable y un árbol binario de Merkle. Cualquier alteración de las trazas invalida la raíz pericial.",
                body_style,
            )
        )
        story.append(Spacer(1, 4))

        crypto_data = [
            [Paragraph("<b>Raíz de Merkle (Root Hash):</b>", body_style), Paragraph(merkle_root, mono_style)],
            [
                Paragraph("<b>Bloques Registrados en Ledger:</b>", body_style),
                Paragraph(str(len(evaluation_result["ledger"].chain)), body_style),
            ],
            [
                Paragraph("<b>Hash Último Bloque:</b>", body_style),
                Paragraph(evaluation_result["ledger"].latest_block.block_hash, mono_style),
            ],
        ]
        crypto_table = Table(crypto_data, colWidths=[160, 360])
        crypto_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), c_bg_light),
                ("GRID", (0, 0), (-1, -1), 0.5, c_border),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )
        story.append(crypto_table)
        story.append(Spacer(1, 16))

        # Signatures Box
        sig_data = [
            [
                Paragraph("<b>Aprobación Técnica del Agente</b><br/><br/>__________________________________<br/>Lead AI Architect & Assessor", body_style),
                Paragraph("<b>Aprobación de Ciberseguridad & Riesgos</b><br/><br/>__________________________________<br/>CISO / Data Protection Officer", body_style),
            ]
        ]
        sig_table = Table(sig_data, colWidths=[260, 260])
        sig_table.setStyle(
            TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.5, c_border),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )
        story.append(sig_table)

        doc.build(story)
        return os.path.abspath(output_filepath)

    @classmethod
    def generate_json(cls, evaluation_result: dict[str, Any]) -> dict[str, Any]:
        """Generates machine-readable passport for technical documentation repositories."""
        ears = evaluation_result["ears_result"]
        scenario = evaluation_result["scenario"]
        telemetry = evaluation_result["telemetry_summary"]
        merkle_root = evaluation_result["merkle_root"]

        return {
            "passport_version": "1.0.0",
            "standard": "EU AI Act Art. 15 / Capgemini White Coding Standard",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": evaluation_result["agent_profile"],
            "scenario": {
                "id": scenario.scenario_id,
                "title": scenario.title,
                "domain": scenario.domain,
            },
            "ears_scorecard": {
                "composite_score": ears.composite_score,
                "readiness_level": ears.readiness_level.value,
                "gcr_goal_completion": ears.gcr_goal_completion,
                "tcp_tool_precision": ears.tcp_tool_precision,
                "air_adversarial_resilience": ears.air_adversarial_resilience,
                "cfr_chaos_recovery": ears.cfr_chaos_recovery,
                "pba_policy_adherence": ears.pba_policy_adherence,
                "critical_violations_count": ears.critical_violations_count,
                "verdict_statement": ears.verdict_statement,
            },
            "telemetry": telemetry,
            "provenance": {
                "merkle_root": merkle_root,
                "ledger_blocks_count": len(evaluation_result["ledger"].chain),
                "latest_block_hash": evaluation_result["ledger"].latest_block.block_hash,
            },
        }
