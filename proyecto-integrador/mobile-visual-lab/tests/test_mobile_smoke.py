"""Smoke móvil: el flujo crítico cabe y funciona en viewport angosto (Sesión 9).

No necesita emulador Android ni Appium: Playwright emula el viewport.
El mapa Appium/Maestro queda en la teoría; este lab demuestra la idea
"mismo flujo, distinta pantalla" sin fricción de SDK.
"""

from playwright.sync_api import Page, expect

from conftest import MOBILE_VIEWPORT


def test_login_usable_en_viewport_mobile(page: Page, app_url: str) -> None:
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(app_url)

    expect(page.get_by_role("heading", name="Tienda Demo")).to_be_visible()
    expect(page.get_by_role("button", name="Ingresar")).to_be_visible()

    page.get_by_label("Correo").fill("alumno@curso.test")
    page.get_by_label("Contraseña").fill("secreto")
    page.get_by_role("button", name="Ingresar").click()

    expect(page.get_by_role("status")).to_have_text("Sesión iniciada")


def test_producto_visible_en_mobile(page: Page, app_url: str) -> None:
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(app_url)

    expect(page.get_by_role("heading", name="Auriculares QA Pro")).to_be_visible()
    expect(page.get_by_text("$89.00")).to_be_visible()
    page.get_by_role("button", name="Agregar al carrito").click()
    expect(page.get_by_role("status")).to_have_text("Producto en el carrito")
