import os
import time
import pytest
from utils.driver_factory import create_driver

def _timestamp():
    return time.strftime("%Y%m%d-%H%M%S")

def _ensure_reports_dir():
    folder = os.path.join("reports", "screenshots")
    os.makedirs(folder, exist_ok=True)
    return folder

def _take_screenshot(driver, name_prefix="screenshot"):
    try:
        folder = _ensure_reports_dir()
        filename = f"{name_prefix}-{_timestamp()}.png"
        path = os.path.join(folder, filename)
        driver.save_screenshot(path)
        return path
    except Exception:
        return None

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

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")
    driver = create_driver(headless=headless)
    yield driver
    driver.quit()

# Fixture that ensures screenshots on failure and exposes helper functions
@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    yield
    # after the test runs, check result
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        test_name = request.node.name
        path = _take_screenshot(driver, name_prefix=test_name)
        if path:
            # attach path to node for reporting or logging
            if not hasattr(request.node, "screenshots"):
                request.node.screenshots = []
            request.node.screenshots.append(path)

# Hook to add test report attributes so fixtures can inspect pass/fail
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

# Optional: provide a small helper fixture to access last screenshots in a test
@pytest.fixture
def last_screenshots(request):
    return getattr(request.node, "screenshots", [])
