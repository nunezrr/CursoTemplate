"""Tests del release gate (Sesión 10)."""

from pathlib import Path

import pytest

from release_gate import (
    THRESHOLDS,
    a11y_critical_ok,
    evaluate,
    mutation_score,
    p95_ok,
    pass_rate,
    visual_ok,
    zap_gate,
)

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "metrics"

HEALTHY = {
    "pass_rate": 0.97,
    "p95_ms": 220.0,
    "zap_fail_new": 0,
    "mutation_score": 0.96,
    "a11y_critical": 0,
    "visual_diff_pixels": 12,
}


def test_helpers_basicos():
    assert pass_rate(97, 100) == pytest.approx(0.97)
    assert pass_rate(0, 0) == 1.0
    assert p95_ok(500) is True
    assert p95_ok(501) is False
    assert zap_gate(0, warn_new=7) is True
    assert zap_gate(1) is False
    assert mutation_score(45, 50) == pytest.approx(0.90)
    assert a11y_critical_ok(0) is True
    assert visual_ok(120) is True
    assert visual_ok(121) is False


def test_evaluate_sano_pasa():
    result = evaluate(HEALTHY)
    assert result["passed"] is True
    assert result["failed"] == []
    assert set(result["checks"]) == {
        "pass_rate",
        "p95",
        "zap",
        "mutation",
        "a11y",
        "visual",
    }


def test_evaluate_bloquea_mutation():
    metrics = dict(HEALTHY, mutation_score=0.80)
    result = evaluate(metrics)
    assert result["passed"] is False
    assert result["failed"] == ["mutation"]


def test_evaluate_bloquea_visual():
    metrics = dict(HEALTHY, visual_diff_pixels=THRESHOLDS["visual_diff_pixels"] + 1)
    result = evaluate(metrics)
    assert result["passed"] is False
    assert "visual" in result["failed"]


def test_evaluate_bloquea_varios():
    metrics = {
        "pass_rate": 0.91,
        "p95_ms": 900.0,
        "zap_fail_new": 2,
        "mutation_score": 0.50,
        "a11y_critical": 1,
        "visual_diff_pixels": 5000,
    }
    result = evaluate(metrics)
    assert result["passed"] is False
    assert set(result["failed"]) == {
        "pass_rate",
        "p95",
        "zap",
        "mutation",
        "a11y",
        "visual",
    }


def test_json_fixtures_existen():
    assert (METRICS / "healthy.json").exists()
    assert (METRICS / "blocked_mutation.json").exists()
    assert (METRICS / "blocked_visual.json").exists()
