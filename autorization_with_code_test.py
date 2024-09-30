import time
import pytest
import re
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from conftest import URL_main, URL_autorization_with_code


# ТК14 - Форма авторизации клиента по временному коду

# Тестовые данные для Формы авторизации клиента с кодом
elements_for_test_tab_displayed = (
    ("button", "rt-btn", " Войти с паролем "),
    ("p", "card-container__desc", "Укажите почту или номер телефона, "
                                  "на которые необходимо отправить код подтверждения"),
    ("span", "rt-input", "E-mail или мобильный телефон"),
    ("button", "rt-btn", " Получить код "),
)


@pytest.mark.parametrize("page_waiter_module", [URL_main, URL_autorization_with_code], indirect=True)
def test_element_displayed_autorization_with_code(driver_module, page_waiter_module):
    # Ожидание загрузки страницы
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.ID, "card-title")))
    test_results = {element: False for element in elements_for_test_tab_displayed}
    # Проверка наличия элементов на странице
    for tag, div, element in elements_for_test_tab_displayed:
        try:
            checking_element = page_waiter_module.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, f"//{tag}[contains(@class, '{div}') and text()='{element}']")
                )
            )
        except TimeoutException:
            pass
        else:
            test_results[(tag, div, element)] = True if checking_element.is_displayed() else False
        if test_results[(tag, div, element)]:
            print(f"Элемент [{element}] с тегом [{tag}] класса [{div}] отображается на странице.")
        else:
            print(f"\033[31mFAILED: \033[0mЭлемент [{element}] с тегом [{tag}] "
                  f"класса [{div}] НЕ отображается или НЕ найден на странице.")
    assert all(test_results.values())


# ТК15 - Авторизация НОВОГО клиента по Временному коду с помощью Номера телефона


# def test_authorization_with_phone_for_new_user(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') "
#                              "and text()='Авторизация по коду']")))
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
#     phone_input.send_keys('+79819536525')
# #   time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(60) # Время для ввода кода вручную на странице
#     # Проверка перенаправления
#     try:
#         assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
#         print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
#     except AssertionError:
#         print('\033[31mFAILED: \033[0mАутентификация клиента, перенаправление клиента на '
#               'страницу из redirect_uri НЕ произошла.')


# ТК16 - Ошибка при авторизации клиента по Временному коду с помощью Номера телефона, введенного НЕкорректно


@pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
def test_incorrect_authorization_with_code_and_incorrect_phone(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация по коду']")))
    phone_input = driver_module.find_element(By.ID, value="address")  # Ввод Некорректного номера телефона в поле
    phone_input.send_keys('79865')
#   time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
    login_button.click()
    time.sleep(5)
    # Появление ошибки
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
                           f"text()='Введите телефон в формате +7ХХХХХХХХХХ или "
                           f"+375XXXXXXXXX, или email в формате example@email.ru']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке всплыло.')


# ТК17 - Авторизация НОВОГО клиента по Временному коду с помощью Почты


# @pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
# def test_authorization_with_email_for_new_user(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container')"
#                              " and text()='Авторизация по коду']")))
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
#     phone_input.send_keys('5q3e3@rustyload.com')
# #    time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(60) # Время для ввода кода вручную на странице
#     # Проверка перенаправления
#     try:
#         assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
#         print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
#     except AssertionError:
#         print('\033[31mFAILED: \033[0mАутентификация клиента, перенаправление клиента на '
#               'страницу из redirect_uri НЕ произошла.')


# ТК18 - Ошибка при авторизации клиента по Временному коду с помощью Почты, введенной НЕкорректно


@pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
def test_incorrect_authorization_with_code_and_incorrect_email(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация по коду']")))
    phone_input = driver_module.find_element(By.ID, value="address")  # Ввод НЕкорректной почты в поле
    phone_input.send_keys('@gmail.com')
#   time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
    login_button.click()
    time.sleep(5)
    # Появление ошибки
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') "
                           f"and text()='Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, "
                           f"или email в формате example@email.ru']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке всплыло.')


# ТК19 - Изменение Номера телефона при Авторизации клиента по Временному коду с помощью Номера телефона


# @pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
# def test_authorization_with_code_and_change_phone(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and "
#                              "text()='Авторизация по коду']")))
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
#     phone_input.send_keys('+79991112233')
#     # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(2)
#     change_phone_button = driver_module.find_element(By.ID, "otp-back")  # Нажатие кнопки Изменить номер
#     change_phone_button.click()
#     time.sleep(2)
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
#     phone_input.send_keys('+79991112244')
#     # time.sleep(15)  # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(60) # Время для ввода кода вручную на странице
#     # Проверка перенаправления
#     try:
#         assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
#         print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
#     except AssertionError:
#         print('\033[31mFAILED: \033[0mАутентификация клиента, перенаправление клиента на '
#               'страницу из redirect_uri НЕ произошла.')


# ТК20 - Изменение Почты при Авторизации клиента по Временному коду с помощью Почты


# @pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
# def test_authorization_with_code_and_change_email(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and "
#                              "text()='Авторизация по коду']")))
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
#     phone_input.send_keys('test123@gmail.com')
#     # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(2)
#     change_phone_button = driver_module.find_element(By.ID, "otp-back")  # Нажатие кнопки Изменить номер
#     change_phone_button.click()
#     time.sleep(2)
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
#     phone_input.send_keys('test321@gmail.com')
#     # time.sleep(15)  # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(60) # Время для ввода кода вручную на странице
#     # Проверка перенаправления
#     try:
#         assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
#         print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
#     except AssertionError:
#         print('\033[31mFAILED: \033[0mАутентификация клиента, перенаправление клиента на '
#               'страницу из redirect_uri НЕ произошла.')


# ТК21 - Ошибка при авторизации клиента по Временному коду с помощью
# Номера телефона и НЕверным значением Кода подтверждения


@pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
def test_incorrect_authorization_with_wrong_code_and_correct_phone(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация по коду']")))
    phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    phone_input.send_keys('+79865451111')
#   time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
    login_button.click()
    time.sleep(5)
    code_input = driver_module.find_element(By.ID, value="rt-code-input")  # Ввод НЕверного Кода подтверждения
    code_input.click()
    code_input.send_keys('123456')
    # Проверка появления ошибки
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
                           f"and text()='Неверный код. Повторите попытку']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке НЕ всплыло.')


# ТК22 - Получение нового Кода подтверждения с помощью Номера телефона


@pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
def test_authorization_with_resend_code_and_correct_phone(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация по коду']")))
    phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    phone_input.send_keys('+79123123137')
    # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
    login_button.click()
    time.sleep(123)  # Пауза для формирования нового кода
    element = WebDriverWait(driver_module, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "otp-resend-code"))
    )
    element.click()  # Элемент стабилен, можно кликнуть
    code_input = WebDriverWait(driver_module, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "rt-code-input"))
    )
    code_input.click()
    code_input.send_keys('123456')

    otp_code_timeout = page_waiter_module.until(expected_conditions.presence_of_element_located(
        (By.ID, 'otp-code-timeout')))
    assert otp_code_timeout.is_displayed()
    print('Код подтверждения отправлен повторно.')


