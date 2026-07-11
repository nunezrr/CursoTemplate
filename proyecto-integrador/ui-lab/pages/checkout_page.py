from __future__ import annotations
import re
from playwright.sync_api import Page, expect

class CheckoutPage:
    """Page Object Model for Checkout Page
    @page /checkout-step-one.html
    """
    URL = "https://www.saucedemo.com/checkout-step-one.html"
    # ============ Ini ============

    def __init__(self, page: Page) -> None:
        self.page = page
        self._first_name  = page.locator('[data-test="firstName"]')
        self._last_name  = page.locator('[data-test="lastName"]')
        self._postal_code  = page.locator('[data-test="postalCode"]')
        self._continue_btn = page.locator('[data-test="continue"]')
        self._error_msg = page.locator('[data-test="error"]')

     # ============ Actions ============
    def go_to(self) -> "CheckoutPage":
        """Navega a la URL de checkout y devuelve self (interfaz fluida)."""
        self.page.goto(self.URL)
        return self

    def fill_shipping(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutPage":
        """Rellena el formulario y hace clic en el botón de continuar."""
        self._first_name.fill(first_name)
        self._last_name.fill(last_name)
        self._postal_code.fill(postal_code)
        self._continue_btn.click()
        return self

    # ============ Assertions ============
    
    def has_no_errors(self) -> "CheckoutPage":
        """Valida que NO aparezca ningún mensaje de error en la página."""
        # El mensaje personalizado va dentro de expect(), no en el método de aserción
        expect(
            self._error_msg, 
            message="Se detectó un mensaje de error en el checkout cuando no se esperaba."
        ).not_to_be_visible()
        return self

    def has_errors(self) -> "CheckoutPage":
        """Valida que aparezca un mensaje de error en la página."""
        expect(
            self._error_msg,
            message="No se detectó ningún mensaje de error en el checkout cuando se esperaba."
        ).to_be_visible()
        return self

