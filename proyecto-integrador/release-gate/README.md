# release-gate — Sesión 10

Juez único de la **Puerta de Calidad de Release**. Lee un JSON de métricas
(pass rate, p95, ZAP, mutación, a11y, diff visual) y decide exit 0 / 1.

## Estructura

```
release-gate/
├── pyproject.toml
├── run_gate.py                 ← uv run python run_gate.py metrics/…
├── src/release_gate/__init__.py  ← THRESHOLDS + evaluate()
├── metrics/*.json              ← entradas de demo
├── tests/test_release_gate.py
└── workflows/qa-release-gate.yml
```

## Setup

```bash
cd proyecto-integrador/release-gate
uv sync --group dev
```

## Comandos

```bash
# Suite del lab
uv run pytest -v

# Release sano → exit 0
uv run python run_gate.py metrics/healthy.json

# Bloqueado por mutación → exit 1
uv run python run_gate.py metrics/blocked_mutation.json

# Bloqueado por visual (S9) → exit 1
uv run python run_gate.py metrics/blocked_visual.json
```

Atajos: `task test:gate` · `task test:gate:healthy` · `task test:gate:blocked`.

## Umbrales

| Check | Umbral | Sesión |
|---|---|---|
| pass_rate | ≥ 0.95 | S4/S5 |
| p95_ms | ≤ 500 | S6 |
| zap_fail_new | ≤ 0 | S7 |
| a11y_critical | ≤ 0 | S7 |
| mutation_score | ≥ 0.90 | S8 |
| visual_diff_pixels | ≤ 120 | S9 |

El reto práctico en `retos/reto-practico/` es la versión para alumnos (sin visual).
Este lab es la versión de clase con Etapa 9 incluida.
