# Sesión 10 — Contenido de diapositivas (para alumnos)
## Cierre · Puerta de Calidad de Release

> **19 slides** · 2 horas · A 1–7 (40) · B 8–9b–14 (40) · C 15–18 (20)
> Guion en `GUIA_INSTRUCTOR.md`. Sin dinámicas de chat.

---

### Slide 1 — Portada (2 min)
**Título:** La puerta que construyeron
- Sesión 10 de 10 · Certificación 3 · **2 horas**
- Hoy: integrar el juez · demo E2E de métricas · retos · cierre
- Frase del día: **el verde no es una opinión: es un conjunto de umbrales acordados**

### Slide 2 — Agenda de 2 horas (2 min)
**Título:** Tres bloques cortos
- A (40): mapa Etapas 1–9
- B (40): lab `release-gate` (sano / bloqueado)
- C (20): retos · evaluación · retrospectiva
- Dos pausas de 10 minutos

### Slide 3 — De S1 a S9 en un minuto (6 min)
**Título:** Nueve preguntas al pipeline
- 1 Diseño · 2–3 API/contrato · 4 UI · 5 CI
- 6 Performance · 7 Seguridad/a11y · 8 Mutación · 9 Visual/móvil
- Cada una dejó un **umbral** o una **evidencia**
- Hoy el juez las mira juntas

### Slide 4 — Qué es un Release Gate (5 min)
**Título:** Un solo veredicto
- Entrada: métricas (JSON)
- Proceso: comparar contra THRESHOLDS
- Salida: `passed` + lista `failed` + **exit code**
- Si un check falla → el release **no** mergea

### Slide 5 — Umbrales del curso (6 min)
**Título:** Los números que ya conocen
- pass_rate ≥ 0.95 · p95 ≤ 500 ms
- ZAP fail_new ≤ 0 (WARN no bloquea)
- mutation ≥ 0.90 · a11y critical ≤ 0
- visual_diff ≤ 120 px (S9)
- En el umbral exacto: **pasa**

### Slide 6 — Score ≠ gate (otra vez) (5 min)
**Título:** Medir no es bloquear
- Ver sobrevivientes / WARN / diff ≠ rojo automático
- El umbral decide (S6 K6 · S7 rules.tsv · S8 --enforce-gate · S9 gate/)
- Hoy: un CLI que aplica todos los umbrales
- Cultura: acordar umbrales en equipo, no en silencio

### Slide 7 — Café (1 min)
**Título:** Pausá 10
- Cuando volvamos: corremos el juez con tres JSON

### Slide 8 — Arranque Bloque B (1 min)
**Título:** Lab del juez
- Carpeta: `proyecto-integrador/release-gate`
- Yo corro; vos podés seguir en silencio
- Objetivo: ver exit 0 y exit 1 y leer el JSON

### Slide 9 — Setup + tests del juez (5 min)
**Título:** Primero la suite del lab
- `uv sync --group dev`
- `uv run pytest -v` → **6 passed**
- El juez tiene tests propios (no es magia)
- Task: `task test:gate`

### Slide 9b — Anatomía del repo (4 min)
**Título:** Core del juez (config, no magia)
- `pyproject.toml` — solo pytest; `pythonpath = ["src"]`
- `src/release_gate/__init__.py` — `THRESHOLDS` + `evaluate()`
- `run_gate.py` — atajo: mete `src/` en el path (Windows-friendly)
- `metrics/*.json` — entradas de demo (simulan artefactos de CI)
- `tests/` — el juez se prueba a sí mismo antes de juzgar

### Slide 10 — Release sano (7 min)
**Título:** metrics/healthy.json → exit 0
- Comando: `uv run python run_gate.py metrics/healthy.json`
- Los 6 checks en `true` · `failed: []` · `passed: true`
- Stderr: `RELEASE: PASA`
- Ese es el merge feliz

### Slide 11 — Bloqueo por mutación (7 min)
**Título:** mutation 0.80 < 0.90
- Comando: `uv run python run_gate.py metrics/blocked_mutation.json`
- Solo `mutation: false` · exit **1**
- Mismo patrón del reto práctico (`retos/reto-practico`)
- El resto puede estar verde: igual se bloquea

### Slide 12 — Bloqueo por visual (7 min)
**Título:** Etapa 9 dentro del juez
- Comando: `uv run python run_gate.py metrics/blocked_visual.json`
- `visual_diff_pixels` enorme (banner broken de S9)
- `failed: ["visual"]` · exit **1**
- El lab de clase incluye visual; el reto alumno no (a propósito)

### Slide 13 — Varios fallos a la vez (5 min)
**Título:** metrics/blocked_many.json
- Varios checks en rojo · lista `failed` completa
- En un PR real: priorizá por riesgo (seguridad / a11y / perf)
- El juez no prioriza: solo reporta; el equipo decide el orden de arreglo

### Slide 14 — Plantilla CI + café (3 min)
**Título:** qa-release-gate.yml
- Workflow de ejemplo en `workflows/`
- Corre pytest del juez + demo sano + demo bloqueado
- Pausá 10 · después: retos y cierre

### Slide 15 — Retos del curso (6 min)
**Título:** Dónde practicar solos
- Teóricos 1 y 2 + práctico Release Gate: carpeta `retos/`
- Paquete: `retos/RETOS_COMPLETOS.md`
- Práctico GitHub: `retos/reto-practico` (14 tests)
- El lab de hoy = juez completo con visual

### Slide 16 — Evaluación rápida (6 min)
**Título:** Cinco preguntas (el instructor las responde en voz alta)
- ¿Cobertura = calidad? No.
- ¿WARN de ZAP bloquea? No.
- ¿Mutante equivalente se puede matar? No.
- ¿Gate visual con broken=1 debe quedar verde? No.
- ¿Appium fue hands-on obligatorio? No: mapa; Playwright sí.

### Slide 17 — Retrospectiva (5 min)
**Título:** Tres frases para llevarse
- Qué usaría mañana en el trabajo
- Qué les costó más (Docker, mutación, ZAP, visual…)
- Qué umbral negociarían primero con el equipo
- El instructor modela una respuesta; no hace ronda obligatoria

### Slide 18 — Cierre del curso (3 min)
**Título:** Gracias
- Construyeron una puerta de 9 etapas + un juez
- Mantenerla es trabajo continuo (umbrales, baselines, flaky)
- Frase final: el verde no es una opinión
- Certificación 3 — cerrada en contenido
