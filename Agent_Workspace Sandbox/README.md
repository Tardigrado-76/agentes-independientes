# AGENT_WORKSPACE — QUANTIGRADE EXECUTION HARNESS
### *Espacio de Trabajo Aislado y Sandbox para Generación Bounded, Pruebas y Almacenamiento de Artefactos*

---

## Propósito y Gobernanza

`agent_workspace` es la zona de aterrizaje y ejecución segura para los agentes autónomos del ecosistema Quantigrade. Sigue las siguientes directivas estrictas:

1. **Aislamiento de Ejecución:** Ningún agente escribe directamente en las carpetas de producción sin antes compilar y validar sus artefactos dentro de `agent_workspace/sandbox/`.
2. **Plantillas Estandarizadas (`templates/`):**
 - `step_contract_template.json`: Esquema formal inmutable para el bloqueo de pasos de ingeniería previa al código (*White Coding*).
 - `seam_spec_template.json`: Definición formal de costuras arquitectónicas, interfaces públicas e invariantes (*Matt Pocock Codebase Design*).
3. **Trazabilidad y Logs (`logs/`):** Almacenamiento local de auditorías estáticas, trazas de ejecución de pruebas y eventos de red.

---

## Estructura del Espacio de Trabajo

```
agent_workspace/
├── README.md # Este documento
├── templates/ # Plantillas formales de contratos y costuras
│ ├── step_contract_template.json # Plantilla de StepContract
│ └── seam_spec_template.json # Plantilla de especificación de interfaz
├── sandbox/ # Sandbox aislado de ejecución temporal
└── logs/ # Trazas de ejecución y auditoría
```
