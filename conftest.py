import os
import time
import pytest
from utils.driver_factory import create_driver

# Devuelve un timestamp para nombres únicos de archivos
def _timestamp():
    return time.strftime("%Y%m%d-%H%M%S")

# Asegura que exista la carpeta reports/screenshots y la devuelve
def _ensure_reports_dir():
    folder = os.path.join("reports", "screenshots")
    os.makedirs(folder, exist_ok=True)
    return folder

# Toma una captura de pantalla y la guarda en disco; devuelve la ruta o None si falla
def _take_screenshot(driver, name_prefix="screenshot"):
    try:
        folder = _ensure_reports_dir()
        filename = f"{name_prefix}-{_timestamp()}.png"
        path = os.path.join(folder, filename)
        driver.save_screenshot(path)
        return path
    except Exception:
        return None

# Añade opciones de línea de comandos para pytest
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Base URL for the application under test"
    )

# Fixture de sesión que proporciona la base URL desde las opciones de pytest
@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")

# Fixture que crea el WebDriver y lo cierra al finalizar cada test
@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")
    driver = create_driver(headless=headless)
    yield driver
    driver.quit()

# Fixture autouse que guarda capturas en caso de fallo y las asocia al nodo del test
@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    yield
    # Después de ejecutar el test, chequea el resultado
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        test_name = request.node.name
        path = _take_screenshot(driver, name_prefix=test_name)
        if path:
            # Adjunta la ruta al nodo para reporting o logging
            if not hasattr(request.node, "screenshots"):
                request.node.screenshots = []
            request.node.screenshots.append(path)

# Hook wrapper para obtener el TestReport y permitir que fixtures inspeccionen pass/fail
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # Guarda el reporte en el item (rep_setup / rep_call / rep_teardown)
    setattr(item, "rep_" + rep.when, rep)
    return rep

# Fixture auxiliar que devuelve la lista de capturas guardadas para el test actual
@pytest.fixture
def last_screenshots(request):
    return getattr(request.node, "screenshots", [])
