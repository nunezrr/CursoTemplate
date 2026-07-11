"""Task: CompleteCheckout — Completa el flujo de checkout en SauceDemo."""

from __future__ import annotations
from screenplay.abilities.browse_web import BrowseTheWeb
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

class CompleteCheckout:
    """Tarea de alto nivel para completar el checkout en la aplicación."""

    def __init__(self, first: str, last: str, zip_code: str) -> None:
        self._first = first
        self._last = last
        self._zip_code = zip_code

    @classmethod
    def with_info(cls, first: str, last: str, zip_code: str) -> CompleteCheckout:
        """Constructor expresivo: CompleteCheckout.with_info('John', 'Doe', '12345')."""
        return cls(first, last, zip_code)

    def perform_as(self, actor) -> None:
        """Ejecuta los pasos para completar el checkout usando las habilidades del Actor."""
        page = actor.ability_to(BrowseTheWeb).page
        
        # 1. Navega al carrito
        InventoryPage(page).go_to_cart()
        
        # 2. Hace clic en Checkout
        CartPage(page).proceed_to_checkout()
        
        # 3. Rellena los datos de envío utilizando los atributos estables data-test
        page.locator('[data-test="firstName"]').fill(self._first)
        page.locator('[data-test="lastName"]').fill(self._last)
        page.locator('[data-test="postalCode"]').fill(self._zip_code)
        
        # 4. Hace clic en continuar
        page.locator('[data-test="continue"]').click()