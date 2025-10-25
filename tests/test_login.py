from utils.pages import LoginPage

def test_login_success(driver):
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")
    page.wait_for_inventory()
    assert "/inventory.html" in driver.current_url
    header = page.get_header_text()
    assert "Products" in header or "Swag Labs" in header
