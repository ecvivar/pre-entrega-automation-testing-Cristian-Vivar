from utils.pages import LoginPage, InventoryPage, CartPage

def test_add_first_product_to_cart(driver):
    LoginPage(driver).open()
    LoginPage(driver).login("standard_user", "secret_sauce")
    inventory = InventoryPage(driver)
    inventory.wait_for_page()
    first_name, _ = inventory.get_first_product_name_price()
    inventory.add_first_to_cart()
    inventory.wait_for_cart_badge()
    assert inventory.get_cart_count() == "1"
    inventory.go_to_cart()
    cart = CartPage(driver)
    cart.wait_for_page()
    assert cart.has_product(first_name)
