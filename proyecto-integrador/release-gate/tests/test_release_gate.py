"""Tests del release gate (Sesión 10)."""

import json
from pathlib import Path

import pytest

from release_gate import (
    THRESHOLDS,
    a11y_critical_ok,
    evaluate,
    load_metrics,
    mutation_score,
    p95_ok,
    pass_rate,
    visual_ok,
    zap_gate,
)

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "metrics"
DEMOS = ROOT / "demos"

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


# Cada JSON de metrics/ debe producir exactamente este resultado en clase.
ESCENARIOS_JSON = [
    ("healthy.json", []),
    ("blocked_pass_rate.json", ["pass_rate"]),
    ("blocked_p95.json", ["p95"]),
    ("blocked_zap.json", ["zap"]),
    ("blocked_a11y.json", ["a11y"]),
    ("blocked_mutation.json", ["mutation"]),
    ("blocked_visual.json", ["visual"]),
    (
        "blocked_many.json",
        ["pass_rate", "p95", "zap", "mutation", "a11y", "visual"],
    ),
]


@pytest.mark.parametrize(
    "json_name,expected_failed",
    ESCENARIOS_JSON,
    ids=[name for name, _ in ESCENARIOS_JSON],
)
def test_escenarios_metrics_json(json_name, expected_failed):
    """Los JSON de demo se evalúan igual que en la clase (exit 0/1)."""
    path = METRICS / json_name
    assert path.exists(), f"Falta {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    result = evaluate(data)
    assert set(result["failed"]) == set(expected_failed)
    assert result["passed"] is (len(expected_failed) == 0)


def test_load_metrics_incomplete_corta():
    """demos/incomplete.json: faltan claves → SystemExit (no evalua)."""
    path = DEMOS / "incomplete.json"
    assert path.exists(), f"Falta {path}"
    with pytest.raises(SystemExit, match="JSON incompleto"):
        load_metrics(path)


def test_load_metrics_invalid_corta():
    """demos/invalid.json: trailing comma → SystemExit (JSON invalido)."""
    path = DEMOS / "invalid.json"
    assert path.exists(), f"Falta {path}"
    with pytest.raises(SystemExit, match="JSON invalido"):
        load_metrics(path)


def test_load_metrics_healthy_ok():
    data = load_metrics(METRICS / "healthy.json")
    assert data["pass_rate"] == pytest.approx(0.97)
