from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_checkout_sin_errores(authenticated_page):
    inventorypage = InventoryPage(authenticated_page)
    inventorypage.add_to_cart("Sauce Labs Backpack").go_to_cart()
    cartpage = CartPage(authenticated_page)
    cartpage.proceed_to_checkout()
    checkout = CheckoutPage(authenticated_page)
    checkout.fill_shipping("John", "Smith", "42003")
    assert checkout.has_no_errors()

def test_checkout_con_errores(authenticated_page):
    inventorypage = InventoryPage(authenticated_page)
    inventorypage.add_to_cart("Sauce Labs Backpack").go_to_cart()
    cartpage = CartPage(authenticated_page)
    cartpage.proceed_to_checkout()
    checkout = CheckoutPage(authenticated_page)
    checkout.fill_shipping("", "", "")
    assert checkout.has_errors()    