# ТК23 - Ошибка при авторизации клиента по Временному коду с помощью Почты и НЕверным значением Кода подтверждения


@pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
def test_incorrect_authorization_with_wrong_code_and_correct_email(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация по коду']")))
    phone_input = driver_module.find_element(By.ID, value="address")  # Ввод почты в поле
    phone_input.send_keys('test111@gmail.com')
#   time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
    login_button.click()
    time.sleep(5)
    code_input = driver_module.find_element(By.ID, value="rt-code-input")  # Ввод Неверного Кода подтверждения в поле
    code_input.click()
    code_input.send_keys('123456')
    # Проверка появления ошибки
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
                           f"and text()='Неверный код. Повторите попытку']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке НЕ всплыло.')


# ТК24 - Получение нового Кода подтверждения с помощью Почты


@pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
def test_authorization_with_resend_code_and_correct_email(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация по коду']")))
    phone_input = driver_module.find_element(By.ID, value="address")  # Ввод почты в поле
    phone_input.send_keys('testovy@gmail.com')
    time.sleep(15)  # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
    login_button.click()
    time.sleep(123)
    element = WebDriverWait(driver_module, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "otp-resend-code"))
    )
    element.click()  # Элемент стабилен, можно кликнуть
    code_input = WebDriverWait(driver_module, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "rt-code-input"))
    )
    code_input.click()
    code_input.send_keys('123456')

    otp_code_timeout = page_waiter_module.until(expected_conditions.presence_of_element_located(
        (By.ID, 'otp-code-timeout')))
    assert otp_code_timeout.is_displayed()
    print('Код подтверждения отправлен повторно.')


# ТК25 - Авторизация СУЩЕСТВУЮЩЕГО клиента по Временному коду с помощью Номера телефона


# @pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
# def test_authorization_with_phone(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and "
#                              "text()='Авторизация по коду']")))
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
#     phone_input.send_keys('+79819536526')
# #    time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(60) # Время для ввода кода вручную на странице
#     # Проверка перенаправления
#     try:
#         assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
#         print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
#     except AssertionError:
#         print('\033[31mFAILED: \033[0mАутентификация клиента, перенаправление клиента '
#               'на страницу из redirect_uri НЕ произошла.')


# ТК26 - Авторизация СУЩЕСТВУЮЩЕГО клиента по Временному коду с помощью Почты


# @pytest.mark.parametrize("page_waiter_module", [URL_autorization_with_code], indirect=True)
# def test_authorization_with_email(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and "
#                              "text()='Авторизация по коду']")))
#     phone_input = driver_module.find_element(By.ID, value="address")  # Ввод почты в поле
#     phone_input.send_keys('diduh6@gmail.com')
# #    time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.ID, "otp_get_code")  # Нажатие кнопки Получить код
#     login_button.click()
#     time.sleep(60) # Время для ввода кода вручную на странице
#     # Проверка перенаправления
#     try:
#         assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
#         print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
#     except AssertionError:
#         print('\033[31mFAILED: \033[0mАутентификация клиента, перенаправление клиента на '
#               'страницу из redirect_uri НЕ произошла.')
