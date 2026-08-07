# maintenance-lab — Sesión 8

Laboratorio de **mantenimiento de suites**: mutation testing, tests flaky y
selectores robustos. Es la **Etapa 8** del proyecto integrador (calidad del
conjunto de pruebas, más allá de la cobertura).

Todo corre con `uv` + Playwright, **sin Docker** y **sin workarounds** en
Windows, macOS y Linux. Las tasks de mutación/flaky son **deterministas**.
`task test:maint:healing` sale **exit 1** a propósito (selector frágil en rojo).

## Por qué estas herramientas (y no las del temario original)

| Tema | Temario original | Lo que usamos | Por qué |
|---|---|---|---|
| Mutation testing | mutmut | **cosmic-ray** | mutmut 3.x necesita `fork` y no corre en Windows nativo (exige WSL). cosmic-ray está mantenido (2026), soporta Windows nativo y genera reporte HTML. |
| Auto-healing | Healenium | **Selectores robustos + reparación con IA** (mapa: Healenium/Alumnium) | Healenium es solo Selenium y pide ~5 contenedores; el curso es Playwright-first. La recomendación 2026 es prevenir con selectores por rol/texto y usar healing como red secundaria. |

## Setup (máquina limpia — una sola vez)

```bash
cd proyecto-integrador/maintenance-lab
uv sync --group dev
uv run playwright install chromium
# o desde la raíz del repo: task setup:maint
```

Requisitos: Python 3.12+, `uv` en el PATH. No hace falta Docker ni WSL.

## Tasks deterministas (siempre el mismo resultado)

| Task | Qué hace | Exit esperado |
|---|---|---|
| `task test:maint` | Suite oficial débil | **0** · 7 passed |
| `task test:maint:mutation` | cosmic-ray completo + HTML | **0** · score **50%** (gate reporta BLOQUEA, pero no tumba la task) |
| `task test:maint:flaky` | Meta-demo de flakiness + cura | **0** · 2 passed |
| `task test:maint:healing` | Selector frágil vs robusto | **1** · 1 failed (frágil), 1 passed (robusto) |

### Mutation testing (Bloque B — Etapa 8)

```bash
# Preferido (multiplataforma, idempotente):
python scripts/run_mutation.py

# Gate estricto del pipeline (con la suite débil SALE 1 — eso es el punto):
python scripts/run_mutation.py --enforce-gate
```

Con la suite débil sobreviven **25 de 50 mutantes (score 50%)**. Escribiendo
los tests de `soluciones/test_mutantes.py` en `tests/`, el score sube a **~96%**
y solo quedan **2 mutantes equivalentes**.

### Flaky (Bloque C)

```bash
# Verificación determinista (task):
uv run pytest flaky/test_flaky_consistent.py -v

# Demo EN VIVO en clase (NO determinista — corré 2–3 veces a mano):
uv run pytest flaky/test_flaky_demo.py::test_worker_es_w1_FLAKY -v
```

### Selectores (Bloque C)

```bash
uv run pytest healing/test_selectores.py -v
# 1 failed (frágil, #login-btn) · 1 passed (robusto, get_by_role)
# Exit 1 a propósito: el selector roto no se esconde con xfail.
```

## Problemas que ya resolvimos (no los vas a ver)

| Problema en Windows | Solución en el repo |
|---|---|
| mutmut no corre (necesita `fork`) | Usamos **cosmic-ray** |
| `cosmic-ray.toml` con acentos → `charmap` codec error | Archivo en **ASCII** |
| `python -m pytest` sin venv → "No module named pytest" | `test-command` usa **`uv run python -m pytest`** |
| `init` falla si ya existe `session.sqlite` | Script usa **`init --force`** |
| `> reports/mutation.html` frágil entre shells | Script escribe el HTML en Python |
| `cr-rate --fail-over 10` hace fallar la task con suite débil | Gate es informativo; `--enforce-gate` solo si lo pedís |
| `task test:maint:flaky` a veces rojo | Task corre solo demos **deterministas**; el flaky vivo es manual |

## Estructura

```
maintenance-lab/
├── maintenance_lab/discount.py      ← blanco de mutación (regla de la S1)
├── tests/test_discount.py           ← suite oficial (débil a propósito)
├── soluciones/test_mutantes.py      ← tests que matan mutantes (referencia)
├── cosmic-ray.toml                  ← config (ASCII + uv run)
├── scripts/run_mutation.py          ← runner idempotente multiplataforma
├── flaky/                           ← demo flaky (consistent + live)
├── healing/                         ← app v1/v2 + selector frágil vs robusto
├── workflows/qa-mutation.yml        ← Etapa 8 en GitHub Actions
└── reports/                         ← reporte HTML (generado)
```
