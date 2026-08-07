#!/usr/bin/env python
"""Demo en vivo: tres clases de fallo (Sesion 10).

    uv run python scripts/demo_force_fail.py

1) JSON incompleto  -> el CLI corta ANTES del juez
2) JSON invalido    -> el CLI corta en el parseo
3) Assert de pytest -> fixture que miente: el test del escenario falla en rojo

El paso 3 envenena metrics/blocked_mutation.json, muestra el AssertionError
y SIEMPRE restaura el archivo (aunque el proceso se interrumpa).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "run_gate.py"
DEMOS = ROOT / "demos"
MUTATION = ROOT / "metrics" / "blocked_mutation.json"
HEALTHY = ROOT / "metrics" / "healthy.json"


def banner(title: str) -> None:
    # ASCII only: Windows cp1252 corrupts em-dash / accents in banners.
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run(cmd: list[str]) -> int:
    print(f"\n>> {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=ROOT).returncode


def demo_incomplete() -> None:
    banner("FALLO 1/3 - JSON incompleto (contrato de entrada)")
    print(
        "Faltan mutation_score y visual_diff_pixels.\n"
        "El juez NO evalua: corta con 'JSON incompleto'.\n"
        "Leccion: informacion ausente NUNCA es verde."
    )
    code = run(
        ["uv", "run", "python", str(GATE), str(DEMOS / "incomplete.json")]
    )
    print(f"\n  exit={code}  (esperado != 0)")
    if code == 0:
        print("  INESPERADO: debia fallar.")


def demo_invalid() -> None:
    banner("FALLO 2/3 - JSON invalido (sintaxis)")
    print(
        "Trailing comma ilegal en demos/invalid.json.\n"
        "El CLI corta en json.loads con mensaje de linea/columna.\n"
        "Leccion: basura en el artefacto != metrica mala; es basura."
    )
    code = run(
        ["uv", "run", "python", str(GATE), str(DEMOS / "invalid.json")]
    )
    print(f"\n  exit={code}  (esperado != 0)")
    if code == 0:
        print("  INESPERADO: debia fallar.")


def demo_assert_fail() -> None:
    banner("FALLO 3/3 - Assert de pytest (fixture que miente)")
    print(
        "Vamos a copiar healthy.json SOBRE blocked_mutation.json.\n"
        "El gate diria PASA, pero el test espera failed=['mutation'].\n"
        "pytest debe fallar en rojo con AssertionError.\n"
        "Despues se restaura el archivo automaticamente."
    )

    if not MUTATION.exists() or not HEALTHY.exists():
        print(f"FALTA {MUTATION} o {HEALTHY}")
        return

    # Backup en memoria (evita PermissionError de tempfile en Windows).
    original = MUTATION.read_text(encoding="utf-8")
    try:
        # Envenenar: el nombre promete bloqueo por mutacion; los datos son sanos.
        shutil.copy2(HEALTHY, MUTATION)
        print(f"\n  Envenenado: {MUTATION.name} ahora tiene datos de healthy.json")

        code = run(
            [
                "uv",
                "run",
                "pytest",
                "-v",
                "tests/test_release_gate.py::test_escenarios_metrics_json[blocked_mutation.json]",
            ]
        )
        print(f"\n  pytest exit={code}  (esperado != 0 = AssertionError en pantalla)")
        if code == 0:
            print("  INESPERADO: el assert debia fallar.")
        else:
            print(
                "  OK pedagogico: el lab se auto-protege.\n"
                "  Si alguien edita un JSON de demo 'para que pase',\n"
                "  pytest lo delata porque el contrato del escenario quedo roto."
            )
    finally:
        MUTATION.write_text(original, encoding="utf-8")
        print(f"\n  Restaurado: {MUTATION.name}")
        data = json.loads(MUTATION.read_text(encoding="utf-8"))
        print(f"  mutation_score actual = {data.get('mutation_score')} (debe ser 0.8)")


def main() -> int:
    print("=== S10 release-gate - forzar fallos (demo instructor) ===")
    print("Tres rojos distintos. Narralos en este orden.")
    demo_incomplete()
    demo_invalid()
    demo_assert_fail()
    banner("FIN - tres clases de fallo demostradas")
    print(
        "Resumen para la pizarra:\n"
        "  1. incompleto  -> contrato de entrada\n"
        "  2. invalido    -> sintaxis del artefacto\n"
        "  3. assert      -> el fixture miente / el lab se protege\n"
        "  (+ blocked_*.json -> metrica bajo umbral = gate de negocio)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
