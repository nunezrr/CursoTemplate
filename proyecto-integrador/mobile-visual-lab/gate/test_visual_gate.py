"""Gate visual Etapa 9: UI rota vs baseline sana → el test DEBE fallar.

No está en tests/: la suite oficial (smoke + visual) queda verde.
Corré: uv run pytest gate -v  → exit 1 esperado.
"""

from pathlib import Path

from playwright.sync_api import Page

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
BASELINES = ROOT / "tests" / "baselines"
APP = ROOT / "app" / "index.html"
DESKTOP = {"width": 1280, "height": 720}
MAX_DIFF = 120


def _count_diff_pixels(baseline: Path, actual: Path) -> int:
    from PIL import Image, ImageChops

    a = Image.open(baseline).convert("RGB")
    b = Image.open(actual).convert("RGB")
    if a.size != b.size:
        return max(a.size[0] * a.size[1], b.size[0] * b.size[1])
    raw = ImageChops.difference(a, b).tobytes()
    return sum(
        1
        for i in range(0, len(raw), 3)
        if raw[i] or raw[i + 1] or raw[i + 2]
    )

def test_broken_ui_falla_gate_visual(page: Page) -> None:
    page.set_viewport_size(DESKTOP)
    page.goto(APP.as_uri() + "?broken=1")
    REPORTS.mkdir(parents=True, exist_ok=True)
    actual = REPORTS / "actual-broken-desktop.png"
    page.screenshot(path=actual, full_page=True)

    baseline = BASELINES / "home-desktop-light.png"
    assert baseline.exists(), (
        f"Falta {baseline}. Corré: python scripts/capture_baselines.py"
    )
    diffs = _count_diff_pixels(baseline, actual)
    assert diffs <= MAX_DIFF, (
        f"Gate visual FALLA: {diffs} píxeles distintos vs baseline sana "
        f"(máx {MAX_DIFF}). Actual: {actual}"
    )
