"""QA Release Gate — Reto práctico Certificación 3.

Implementá las funciones marcadas con TODO. La suite en
tests/test_release_gate.py valida cada una: cuando todo esté bien
implementado vas a ver 14 passed.

Regla del reto: no modifiques THRESHOLDS ni los tests.
"""

from __future__ import annotations

import json

# Umbrales del curso (S4–S8) — no los cambies
THRESHOLDS = {
    "pass_rate": 0.95,       # falla si <
    "p95_ms": 500,           # falla si p95 >
    "zap_fail_new": 0,       # falla si fail_new >
    "mutation_score": 0.90,  # falla si <
    "a11y_critical": 0,      # falla si critical >
}


def pass_rate(passed: int, total: int) -> float:
    """Tests que pasaron / tests ejecutados (API/UI).

    Caso borde: si total es 0, devolvé 1.0 (nada que fallar).
    Ejemplo: pass_rate(95, 100) -> 0.95
    """
    # TODO: implementar
    raise NotImplementedError


def p95_ok(p95_ms: float, threshold_ms: float | None = None) -> bool:
    """True si el p95 está dentro del umbral de K6 (gate de performance).

    Pasa si p95_ms <= threshold. Por defecto usá THRESHOLDS["p95_ms"].
    Ejemplo: p95_ok(180, 500) -> True; p95_ok(800, 500) -> False
    """
    # TODO: implementar
    raise NotImplementedError


def zap_gate(fail_new: int, warn_new: int = 0, fail_limit: int | None = None) -> bool:
    """Gate de ZAP: los FAIL bloquean; los WARN no (patrón baseline + -I).

    Pasa si fail_new <= fail_limit. Por defecto fail_limit = THRESHOLDS["zap_fail_new"] (0).
    warn_new se ignora a propósito (no tumba el job).
    Ejemplo: zap_gate(0, 7) -> True; zap_gate(1, 0) -> False
    """
    # TODO: implementar
    raise NotImplementedError


def mutation_score(killed: int, total_mutants: int) -> float:
    """Mutantes muertos / total de mutantes.

    Caso borde: si total_mutants es 0, devolvé 1.0.
    Ejemplo: mutation_score(45, 50) -> 0.90
    """
    # TODO: implementar
    raise NotImplementedError


def a11y_critical_ok(critical_violations: int) -> bool:
    """True si no hay violaciones Axe de impacto critical.

    Pasa si critical_violations <= THRESHOLDS["a11y_critical"] (0).
    Ejemplo: a11y_critical_ok(0) -> True; a11y_critical_ok(1) -> False
    """
    # TODO: implementar
    raise NotImplementedError


def release_gate(metrics: dict) -> dict:
    """Evalúa el release contra THRESHOLDS y decide.

    metrics trae exactamente estas llaves:
      pass_rate (float), p95_ms (float), zap_fail_new (int),
      mutation_score (float), a11y_critical (int)

    Devuelve: {"checks": {<nombre>: bool, ...}, "passed": bool}
    - pass_rate: True si >= THRESHOLDS["pass_rate"]
    - p95: True si p95_ok(metrics["p95_ms"])
    - zap: True si zap_gate(metrics["zap_fail_new"])
    - mutation: True si mutation_score >= THRESHOLDS["mutation_score"]
    - a11y: True si a11y_critical_ok(metrics["a11y_critical"])
    - Valor exactamente en el umbral PASA (falla solo si lo cruza).
    - passed es True solo si TODOS los checks son True.
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # Release de ejemplo: todo sano excepto mutation score (40/50 = 0.80 < 0.90)
    release = {
        "pass_rate": pass_rate(97, 100),
        "p95_ms": 220.0,
        "zap_fail_new": 0,
        "mutation_score": mutation_score(40, 50),
        "a11y_critical": 0,
    }
    print(json.dumps(release_gate(release), indent=2))
