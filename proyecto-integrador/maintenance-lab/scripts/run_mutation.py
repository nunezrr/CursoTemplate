"""Runner multiplataforma del mutation testing (Sesión 8).

Por qué existe este script
--------------------------
Los comandos de cosmic-ray funcionan, pero encadenarlos a mano (o en Taskfile
con redirecciones ``>``) falla de formas distintas según la shell:

- En Windows, ``python -m pytest`` (sin ``uv run``) apunta al Python del sistema.
- ``cr-html ... > reports/mutation.html`` depende de cómo Task/PowerShell/cmd
  manejen el redirect y el encoding.
- ``cosmic-ray init`` sin ``--force`` falla si ya existe ``session.sqlite``.
- El gate (``cr-rate --fail-over 10``) SALE CON ERROR cuando la suite es la
  débil a propósito (score 50%). Eso es el punto pedagógico, pero no debe
  hacer que ``task test:maint:mutation`` "falle" de forma confusa.

Este script hace el flujo completo y sale 0 si la mutación corrió bien.
El gate se reporta; solo bloquea el exit code si pasás ``--enforce-gate``.

Uso
---
    python scripts/run_mutation.py              # flujo completo, exit 0
    python scripts/run_mutation.py --enforce-gate   # exit 1 si score < 90%
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "cosmic-ray.toml"
SESSION = ROOT / "session.sqlite"
REPORTS = ROOT / "reports"
REPORT_HTML = REPORTS / "mutation.html"
# Umbral del gate (Etapa 8): falla si sobrevive MÁS de este % (score < 90%).
FAIL_OVER = 10.0


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print(f"\n>> {' '.join(cmd)}", flush=True)
    return subprocess.run(
        cmd,
        cwd=ROOT,
        check=check,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Mutation testing S8 (cosmic-ray)")
    parser.add_argument(
        "--enforce-gate",
        action="store_true",
        help="Exit 1 si la tasa de sobrevivientes supera 10%% (score < 90%%)",
    )
    args = parser.parse_args()

    if shutil.which("uv") is None:
        print("ERROR: necesitás `uv` en el PATH. Ver SETUP_ESTUDIANTES.md", file=sys.stderr)
        return 2

    if not CONFIG.exists():
        print(f"ERROR: no existe {CONFIG}", file=sys.stderr)
        return 2

    REPORTS.mkdir(parents=True, exist_ok=True)

    # 1) Baseline: la suite debe pasar SIN mutar.
    run(["uv", "run", "cosmic-ray", "baseline", str(CONFIG)])

    # 2) Init idempotente: --force recrea la sesión aunque exista sqlite.
    run(["uv", "run", "cosmic-ray", "init", "--force", str(CONFIG), str(SESSION)])

    # 3) Ejecutar mutantes.
    run(["uv", "run", "cosmic-ray", "exec", str(CONFIG), str(SESSION)])

    # 4) Reporte HTML sin depender del redirect de la shell.
    html = subprocess.check_output(
        ["uv", "run", "cr-html", str(SESSION)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    REPORT_HTML.write_text(html, encoding="utf-8")
    print(f"\n>> reporte HTML: {REPORT_HTML} ({REPORT_HTML.stat().st_size} bytes)")

    # 5) Resumen en terminal.
    run(["uv", "run", "cr-report", str(SESSION)])

    # 6) Gate: medir tasa de sobrevivientes.
    rate_proc = subprocess.run(
        ["uv", "run", "cr-rate", str(SESSION)],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    rate_text = (rate_proc.stdout or "").strip()
    try:
        survival = float(rate_text)
    except ValueError:
        print(f"ERROR: no pude interpretar cr-rate: {rate_text!r}", file=sys.stderr)
        return 2

    score = 100.0 - survival
    print(f"\n>> survival rate: {survival:.2f}%  |  mutation score: {score:.2f}%")
    print(f">> gate (fail-over {FAIL_OVER}%): ", end="")

    gate_blocks = survival > FAIL_OVER
    if gate_blocks:
        print(f"BLOQUEA (esperado con la suite debil de clase)")
    else:
        print("PASA")

    if args.enforce_gate and gate_blocks:
        print(
            f"\nGate enforced: survival {survival:.2f}% > {FAIL_OVER}% -> exit 1",
            file=sys.stderr,
        )
        return 1

    print("\nOK - mutation run completo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
