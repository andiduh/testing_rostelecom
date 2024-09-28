import time
import pytest
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from conftest import URL_main


# ТК63 - Форма авторизации с настройкой cookies

@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_cookie(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    try:
        popup = page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'base-modal-wrapper card-modal')]")
        )
    )
        assert popup.is_displayed()
        print("Отображается popup с cookie.")
    except TimeoutException:
        print("НЕ отображается popup с cookie.")
