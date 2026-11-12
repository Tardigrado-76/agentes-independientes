# Ad Manager Employee (Autonomous Paid Media System)
### Enterprise B2B Advertising, Creative Optimization & Zero-Overspend Governance

[![Role](https://img.shields.io/badge/Role-Paid_Media_%26_Ad_Buyer-blue.svg)]()
[![Spend Safety](https://img.shields.io/badge/Governance-Zero_Overspend_Hard_Limit-red.svg)]()
[![Cadence](https://img.shields.io/badge/Routines-7_Scheduled_Automations-green.svg)]()
[![Compliance](https://img.shields.io/badge/Compliance-EU_AI_Act_Art._14_%7C_Audit_Trail-purple.svg)]()

---

## 1. Resumen Ejecutivo (C-Level Executive Brief)

El **Ad Manager Employee** es un operador digital autónomo especializado en la gestión integral de canales de adquisición de pago (Meta Ads, Google Ads, LinkedIn Ads) diseñado para sustituir contratos de agencias de medios en tareas sistemáticas y recurrentes.

Opera bajo el principio de **Gobernanza Human-in-the-Loop (HITL)**: produce borradores, audita conversiones, califica creatividades y prepara hojas de ejecución listas para desplegar, **deteniéndose de forma estricta ante el botón de gasto (*spend ceiling*)** a menos que sea explícitamente liberado por la dirección financiera.

### Matriz de Impacto para la Dirección

| Rol Directivo | Reto Habitual en Media Buying | Solución Ad Manager Employee | Métrica de Retorno (ROI) |
|---|---|---|---|
| **Chief Marketing Officer (CMO)** | Dependencia de agencias lentas y fatiga creativa en anuncios. | Generación continua de variaciones creativas y testing de ángulos. | Reducción de fatiga publicitaria en 70%. |
| **Chief Financial Officer (CFO)** | Gasto descontrolado y discrepancia en atribución de conversiones. | Monitorización diaria de píxeles y tope de gasto por canal (*Held Mode*). | 0% desviaciones presupuestarias sobre plan. |
| **Chief Information Security Officer (CISO)** | Fuga de credenciales de tarjetas bancarias y accesos a cuentas de anuncios. | Ejecución aislada en host local sin almacenamiento de tokens bancarios. | Aislamiento completo de claves API publicitarias. |
| **Chief Compliance Officer (CCO)** | Publicidad engañosa o no conforme con regulaciones europeas. | Reglas de validación semántica previas a la propuesta de copies. | Trazabilidad documental de cada creatividad generada. |

---

## 2. Arquitectura Operativa y Flujo de Decisión

`
flowchart TD
    subgraph Scheduling ["CADENCIA Y MONITOREO"]
        CRON["Programador de Rutinas (Diario / Semanal / Mensual)"]
        TRACK["Auditor de Píxeles & Conversiones"]
    end

    subgraph AnalyticsEngine ["ANÁLISIS DE ADQUISICIÓN"]
        PERF["Análisis de CAC, ROAS y Eficiencia por Canal"]
        ANGLES["Evaluación de Ángulos y Fatiga Creativa"]
    end

    subgraph ProductionLayer ["PRODUCCIÓN DE ACTIVOS"]
        COPY["Generación de Variaciones de Copy Publicitario"]
        SHEET["Elaboración de Hoja de Despliegue (Build Sheet)"]
    end

    subgraph SafetyGate ["BARRERA DE SEGURIDAD (SPEND CEILING)"]
        CEIL{"¿Canal Liberado o Retenido (Held)?"}
        HOLD["Borrador Pendiente de Aprobación Humana"]
        DISPATCH["Ejecución Automática dentro del Límite de Gasto"]
    end

    CRON --> TRACK
    TRACK --> PERF
    PERF --> ANGLES
    ANGLES --> COPY
    COPY --> SHEET
    SHEET --> CEIL
    CEIL -->|Held / Por defecto| HOLD
    CEIL -->|Released| DISPATCH
`

---

## 3. Catálogo de Rutinas Autónomas

1. **conversion-audit (Diario)**: Verifica que las URLs de destino y los eventos de conversión sigan activos antes de permitir gasto.
2. **spend-reconciliation (Diario)**: Cruza el gasto reportado por plataforma con el balance asignado para prevenir cobros fantasma.
3. **creative-generation (Martes/Jueves)**: Produce 5 nuevos ángulos basados en las métricas de clics del ciclo anterior.
4. **weekly-rankings (Viernes)**: Clasifica los anuncios ganadores y perdedores con evidencia cuantitativa.
5. **monthly-thesis (Fin de mes)**: Redacta la tesis de inversión del canal para el comité directivo.

---

## 4. Gobernanza y Despliegue

`ash
# Repositorio privado enterprise (acceso confidencial bajo acuerdo NDA)
cd ad-manager-employee
# Configurar parámetros en work-profile.json
`

Distribuido bajo licencia enterprise. Cumplimiento conforme al **EU AI Act (Art. 14 Human Oversight)**.
