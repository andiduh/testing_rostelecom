import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

# URL страниц и продуктов
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
URL_ELK_WEB = 'https://lk.rt.ru/'
URL_Onlime_WEB = 'https://my.rt.ru/'
URL_Start_WEB = 'https://start.rt.ru/'
URL_Umny_dom_WEB = 'https://lk.smarthome.rt.ru/'
URL_Kluch_WEB = 'https://key.rt.ru/'

# Путь к файлу chromedriver.exe по умолчанию
default_chrome_driver_path = ('C:\chromedriver-win64\chromedriver.exe')


def driver(request):
    # Получаем путь к chromedriver, переданный через параметр --driver-path при запуске тестов
    driver_path = request.config.getoption("--driver-path")
    # Если путь к chromedriver был передан, используем его, иначе используем путь по умолчанию
    chrome_driver_path = driver_path if driver_path else default_chrome_driver_path
    # Создаем объект Service, который управляет процессом chromedriver
    # Передаем путь к исполняемому файлу chromedriver
    service = Service(chrome_driver_path)
    # Создаем объект Options для настройки параметров запуска браузера Chrome.
    options = Options()
    # Добавляем опцию, чтобы браузер открывался в максимизированном окне
    options.add_argument('--start-maximized')
    # Инициализируем WebDriver с переданной службой Service и параметрами Options
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    # После завершения тестов, закрываем браузер и завершаем процесс chromedriver
    driver.quit()


def pytest_addoption(parser):
    # Добавляет опцию командной строки --driver-path для передачи пути к исполняемому файлу ChromeDriver.
    parser.addoption("--driver-path", action="store", help="Path to ChromeDriver executable")


@pytest.fixture(scope="module")
def driver_module(request):
    # Фикстура с областью видимости "module"; создает драйвер один раз для всех тестов в модуле.
    yield from driver(request)


@pytest.fixture(scope="function")
def driver_function(request):
    # Фикстура с областью видимости "function"; создает драйвер для каждого теста.
    yield from driver(request)


@pytest.fixture(scope="module")
def page_waiter_module(driver_module, request):
    # Фикстура, использующая драйвер с областью видимости "module"; ожидает загрузку страницы.
    driver_module.get(request.param)  # Переход к указанному URL
    yield WebDriverWait(driver_module, 10)  # Создает ожидание до 10 секунд


@pytest.fixture(scope="function")
def page_waiter_function(driver_function, request):
    # Фикстура, использующая драйвер с областью видимости "function"; ожидает загрузку страницы для каждого теста.
    driver_function.get(request.param)  # Переход к указанному URL
    yield WebDriverWait(driver_function, 10)  # Создает ожидание до 10 секунд
