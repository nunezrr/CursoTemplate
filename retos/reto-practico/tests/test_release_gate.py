"""Suite del reto práctico — NO MODIFICAR.

Cuando las 6 funciones estén bien implementadas: 14 passed.
"""

import pytest

from src.release_gate import (
    THRESHOLDS,
    a11y_critical_ok,
    mutation_score,
    p95_ok,
    pass_rate,
    release_gate,
    zap_gate,
)

HEALTHY = {
    "pass_rate": 0.97,
    "p95_ms": 220.0,
    "zap_fail_new": 0,
    "mutation_score": 0.94,
    "a11y_critical": 0,
}


def test_pass_rate_basico():
    assert pass_rate(95, 100) == pytest.approx(0.95)
    assert pass_rate(97, 100) == pytest.approx(0.97)


def test_pass_rate_sin_tests_es_uno():
    assert pass_rate(0, 0) == 1.0


def test_p95_ok_dentro_y_fuera():
    assert p95_ok(180, 500) is True
    assert p95_ok(800, 500) is False


def test_p95_ok_en_el_limite_pasa():
    assert p95_ok(500, 500) is True


def test_p95_ok_usa_threshold_default():
    assert p95_ok(THRESHOLDS["p95_ms"] - 1) is True
    assert p95_ok(THRESHOLDS["p95_ms"] + 1) is False


def test_zap_gate_warn_no_bloquea():
    assert zap_gate(0, warn_new=7) is True


def test_zap_gate_fail_bloquea():
    assert zap_gate(1, warn_new=0) is False


def test_mutation_score_basico():
    assert mutation_score(45, 50) == pytest.approx(0.90)
    assert mutation_score(25, 50) == pytest.approx(0.50)


def test_mutation_score_sin_mutantes_es_uno():
    assert mutation_score(0, 0) == 1.0


def test_a11y_critical_ok():
    assert a11y_critical_ok(0) is True
    assert a11y_critical_ok(1) is False


def test_gate_release_sano_pasa():
    result = release_gate(HEALTHY)
    assert result["passed"] is True
    assert all(result["checks"].values())
    assert set(result["checks"]) == {"pass_rate", "p95", "zap", "mutation", "a11y"}


def test_gate_bloquea_solo_mutation():
    metrics = dict(HEALTHY, mutation_score=0.80)
    result = release_gate(metrics)
    assert result["passed"] is False
    assert result["checks"]["mutation"] is False
    fallidos = [name for name, ok in result["checks"].items() if not ok]
    assert fallidos == ["mutation"]


def test_gate_bloquea_p95():
    metrics = dict(HEALTHY, p95_ms=900.0)
    result = release_gate(metrics)
    assert result["passed"] is False
    assert result["checks"]["p95"] is False


def test_gate_umbral_exacto_pasa():
    metrics = {
        "pass_rate": 0.95,
        "p95_ms": 500.0,
        "zap_fail_new": 0,
        "mutation_score": 0.90,
        "a11y_critical": 0,
    }
    result = release_gate(metrics)
    assert result["passed"] is True
