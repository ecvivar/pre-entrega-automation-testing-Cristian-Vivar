from utils.pages import LoginPage, InventoryPage

def test_inventory_checks(driver):
    LoginPage(driver).open()
    LoginPage(driver).login("standard_user", "secret_sauce")
    inventory = InventoryPage(driver)
    inventory.wait_for_page()
    name, price = inventory.get_first_product_name_price()
    assert name != ""
    assert price.startswith("$")
