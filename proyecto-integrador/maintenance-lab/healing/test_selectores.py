"""DEMO Bloque C: selector FRÁGIL vs selector ROBUSTO ante un rediseño.

Historia: escribimos los tests contra la versión 1 de la página. Meses después,
el equipo de front hace un rediseño (versión 2): cambian ids y clases, pero para
el usuario la página hace lo mismo. ¿Cuáles de nuestros tests sobreviven?

Los tests de este archivo corren contra `app_v2.html` (la página YA rediseñada).

Correlo así:
    uv run pytest healing/test_selectores.py -v

No está en `tests/`, así que no entra en la suite oficial ni en el mutation
testing. Es material de demostración.

La lección (recomendación 2026): la mejor "autorreparación" es no romperse. Un
selector por ROL + TEXTO visible sobrevive cambios de DOM que destruyen a los
selectores por id/clase. El auto-healing (Healenium en Selenium; capas de IA en
Playwright) es la RED de seguridad para lo que igual se rompa, no el plan A.
"""

from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

PAGINA_REDISENADA = (Path(__file__).resolve().parent / "app_v2.html").as_uri()


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()
        pg.goto(PAGINA_REDISENADA)
        yield pg
        browser.close()


# ─────────────────────────────────────────────────────────────────────────────
# SELECTOR FRÁGIL: dependía de id="login-btn", que el rediseño eliminó.
# Este test se ROMPE con la v2 → DEBE salir FAILED. No lo tapamos con xfail:
# si encuentra un fallo, el suite tiene que fallar (mismo criterio que el gate).
# xfail/skipif se explican en teoría; no se usan aquí para esconder rojo.
# ─────────────────────────────────────────────────────────────────────────────
def test_login_selector_fragil(page):
    page.locator("#login-btn").click(timeout=2000)


# ─────────────────────────────────────────────────────────────────────────────
# SELECTOR ROBUSTO: por ROL + TEXTO visible. No le importa el id ni la clase;
# le importa lo que el usuario ve: un botón que dice "Ingresar". Sobrevive.
# ─────────────────────────────────────────────────────────────────────────────
def test_login_selector_robusto(page):
    page.get_by_role("button", name="Ingresar").click(timeout=2000)
