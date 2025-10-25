import os
import time
import pytest

def take_screenshot(driver, name_prefix="screenshot"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder = os.path.join("reports", "screenshots")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name_prefix}-{timestamp}.png")
    driver.save_screenshot(path)
    return path

# conftest-like fixture (copiar en conftest.py)
import pytest
from utils.driver_factory import create_driver

@pytest.fixture
def driver(request):
    drv = create_driver(headless=False)
    yield drv
    if request.node.rep_call.failed:
        try:
            take_screenshot(drv, name_prefix=request.node.name)
        except Exception:
            pass
    drv.quit()

# hook para marcar resultado y permitir screenshot en teardown
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
