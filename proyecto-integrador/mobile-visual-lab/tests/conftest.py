"""Fixtures del lab S9: URL file:// de la app demo + helpers de viewport."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from playwright.sync_api import Page

APP_HTML = Path(__file__).resolve().parents[1] / "app" / "index.html"

# Viewport tipo teléfono (aprox. iPhone 14)
MOBILE_VIEWPORT = {"width": 390, "height": 844}
DESKTOP_VIEWPORT = {"width": 1280, "height": 720}


@pytest.fixture
def app_url() -> str:
    """URL file:// de app/index.html (sin query)."""
    return APP_HTML.as_uri()


@pytest.fixture
def app_url_broken() -> str:
    """Misma app con ?broken=1 — cambia layout a propósito (gate visual)."""
    return APP_HTML.as_uri() + "?broken=1"


@pytest.fixture
def app_url_dark() -> str:
    return APP_HTML.as_uri() + "?theme=dark"


@contextmanager
def headless_chromium_page(playwright, viewport: dict[str, int]) -> Iterator[Page]:
    """Capturas visuales siempre headless — las baselines se generan así.

    Usa el driver ``playwright`` del plugin (no ``sync_playwright()`` anidado).
    ``--headed`` afecta solo al smoke móvil.
    """
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size(viewport)
    try:
        yield page
    finally:
        browser.close()
