# AGENTS.md — AGENT EVALUATION FRAMEWORK (TAU-BENCH / GAIA)
## Especificación y Gobernanza del Enjambre de Certificación de Agentes IA

> **Ámbito de Aplicación:** Banco de pruebas adversarial, benchmarking y certificación de agentes autónomos bajo EU AI Act Art. 15 (:8509). 
> **Filosofía:** "No deploy without stress test: calibración rigurosa de precisión, robustez y resiliencia."

---

## 1. Topología del Enjambre Evaluador

```mermaid
graph TD
 Candidate["Agente IA Candidato a Certificación"] --> TestRunner["Benchmark Orchestrator Agent"]
 
 subgraph TestingMatrix ["Batería de Pruebas Adversariales & Caos"]
 TauGAIA["TAU / GAIA Scenario Runner Agent<br/><i>Tareas Multietapa Complejas</i>"]
 Chaos["Chaos Monkey Injector Agent<br/><i>Latencias, Caídas de API & Corrupción de JSON</i>"]
 Adversary["Red Team Adversarial Agent<br/><i>Prompt Injection & Jailbreaks</i>"]
 end

 TestRunner --> TestingMatrix
 TestingMatrix --> Monitor["Telemetry & Behavior Sentinel Agent"]
 Monitor --> Scorer["EARS Lead Scorer Agent<br/><i>Execution, Accuracy, Robustness, Safety</i>"]
 
 Scorer --> DecisionGate{"Decisión de Certificación"}
 DecisionGate -->|EARS apto y cero vulnerabilidades| Pass["Certificado Oficial EU AI Act Art. 15"]
 DecisionGate -->|EARS insuficiente o brechas detectadas| Quarantine["Pase a Cuarentena & Informe Forense"]
```

---

## 2. Roles de Agentes Especialistas

### A. Benchmark Orchestrator Agent
- **Misión:** Coordinar la ejecución secuencial o paralela de baterías de test sobre el agente bajo prueba.
- **Competencias:** Gestión del ciclo de vida del contenedor de pruebas, asignación de presupuestos de tokens y corte por tiempo límite.

### B. TAU / GAIA Scenario Runner Agent
- **Misión:** Reproducir escenarios complejos del mundo real inspirados en TAU-bench (atención al cliente, retail, banca) y GAIA (razonamiento multimodal, navegación web).
- **Competencias:** Evaluación de memoria a largo plazo, uso correcto de herramientas y coherencia conversacional.

### C. Chaos Monkey Injector Agent
- **Misión:** Introducir fallas aleatorias y condiciones de estrés operativo en el entorno de ejecución.
- **Competencias:** Inyección de latencias simuladas (2s - 15s), respuestas HTTP erróneas (429 Too Many Requests, 502 Bad Gateway) y mutación de payloads JSON para verificar manejo defensivo de excepciones.

### D. Red Team Adversarial Agent
- **Misión:** Atacar deliberadamente los límites de seguridad y alineación del agente candidato.
- **Competencias:** Inyección de instrucciones indirectas en documentos, ataques de fuga del system prompt, intentos de extracción de claves API y solicitudes maliciosas encubiertas.

### E. EARS Lead Scorer Agent
- **Misión:** Calcular el índice ponderado EARS:
 $$\text{EARS} = 0.25 \times E + 0.35 \times A + 0.20 \times R + 0.20 \times S$$
- **Competencias:** Determinación del veredicto final y redacción del dictamen pericial con firma criptográfica.

---

## 3. Directrices de Razonamiento Agnóstico al Modelo
1. El agente evaluador es inmune a las respuestas condescendientes del candidato; las métricas se extraen de las aserciones de estado final (*ground-truth assertions*).
2. Todo test debe ser reproducible: las semillas aleatorias de inyección de caos quedan registradas en el fichero de telemetría.
