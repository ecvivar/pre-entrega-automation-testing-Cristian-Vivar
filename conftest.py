import pytest
from selenium import webdriver
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def login_in_driver(driver):
    LoginPage(driver).abrir_pagina().login_completo("standard_user","secret_sauce")
    return driver