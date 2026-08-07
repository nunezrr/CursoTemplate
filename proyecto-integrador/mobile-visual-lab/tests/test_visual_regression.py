"""Regresión visual contra baselines versionadas (Sesión 9).

Generar / actualizar baselines:
    uv run python scripts/capture_baselines.py

Nota: estos tests ignoran ``--headed`` y capturan en headless (igual que el script
de baselines y CI). Usá ``--headed`` en ``test_mobile_smoke.py`` para ver el flujo.
"""

from pathlib import Path

from conftest import DESKTOP_VIEWPORT, MOBILE_VIEWPORT, headless_chromium_page
from visual_utils import assert_matches_baseline

REPORTS = Path(__file__).resolve().parents[1] / "reports"
MAX_DIFF = 120


def _shot(page, name: str) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / name
    page.screenshot(path=path, full_page=True)
    return path


def test_home_desktop_light(playwright, app_url: str) -> None:
    with headless_chromium_page(playwright, DESKTOP_VIEWPORT) as page:
        page.goto(app_url)
        actual = _shot(page, "actual-desktop-light.png")
        assert_matches_baseline("home-desktop-light.png", actual, max_diff_pixels=MAX_DIFF)


def test_home_mobile_light(playwright, app_url: str) -> None:
    with headless_chromium_page(playwright, MOBILE_VIEWPORT) as page:
        page.goto(app_url)
        actual = _shot(page, "actual-mobile-light.png")
        assert_matches_baseline("home-mobile-light.png", actual, max_diff_pixels=MAX_DIFF)


def test_home_desktop_dark(playwright, app_url_dark: str) -> None:
    with headless_chromium_page(playwright, DESKTOP_VIEWPORT) as page:
        page.goto(app_url_dark)
        actual = _shot(page, "actual-desktop-dark.png")
        assert_matches_baseline("home-desktop-dark.png", actual, max_diff_pixels=MAX_DIFF)
