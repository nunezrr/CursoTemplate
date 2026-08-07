"""Puerta de Calidad de Release — Sesión 10 (Etapas 1–9 resumidas en un juez).

Lee un JSON de métricas, aplica THRESHOLDS del curso y decide:
  exit 0 → release puede seguir
  exit 1 → release bloqueado

Incluye el chequeo visual de la S9 (diff de píxeles).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

THRESHOLDS = {
    "pass_rate": 0.95,        # falla si <
    "p95_ms": 500,            # falla si p95 >
    "zap_fail_new": 0,        # falla si fail_new >
    "mutation_score": 0.90,   # falla si <
    "a11y_critical": 0,       # falla si critical >
    "visual_diff_pixels": 120,  # falla si diff >
}


def pass_rate(passed: int, total: int) -> float:
    if total == 0:
        return 1.0
    return passed / total


def p95_ok(p95_ms: float, threshold_ms: float | None = None) -> bool:
    limit = THRESHOLDS["p95_ms"] if threshold_ms is None else threshold_ms
    return p95_ms <= limit


def zap_gate(fail_new: int, warn_new: int = 0, fail_limit: int | None = None) -> bool:
    limit = THRESHOLDS["zap_fail_new"] if fail_limit is None else fail_limit
    _ = warn_new
    return fail_new <= limit


def mutation_score(killed: int, total_mutants: int) -> float:
    if total_mutants == 0:
        return 1.0
    return killed / total_mutants


def a11y_critical_ok(critical_violations: int) -> bool:
    return critical_violations <= THRESHOLDS["a11y_critical"]


def visual_ok(diff_pixels: int, max_diff: int | None = None) -> bool:
    """True si el diff visual está dentro del umbral (S9)."""
    limit = THRESHOLDS["visual_diff_pixels"] if max_diff is None else max_diff
    return diff_pixels <= limit


def evaluate(metrics: dict) -> dict:
    """Evalúa métricas del release. Devuelve checks + passed + failed list."""
    checks = {
        "pass_rate": metrics["pass_rate"] >= THRESHOLDS["pass_rate"],
        "p95": p95_ok(metrics["p95_ms"]),
        "zap": zap_gate(metrics["zap_fail_new"]),
        "mutation": metrics["mutation_score"] >= THRESHOLDS["mutation_score"],
        "a11y": a11y_critical_ok(metrics["a11y_critical"]),
        "visual": visual_ok(metrics["visual_diff_pixels"]),
    }
    failed = [name for name, ok in checks.items() if not ok]
    return {
        "checks": checks,
        "failed": failed,
        "passed": len(failed) == 0,
        "thresholds": dict(THRESHOLDS),
    }


REQUIRED_KEYS = {
    "pass_rate",
    "p95_ms",
    "zap_fail_new",
    "mutation_score",
    "a11y_critical",
    "visual_diff_pixels",
}


def load_metrics(path: Path) -> dict:
    """Lee y valida el contrato de entrada. Errores claros para la demo en clase."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"No se pudo leer {path}: {exc}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        # ASCII: consolas Windows cp1252 corrompen acentos.
        raise SystemExit(
            f"JSON invalido en {path.name}: {exc.msg} (linea {exc.lineno}, col {exc.colno})"
        ) from exc

    if not isinstance(data, dict):
        raise SystemExit(f"JSON invalido en {path.name}: se esperaba un objeto {{...}}")

    missing = REQUIRED_KEYS - set(data)
    if missing:
        raise SystemExit(f"JSON incompleto; faltan: {sorted(missing)}")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="QA Release Gate — decide si el release pasa o se bloquea"
    )
    parser.add_argument(
        "metrics_json",
        type=Path,
        help="Ruta a un JSON de métricas (ver metrics/*.json)",
    )
    args = parser.parse_args(argv)

    metrics = load_metrics(args.metrics_json)
    result = evaluate(metrics)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Mensajes en ASCII: las consolas Windows cp1252 corrompen acentos/em-dash.
    if result["passed"]:
        print("\nRELEASE: PASA", file=sys.stderr)
        return 0
    print(
        f"\nRELEASE: BLOQUEADO - fallo: {', '.join(result['failed'])}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
