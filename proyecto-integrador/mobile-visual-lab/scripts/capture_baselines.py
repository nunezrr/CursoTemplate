"""Captura las baselines visuales de la app sana (Sesión 9).

Corré esto UNA vez (o tras un cambio intencional de UI):

    uv run python scripts/capture_baselines.py

Escribe PNG en tests/baselines/. Esos archivos se versionan en git.
"""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app" / "index.html"
OUT = ROOT / "tests" / "baselines"

DESKTOP = {"width": 1280, "height": 720}
MOBILE = {"width": 390, "height": 844}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    uri = APP.as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_viewport_size(DESKTOP)
        page.goto(uri)
        page.screenshot(path=OUT / "home-desktop-light.png", full_page=True)

        page.goto(uri + "?theme=dark")
        page.screenshot(path=OUT / "home-desktop-dark.png", full_page=True)

        page.set_viewport_size(MOBILE)
        page.goto(uri)
        page.screenshot(path=OUT / "home-mobile-light.png", full_page=True)

        browser.close()
    print(f"Baselines escritas en {OUT}")
    for f in sorted(OUT.glob("*.png")):
        print(f"  - {f.name} ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
