import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

URL_main = ('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth'
       '?client_id=account_b2c'
       '&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login'
       '&response_type=code&scope=openid'
       '&state=04bb1ff5-db58-48d7-a0f2-3ff29aff2910')

URL_autorization_with_code = ('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth'
                              '?response_type=code'
                              '&scope=openid'
                              '&client_id=lk_b2c'
                              '&redirect_uri=https%3A%2F%2Flk'
                              '-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Flk.rt.ru%252F'
                              '&state=%7B%22uuid%22%3A%22EEE6B524-95C8-4DBC-A762-40610C6E9588%22%7D')
URL_ELK_WEB = ('https://lk.rt.ru/')
URL_Onlime_WEB = ('https://my.rt.ru/')
URL_Start_WEB = ('https://start.rt.ru/')
URL_Umny_dom_WEB = ('https://lk.smarthome.rt.ru/')
URL_Kluch_WEB = ('https://key.rt.ru/')
default_chrome_driver_path = ('C:\chromedriver-win64\chromedriver.exe')


def driver(request):
    driver_path = request.config.getoption("--driver-path")
    chrome_driver_path = driver_path if driver_path else default_chrome_driver_path
    service = Service(chrome_driver_path)  # Путь к chromedriver
    options = Options()
    options.add_argument('--start-maximized')  # Открывать браузер в максимизированном состоянии
    driver = webdriver.Chrome(service=service, options=options)  # Инициализация WebDriver
    yield driver  # Возвращение объекта драйвера
    driver.quit()  # После завершения тестов закрывается браузер


def pytest_addoption(parser):
    parser.addoption("--driver-path", action="store", help="Path to ChromeDriver executable")


@pytest.fixture(scope="module")
def driver_module(request):
    yield from driver(request)


@pytest.fixture(scope="function")
def driver_function(request):
    yield from driver(request)


@pytest.fixture(scope="module")
def page_waiter_module(driver_module, request):
    driver_module.get(request.param)
    yield WebDriverWait(driver_module, 10)


@pytest.fixture(scope="function")
def page_waiter_function(driver_function, request):
    driver_function.get(request.param)
    yield WebDriverWait(driver_function, 10)



