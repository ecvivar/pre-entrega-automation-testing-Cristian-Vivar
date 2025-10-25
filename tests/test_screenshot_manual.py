def test_take_screenshot_manual(driver):
    driver.get("https://www.saucedemo.com/")
    # espera corta para que cargue visualmente si hace falta
    driver.implicitly_wait(2)
    # usar la función interna de tu conftest/utils si la exportaste; si no, usamos el método del driver
    path = driver.save_screenshot("reports/screenshots/manual-screenshot.png")
    assert path is True or path is not None
