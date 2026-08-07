# Security Lab — Sesión 7 (OWASP ZAP + Axe)

Escaneo de seguridad **baseline** con OWASP ZAP contra **OWASP Juice Shop** local,
más una demo de accesibilidad con **Axe** sobre una página HTML con problemas a propósito.

## Requisitos

- Docker Desktop **Running**
- Python 3.12+ (solo para el atajo del lab; no instala dependencias extra)
- Puerto **3000** libre (Juice Shop)
- Para Axe (opcional): `uv` + Chromium (Playwright)

## Arranque rápido — ZAP baseline

```bash
cd proyecto-integrador/security
python scripts/run_baseline.py
```

Eso levanta Juice Shop, copia `zap/rules.tsv` a `reports/` y corre el baseline.  
Reportes: `reports/zap-report.html` y `reports/zap-report.json`.

Atajo desde la raíz del curso: `task test:security:zap`.

## Axe (demo de accesibilidad)

```bash
cd proyecto-integrador/security/a11y
uv sync --group dev
uv run playwright install chromium
uv run pytest -v
```

## Detener

```bash
cd proyecto-integrador/security
docker compose down
```
