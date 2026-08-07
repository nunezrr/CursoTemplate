#!/usr/bin/env python3
"""Corre OWASP ZAP baseline contra Juice Shop (Windows / macOS / Linux).

Uso (desde cualquier cwd):
  python scripts/run_baseline.py

Requiere: Docker Desktop Running + `docker compose` en PATH.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
RULES_SRC = ROOT / "zap" / "rules.tsv"
RULES_DST = REPORTS / "rules.tsv"


def run(cmd: list[str]) -> int:
    print(f"==> {' '.join(cmd)}", flush=True)
    completed = subprocess.run(cmd, cwd=ROOT)
    return int(completed.returncode)


def main() -> int:
    if shutil.which("docker") is None:
        print(
            "ERROR: no se encontró `docker` en el PATH. Abrí Docker Desktop y reintentá.",
            flush=True,
        )
        return 1

    REPORTS.mkdir(parents=True, exist_ok=True)
    if not RULES_SRC.is_file():
        print(f"ERROR: no existe {RULES_SRC}", flush=True)
        return 1
    shutil.copyfile(RULES_SRC, RULES_DST)

    print("==> Levantando Juice Shop...", flush=True)
    code = run(["docker", "compose", "up", "-d", "--wait", "juiceshop"])
    if code != 0:
        return code

    print("==> Corriendo ZAP baseline (puede tardar ~2-3 min)...", flush=True)
    code = run(["docker", "compose", "run", "--rm", "zap-baseline"])

    report = REPORTS / "zap-report.html"
    if report.is_file():
        print(f"==> Exit code: {code}", flush=True)
        print(f"==> Abrí el reporte: {report}", flush=True)
    else:
        print(f"==> Exit code: {code}", flush=True)
        print(
            "==> No se generó zap-report.html — revisá la salida de ZAP arriba.",
            flush=True,
        )
    return code


if __name__ == "__main__":
    sys.exit(main())
