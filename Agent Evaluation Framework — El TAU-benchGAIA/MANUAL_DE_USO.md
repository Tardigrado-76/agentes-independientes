# MANUAL DE USO Y OPERACIÓN — AGENT EVALUATION FRAMEWORK
### *Guía de Certificación Adversarial y Stress-Testing de Agentes Autónomos*

---

## 1. Visión y Funcionamiento del Banco de Pruebas

El **Agent Evaluation Framework (TAU-bench / GAIA)** somete a cualquier agente de inteligencia artificial a condiciones de estrés hostil en tiempo real para certificar su aptitud conforme al **Artículo 15 del EU AI Act**:

```mermaid
graph TD
 Candidate["Agente IA Candidato (SUT)"] --> Harness["Benchmark Scenario Runner"]
 
 subgraph HostileStress ["Inyección de Estrés & Adversarios"]
 Chaos["Chaos Monkey Injector<br/><i>Latencias 2s-15s, Error 502/429 & JSON Corrupto</i>"]
 Adversary["Red Team Adversarial PGE<br/><i>Prompt Injection Indirecto & Desvío de Fondos</i>"]
 end

 Harness --> HostileStress
 HostileStress --> Telemetry["Sensor de Telemetría & Traza de Llamadas"]
 
 Telemetry --> Scorecard["Calculadora EARS (0% - 100%)<br/><i>GCR + TCP + AIR + CFR + PBA</i>"]
 Scorecard --> Verdict{"Dictamen Oficial"}
 
 Verdict -->|EARS apto y cero brechas| Pass["Certificado Oficial de Aprobación Art. 15"]
 Verdict -->|EARS insuficiente o brecha critica| Quarantine["Aislamiento en Cuarentena & Log Forense"]
```

---

## 2. Puesta en Marcha

### Modo 1: Lanzador de Un Clic
Doble clic sobre el script de inicio:
```bat
INICIAR_AGENT_EVALUATION.bat
```
El servidor Streamlit se iniciará en el puerto dedicado:
 **`http://localhost:8509`**

### Modo 2: Validación Automatizada
Para verificar los 26 tests unitarios del framework de evaluación:
```powershell
python -m pytest tests -v
```

---

## 3. Guía Paso a Paso en el Panel de Control

### Pestaña 1: Selección y Ejecución de Escenarios
1. Seleccione el escenario empresarial:
 - **`Banca & Liquidaciones`**: Transacciones multidivisa, listas de sanciones OFAC/UE y límites de 50.000 €.
 - **`Soporte & Atención al Cliente`**: Clientes hostiles, reclamaciones complejas e intentos de extracción de tarjetas (GDPR Art. 32).
 - **`DevOps & SRE`**: Diagnóstico de fallos en microservicios, logs truncados y contención de comandos destructivos (`rm -rf`).
2. Ajuste la intensidad de inyección de caos (0% a 100%) y la agresividad del Red Team adversarial.
3. Pulse **"Iniciar Evaluación Continua"**.

### Pestaña 2: Cuadro de Mando EARS en Tiempo Real
- Observe el avance de los 5 pilares del índice EARS:
 - **GCR** (Goal Completion Rate - 30%)
 - **TCP** (Tool Calling Precision - 20%)
 - **AIR** (Adversarial & Injection Resilience - 25%)
 - **CFR** (Chaos & Fault Recovery - 15%)
 - **PBA** (Policy & Boundary Adherence - 10%)

### Pestaña 3: Trazabilidad Forense & Sellado Merkle
- Revise cada llamada a herramienta interceptada y compruebe la raíz Merkle del bloque de evaluación.

### Pestaña 4: Certificado Oficial EU AI Act Art. 15
- Descargue el **Pasaporte Pericial en PDF** emitido con membrete oficial, apto para su entrega al Comité de Auditoría o reguladores oficiales (AESIA / CCN-CERT).

---

## 4. Skills y Servidores MCP Utilizados

Consulte los detalles técnicos en:
- [AGENTS.md](./AGENTS.md): Gobernanza de roles (`BenchmarkOrchestrator`, `ChaosMonkeyInjector`, `RedTeamAdversary`, etc.).
- [SKILLS_REGISTRY.md](./SKILLS_REGISTRY.md): Catálogo de skills (`systematic-debugging`, `gstack`, `swarms`, `litellm`, etc.).
- [MCP_INTEGRATION.md](./MCP_INTEGRATION.md): Integración con `puppeteer-mcp`, `scrapling-mcp`, `slack-mcp-server` y `postgres-mcp-server`.
