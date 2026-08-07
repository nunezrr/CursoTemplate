"""Comparación visual simple (línea base PNG vs captura actual)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops

BASELINES = Path(__file__).resolve().parent / "baselines"


def count_diff_pixels(baseline: Path, actual: Path) -> int:
    """Cuenta píxeles distintos entre dos PNG del mismo tamaño."""
    a = Image.open(baseline).convert("RGB")
    b = Image.open(actual).convert("RGB")
    if a.size != b.size:
        return max(a.size[0] * a.size[1], b.size[0] * b.size[1])
    diff = ImageChops.difference(a, b)
    raw = diff.tobytes()
    # RGB empaquetado: un píxel difiere si algún canal ≠ 0.
    return sum(
        1
        for i in range(0, len(raw), 3)
        if raw[i] or raw[i + 1] or raw[i + 2]
    )


def assert_matches_baseline(
    baseline_name: str,
    actual_png: Path,
    *,
    max_diff_pixels: int = 120,
) -> None:
    baseline = BASELINES / baseline_name
    assert baseline.exists(), (
        f"No existe la baseline {baseline}. "
        "Generala con: uv run python scripts/capture_baselines.py"
    )
    diffs = count_diff_pixels(baseline, actual_png)
    assert diffs <= max_diff_pixels, (
        f"Gate visual FALLA: {diffs} píxeles distintos vs {baseline_name} "
        f"(máx permitido {max_diff_pixels}). Actual: {actual_png}"
    )
