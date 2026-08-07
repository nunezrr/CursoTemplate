#!/usr/bin/env python
"""Corre el arco completo del lab S10 en orden (instructor o alumno).

    uv run python scripts/run_all_demos.py

Exit 0 si pytest pasa y cada escenario dio el exit code esperado.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (etiqueta, json relativo a metrics/, exit esperado)
# Etiquetas en ASCII: consolas Windows cp1252 corrompen los acentos.
SCENARIOS = [
    ("Release sano", "healthy.json", 0),
    ("Bloqueo pass_rate", "blocked_pass_rate.json", 1),
    ("Bloqueo p95", "blocked_p95.json", 1),
    ("Bloqueo ZAP", "blocked_zap.json", 1),
    ("Bloqueo a11y", "blocked_a11y.json", 1),
    ("Bloqueo mutation", "blocked_mutation.json", 1),
    ("Bloqueo visual (S9)", "blocked_visual.json", 1),
    ("Varios fallos", "blocked_many.json", 1),
]


def run(cmd: list[str], *, cwd: Path) -> int:
    print(f"\n>> {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=cwd)
    return proc.returncode


def main() -> int:
    print("=== S10 release-gate - arco completo ===")

    code = run(["uv", "run", "pytest", "-v"], cwd=ROOT)
    if code != 0:
        print("\nFALLO: pytest del juez")
        return code

    gate = ROOT / "run_gate.py"
    failures = 0
    for label, json_name, expected in SCENARIOS:
        path = ROOT / "metrics" / json_name
        if not path.exists():
            print(f"\nFALTA {path}")
            failures += 1
            continue
        code = run(
            ["uv", "run", "python", str(gate), str(path)],
            cwd=ROOT,
        )
        ok = code == expected
        status = "OK" if ok else "FALLO"
        print(f"  [{status}] {label}: exit {code} (esperado {expected})")
        if not ok:
            failures += 1

    if failures:
        print(f"\n{failures} escenario(s) con exit inesperado.")
        return 1
    print("\nArco completo OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
