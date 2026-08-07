# release-gate — Sesión 10

Juez único de la **Puerta de Calidad de Release**. Lee un JSON de métricas
(pass rate, p95, ZAP, mutación, a11y, diff visual) y decide exit 0 / 1.

Lab **sincronizado en clase**: mismos comandos en la máquina del instructor y
en la de cada alumno. Sin Docker. Solo `uv` + Python.

## Estructura

```
release-gate/
├── pyproject.toml
├── run_gate.py                 ← uv run python run_gate.py metrics/…
├── scripts/run_all_demos.py    ← arco completo en un comando
├── scripts/demo_force_fail.py  ← tres fallos forzados (clase)
├── src/release_gate/__init__.py  ← THRESHOLDS + evaluate()
├── metrics/*.json              ← escenarios de demo (negocio)
├── demos/                      ← JSON rotos (incompleto / inválido)
├── tests/test_release_gate.py
└── workflows/qa-release-gate.yml
```

## Setup

```bash
cd proyecto-integrador/release-gate
uv sync --group dev
```

## Comandos (lab sincronizado)

```bash
# Suite del juez (16 passed: unitarios + escenarios + demos rotos)
uv run pytest -v

# Release sano → exit 0
uv run python run_gate.py metrics/healthy.json

# Un solo check rojo (Bloque C)
uv run python run_gate.py metrics/blocked_p95.json
uv run python run_gate.py metrics/blocked_zap.json
uv run python run_gate.py metrics/blocked_a11y.json
uv run python run_gate.py metrics/blocked_pass_rate.json
uv run python run_gate.py metrics/blocked_mutation.json
uv run python run_gate.py metrics/blocked_visual.json

# Varios fallos → exit 1
uv run python run_gate.py metrics/blocked_many.json

# Arco completo (todos los escenarios)
uv run python scripts/run_all_demos.py

# Forzar fallos (incompleto + inválido + AssertionError de pytest)
uv run python run_gate.py demos/incomplete.json
uv run python run_gate.py demos/invalid.json
uv run python scripts/demo_force_fail.py
```

Atajos: `task test:gate` · `task test:gate:healthy` · `task test:gate:demos` · `task test:gate:force-fail`.

**Demo en vivo — desbloquear:** abrí `metrics/blocked_mutation.json`, cambiá
`mutation_score` de `0.80` a `0.96`, guardá y volvé a correr el gate → exit 0.
Al terminar revertí con `git checkout -- metrics/blocked_mutation.json`
(cada JSON tiene test: si queda editado, `pytest` falla).

**Demo en vivo — forzar el assert:** `demo_force_fail.py` copia `healthy.json`
sobre `blocked_mutation.json`, corre el test del escenario (falla en rojo) y
restaura el archivo solo.

## Umbrales

| Check | Umbral | Sesión |
|---|---|---|
| pass_rate | ≥ 0.95 | S4/S5 |
| p95_ms | ≤ 500 | S6 |
| zap_fail_new | ≤ 0 | S7 |
| a11y_critical | ≤ 0 | S7 |
| mutation_score | ≥ 0.90 | S8 |
| visual_diff_pixels | ≤ 120 | S9 |
