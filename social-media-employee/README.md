# Social Media Employee (Autonomous Executive Brand Operator)
### Thought Leadership, B2B Organic Social & Audience Engagement Engineering

[![Role](https://img.shields.io/badge/Role-B2B_Organic_Social_Operator-blue.svg)]()
[![Safety](https://img.shields.io/badge/Brand_Safety-Nightly_Human_Review_Window-red.svg)]()
[![Cadence](https://img.shields.io/badge/Routines-7_Scheduled_Automations-green.svg)]()
[![Compliance](https://img.shields.io/badge/Compliance-Brand_Guidelines_%7C_No_Automated_DMs-purple.svg)]()

---

## 1. Resumen Ejecutivo (C-Level Executive Brief)

El **Social Media Employee** es un operador digital diseñado para gestionar de manera profesional y rigurosa la presencia corporativa en canales B2B (LinkedIn, Twitter/X, plataformas sectoriales).

Elimina publicaciones genéricas sin alma mediante la construcción de un **archivo de voz corporativa real (*voice profile*)** basado en lo que la empresa realmente entrega y construye. Todo contenido se deposita en disco con una **ventana de revisión nocturna** antes de su difusión.

### Matriz de Impacto para la Dirección

| Rol Directivo | Reto en Redes Corporativas | Solución Social Media Employee | Métrica de Retorno (ROI) |
|---|---|---|---|
| **Chief Executive Officer (CEO)** | Falta de tiempo para mantener presencia de liderazgo de opinión (*thought leadership*). | Extracción de aprendizajes reales de ingeniería para redactar publicaciones de alto nivel. | Posicionamiento C-Level continuo sin consumo de agenda. |
| **Chief Marketing Officer (CMO)** | Redes sociales convertidas en un escaparate plano sin interacción real. | Enfoque centrado en problemas técnicos y casos de estudio que atraen clientes B2B. | Alcance cualificado en audiencia objetivo +50%. |
| **Chief Communications Officer** | Riesgo de publicaciones desafortunadas o respuestas inapropiadas a críticas. | Ventana de cuarentena nocturna y borrador previo de respuestas a comentarios. | 100% de protección de reputación de marca. |
| **Chief People Officer (HR)** | Dificultad para atraer talento técnico cualificado sin visibilidad de proyectos. | Divulgación transparente de la cultura técnica y arquitecturas implementadas. | Reducción del coste de adquisición de talento técnico. |

---

## 2. Arquitectura de Publicación y Gestión de Marca

`
flowchart TD
    subgraph CorporateVoice ["NÚCLEO DE VOZ Y CONTEXTO"]
        SHIPPED["Registro de Entregas y Lanzamientos Reales"]
        VOICE["Perfil de Tono y Estilo Corporativo (Sin Jerga Vacía)"]
    end

    subgraph ContentCreation ["GENERACIÓN EDITORIAL"]
        TOPIC["Selección del Tema Semanal (Casos de Éxito, Arquitectura)"]
        POSTS["Redacción de Publicaciones Multi-Canal (LinkedIn / X)"]
    end

    subgraph QuarantineWindow ["VENTANA DE SEGURIDAD (NOCTURNA)"]
        DISK["Depósito de Archivos en Disco para Revisión"]
        OVERNIGHT{"¿Modificado o Cancelado por el Humano?"}
        CANCEL["Publicación Descartada"]
        APPROVE["Publicación Validada para Difusión"]
    end

    subgraph LiveInteraction ["MONITOREO DE COMENTARIOS"]
        INTERACT["Captura de Respuestas y Conversaciones"]
        REPLY["Preparación de Respuestas Técnicas Contextuales"]
    end

    SHIPPED --> TOPIC
    VOICE --> POSTS
    TOPIC --> POSTS
    POSTS --> DISK
    DISK --> OVERNIGHT
    OVERNIGHT -->|Pausado| CANCEL
    OVERNIGHT -->|Aprobado| APPROVE
    APPROVE --> INTERACT
    INTERACT --> REPLY
`

---

## 3. Rutinas Operativas

- **daily-ship-scan (Lunes a Jueves)**: Identifica novedades implementadas en el repositorio para comunicar hechos reales.
- **overnight-queue (Diario)**: Deposita en disco los borradores que se difundirán al día siguiente para permitir veto humano.
- **live-proof (Diario)**: Verifica que la publicación esté visible y sin errores de formato.
- **riday-social-retrospective (Viernes)**: Revisa qué temas generaron más conversaciones con clientes potenciales.

---

## 4. Despliegue y Gobernanza

`ash
# Repositorio privado enterprise (acceso confidencial bajo acuerdo NDA)
cd social-media-employee
# Configurar cuentas y parámetros en ROLE.md
`

Cumplimiento estricto de **Guías de Identidad de Marca** y políticas anti-automatización invasiva.
