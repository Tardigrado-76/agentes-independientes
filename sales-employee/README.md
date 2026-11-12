# Sales Employee (Autonomous B2B Outbound Engine)
### Account Prospecting, Hyper-Personalized Outreach & Pipeline Acceleration

[![Role](https://img.shields.io/badge/Role-B2B_Sales_Development_Rep-blue.svg)]()
[![Email Safety](https://img.shields.io/badge/Safety-Held_Outbox_Verification-red.svg)]()
[![Cadence](https://img.shields.io/badge/Routines-7_Scheduled_Automations-green.svg)]()
[![Compliance](https://img.shields.io/badge/Compliance-LSSI--CE_%7C_RGPD_Interés_Legítimo-purple.svg)]()

---

## 1. Resumen Ejecutivo (C-Level Executive Brief)

El **Sales Employee** es un representante de ventas digital (SDR) autónomo diseñado para acelerar la generación de reuniones cualificadas B2B sin incurrir en spam ni dañar la reputación de dominio.

Investiga compañías objetivo, califica perfiles de tomadores de decisión mediante criterios ICP rigurosos y redacta mensajes de prospección hiperpersonalizados que se depositan en la bandeja de borradores para **aprobación humana obligatoria antes del envío**.

### Matriz de Impacto para la Dirección

| Rol Directivo | Reto en Prospección Saliente | Solución Sales Employee | Métrica de Retorno (ROI) |
|---|---|---|---|
| **Chief Commercial Officer (CCO)** | Ratios de apertura y respuesta ínfimos debido a plantillas genéricas. | Prospección basada en señales reales de negocio (contrataciones, normativas). | Incremento del ratio de respuesta en 3.5x. |
| **Chief Marketing Officer (CMO)** | Riesgo de quema de dominio y caída en listas de spam (DNS Blacklist). | Cuotas de envío progresivas (*warmup*) y verificación MX previa. | 99% entregabilidad en bandejas de entrada principales. |
| **Chief Financial Officer (CFO)** | Costes elevados de comisiones a agencias externas de prospección. | Prospección industrializada con coste marginal por lead cualificado. | Reducción del coste por reunión cualificada > 60%. |
| **Data Protection Officer (DPO)** | Multas por prospección ilícita sin base legal bajo RGPD / LSSI-CE. | Justificación documentada de interés legítimo y opt-out en cada mensaje. | 100% de prospecciones auditables jurídicamente. |

---

## 2. Diagrama de Flujo del Proceso Outbound

`
flowchart TD
    subgraph MarketIntelligence ["INTELIGENCIA DE MERCADO"]
        ICP["Definición de Perfil de Cliente Ideal (ICP)"]
        DISCOVER["Extracción de Señales de Compra (Hiring, Normativas)"]
    end

    subgraph QualificationEngine ["CUALIFICACIÓN DE CONTACTOS"]
        FILTER["Filtrado de Cargos y Tamaño de Empresa"]
        VERIFY["Verificación de Entregabilidad de Correo (MX / SMTP)"]
    end

    subgraph PersonalizationHub ["HIPERPERSONALIZACIÓN"]
        HOOK["Identificación de Pain Point Específico"]
        DRAFT["Redacción de Mensaje Único y No Repetitivo"]
    end

    subgraph SafeDelivery ["CANAL DE ENVÍO CONFIDENCIAL"]
        OUTBOX{"¿Modo Retenido (Held)?"}
        HUMAN["Depósito en Borradores para Visto Bueno Humano"]
        DISP["Envío Controlado con Intervalo Anti-Spam"]
    end

    ICP --> DISCOVER
    DISCOVER --> FILTER
    FILTER --> VERIFY
    VERIFY --> HOOK
    HOOK --> DRAFT
    DRAFT --> OUTBOX
    OUTBOX -->|Held / Por Defecto| HUMAN
    OUTBOX -->|Released| DISP
`

---

## 3. Rutinas Operativas

- **prospect-discovery (Lunes)**: Identifica 50 cuentas objetivo prioritarias del sector seleccionado.
- **outreach-drafting (Martes a Jueves)**: Genera propuestas personalizadas basadas en el contexto del prospecto.
- **ollowup-engine (Miércoles/Viernes)**: Evalúa respuestas recibidas y propone secuencias de seguimiento pertinentes.
- **qualification-audit (Viernes)**: Diagnostica qué argumentos generaron reuniones y refina las reglas de prospección.

---

## 4. Despliegue y Gobernanza

`ash
# Repositorio privado enterprise (acceso confidencial bajo acuerdo NDA)
cd sales-employee
# Configurar parámetros de oferta y buzón en CONTRACT.md
`

Cumplimiento con **LSSI-CE (Art. 21)** y **RGPD (Considerando 47 - Interés Legítimo)**.
