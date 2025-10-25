from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com/"
    USER = (By.ID, "user-name")
    PASS = (By.ID, "password")
    LOGIN = (By.ID, "login-button")
    HEADER = (By.CSS_SELECTOR, ".header_secondary_container .title, .product_label")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USER)).send_keys(username)
        self.driver.find_element(*self.PASS).send_keys(password)
        self.driver.find_element(*self.LOGIN).click()

    def wait_for_inventory(self):
        self.wait.until(EC.url_contains("/inventory.html"))
        self.wait.until(EC.visibility_of_element_located(self.HEADER))

    def get_header_text(self):
        return self.driver.find_element(*self.HEADER).text

class InventoryPage:
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".inventory_item_name")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ADD_FIRST_BTN = (By.CSS_SELECTOR, ".inventory_list .inventory_item:first-child button")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.ID, "shopping_cart_container")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_page(self):
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLES))

    def get_first_product_name_price(self):
        name = self.driver.find_element(*self.PRODUCT_TITLES).text
        price = self.driver.find_element(*self.PRODUCT_PRICES).text
        return name, price

    def add_first_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_FIRST_BTN)).click()

    def wait_for_cart_badge(self):
        self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))

    def get_cart_count(self):
        return self.driver.find_element(*self.CART_BADGE).text

    def go_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()

class CartPage:
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_page(self):
        self.wait.until(EC.visibility_of_element_located(self.CART_ITEMS))

    def has_product(self, product_name):
        items = self.driver.find_elements(*self.ITEM_NAME)
        return any(p.text == product_name for p in items)
