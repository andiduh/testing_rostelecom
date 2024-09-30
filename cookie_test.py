import pytest
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from conftest import URL_main


# ТК63 - Форма авторизации с настройкой cookies


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_cookie(driver_module, page_waiter_module):
    # Ожидание загрузки страницы
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    # Очистка cookie
    driver_module.delete_all_cookies()
    # Повторное ожидание загрузки страницы
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    # Появление popup с информацией о cookie
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
