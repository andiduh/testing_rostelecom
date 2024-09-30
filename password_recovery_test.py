import time
import pytest
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from conftest import URL_main
import re

# ТК27 - Форма Восстановления пароля

# Тестовые данные для Формы авторизации клиента с паролем
elements_for_test_tab_displayed = (
        ("div", "rt-tab", "Номер"),
        ("div", "rt-tab", "Почта"),
        ("div", "rt-tab", "Логин"),
        ("div", "rt-tab", "Лицевой счёт"),
        ("span", "rt-input", "Символы"),
        ("button", "rt-btn", "Далее"),
)


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_form_of_recovery_password(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'forgot_password')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
    assert title_forgot_pwd.is_displayed()
    test_results = {element: False for element in elements_for_test_tab_displayed}
    for tag, div, element in elements_for_test_tab_displayed:
        try:
            checking_element = page_waiter_function.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, f"//{tag}[contains(@class, '{div}') and text()='{element}']")
                )  # Проверка наличия элементов на странице
            )
        except TimeoutException:
            pass
        else:
            test_results[(tag, div, element)] = True if checking_element.is_displayed() else False
        if test_results[(tag, div, element)]:
            print(f"Элемент [{element}] с тегом [{tag}] класса [{div}] отображается на странице.")
        else:
            print(f"\033[31mFAILED: \033[0mЭлемент [{element}] с тегом [{tag}] класса [{div}] "
                  f"НЕ отображается или НЕ найден на странице.")
    assert all(test_results.values())


# ТК28 - Восстановление пароля клиента по Номеру телефона


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_recovery_password_with_phone(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79320505025")
#     time.sleep(15) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     time.sleep(60) #время для ввода кода вручную
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     password_new = driver_function.find_element(By.ID, value="password-new")
#     password_new.send_keys('Tyfryrn3624')
#     password_confirm = driver_function.find_element(By.ID, value="password-confirm")
#     password_confirm.send_keys('Tyfryrn3624')
#     button_save = driver_function.find_element(By.ID, value="t-btn-reset-pass")
#     button_save.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
#     phone_input = driver_function.find_element(By.ID, value="username")  # Ввод почты в поле
#     phone_input.send_keys("+79819536526")
#     password_input = driver_function.find_element(By.ID, value="password")  # Ввод пароля в поле
#     password_input.send_keys("Tyfryrn3624")
#     time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_function.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
#     login_button.click()
#     time.sleep(5)
#     # Проверка перенаправления
#     assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_function.current_url)
#     print('Авторизация после восстановления пароля прошла успешно.')
#     logout_button = driver_function.find_element(By.ID, "logout-btn")  # Нажатие кнопки Выйти
#     logout_button.click()
#     time.sleep(5)

# ТК29 - Ошибка при восстановлении пароля клиента по Номеру телефона при НЕверно введенном коде подтверждения


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_witn_phone_and_wrong_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79819536526")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     rt_code_input.send_keys('123456')
#     try:
#         error_message = (page_waiter_function.until
#                             (expected_conditions.presence_of_element_located(
#                                 (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
#                                            f"and text()='Неверный код. Повторите попытку']")
#                                 )
#                             )
#                         )
#         assert error_message.is_displayed()
#         print("Отображается ошибка: 'Неверный код. Повторите попытку'.")
#     except TimeoutException:
#         print("\033[31mFAILED: \033[0mНЕ отображается ошибка: 'Неверный код. Повторите попытку'.")


# ТК30 - Ошибка при восстановлении пароля клиента по Номеру телефона при вводе
# Кода подтверждения с истекшим временем ожидания


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_phone_and_timeout_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79819536526")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(123)
#     rt_code_input.send_keys('123456')
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
#                        f"and text()='Время жизни кода истекло']")
#         )
#     )
#     assert error_message.is_displayed()
#     print("Отображается ошибка: 'Время жизни кода истекло'.")


# ТК31 - Получение повторного кода при восстановлении пароля клиента по Номеру телефона


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_recovery_password_with_phone_and_resend_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79819536526")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(123)
#     element = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
#         expected_conditions.presence_of_element_located((By.ID, "otp-resend-code"))
#     )
#     element.click()  # Элемент стабилен, можно кликнуть
#     code_input = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
#         expected_conditions.presence_of_element_located((By.ID, "rt-code-input"))
#     )
#     code_input.click()
#     code_input.send_keys('123456')
#     otp_code_timeout = page_waiter_function.until(expected_conditions.presence_of_element_located
#                                                 ((By.ID, 'otp-code-timeout')))
#     assert otp_code_timeout.is_displayed()
#     print('Код подтверждения отправлен повторно.')


# ТК32 - Нажатие на кнопку "Вернуться назад" при восстановлении пароля клиента
# по номеру телефона приводит на страницу ввода контактных данных


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_recovery_password_with_phone_and_reset_cancel(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79819536526")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(1)
#     reset_cancel = driver_function.find_element(By.ID, value="reset-cancel")
#     reset_cancel.click()
#     assert page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     print('Нажатие на кнопку "Вернуться назад" при восстановлении '
#           'пароля клиента по Почте приводит на страницу ввода контактных данных')


# ТК33 - Ошибка при восстановлении пароля клиента по Номеру телефона при НЕкорректно введенном коде подтверждения


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_phone_and_incorrect_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79819536526")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(1)
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     code_input = driver_function.find_element(By.ID, value="rt-code-input")  # Ввод номера телефона в поле
#     code_input.click()
#     code_input.send_keys('123456')
#
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'code-input-container__error') and "
#                        f"text()='Неверный код. Повторите попытку']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')

# ТК34 - Ошибка при восстановлении пароля клиента по Номеру телефона при
# создании нового пароля НЕсогласно парольной политике


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_phone_and_wrong_password(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79320505025")
#     time.sleep(15) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     time.sleep(60) #время для ввода кода вручную
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     password_new = driver_function.find_element(By.ID, value="password-new")
#     password_new.send_keys('123')
#     password_confirm = driver_function.find_element(By.ID, value="password-confirm")
#     password_confirm.send_keys('123')
#     button_save = driver_function.find_element(By.ID, value="t-btn-reset-pass")
#     button_save.click()
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
#                        f"text()='Длина пароля должна быть не менее 8 символов']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')


# ТК35 - Ошибка при восстановлении пароля клиента по Номеру телефона при
# создании нового пароля, совпадающего с любым из трех предыдущих паролей


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_phone_and_repeat_pwd(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("+79320505025")
#     time.sleep(15) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     time.sleep(60) #время для ввода кода вручную
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     password_new = driver_function.find_element(By.ID, value="password-new")
#     password_new.send_keys('Tyfryrn3624')
#     password_confirm = driver_function.find_element(By.ID, value="password-confirm")
#     password_confirm.send_keys('Tyfryrn3624')
#     button_save = driver_function.find_element(By.ID, value="t-btn-reset-pass")
#     button_save.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'card-error__message') and "
#                        f"text()='Этот пароль уже использовался, укажите другой пароль']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')


# ТК36 - Восстановление пароля клиента по Почте


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_recovery_password_with_email(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("diduh.an.v@gmail.com")
#     time.sleep(15) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     time.sleep(60) #время для ввода кода вручную
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     password_new = driver_function.find_element(By.ID, value="password-new")
#     password_new.send_keys('Tyfryrn3636')
#     password_confirm = driver_function.find_element(By.ID, value="password-confirm")
#     password_confirm.send_keys('Tyfryrn3636')
#     button_save = driver_function.find_element(By.ID, value="t-btn-reset-pass")
#     button_save.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
#     phone_input = driver_function.find_element(By.ID, value="username")  # Ввод почты в поле
#     phone_input.send_keys("lgh4n@rustyload.com")
#     password_input = driver_function.find_element(By.ID, value="password")  # Ввод пароля в поле
#     password_input.send_keys("Tyfryrn3636")
#     time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_function.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
#     login_button.click()
#     time.sleep(5)
#
#     # Проверка перенаправления
#     assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_function.current_url)
#     print('Авторизация прошла успешно.')
#
#     logout_button = driver_function.find_element(By.ID, "logout-btn")  # Нажатие кнопки Выйти
#     logout_button.click()
#     time.sleep(5)


# ТК37 - Ошибка при восстановлении пароля клиента по Почте при НЕверно введенном коде подтверждения


# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_email_and_wrong_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("lgh4n@rustyload.com")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     rt_code_input.send_keys('123456')
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
#                        f"and text()='Неверный код. Повторите попытку']")
#         )
#     )
#     assert error_message.is_displayed()
#     print("Отображается ошибка: 'Неверный код. Повторите попытку'.")
#
# # ТК38 - Ошибка при восстановлении пароля клиента по Почте при вводе Кода подтверждения с истекшим временем ожидания
#
#
# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_email_and_timeout_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("lgh4n@rustyload.com")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(123)
#     rt_code_input.send_keys('123456')
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
#                        f"and text()='Время жизни кода истекло']")
#         )
#     )
#     assert error_message.is_displayed()
#     print("Отображается ошибка: 'Время жизни кода истекло'.")
#
#
# # ТК39 - Получение повторного кода при восстановлении пароля клиента по Почте
#
#
# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_recovery_password_with_email_and_resend_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("lgh4n@rustyload.com")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(123)
#     element = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
#         expected_conditions.presence_of_element_located((By.ID, "otp-resend-code"))
#     )
#     element.click()  # Элемент стабилен, можно кликнуть
#     code_input = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
#         expected_conditions.presence_of_element_located((By.ID, "rt-code-input"))
#     )
#     code_input.click()
#     code_input.send_keys('123456')
#
#     otp_code_timeout = page_waiter_function.until(expected_conditions.presence_of_element_located
#                                                 ((By.ID, 'otp-code-timeout')))
#     assert otp_code_timeout.is_displayed()
#     print('Код подтверждения отправлен повторно.')
#
#
# # ТК40 - Нажатие на кнопку "Вернуться назад" при восстановлении пароля
# # клиента по Почте приводит на страницу ввода контактных данных
#
#
# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_recovery_password_with_email_and_reset_cancel(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("lgh4n@rustyload.com")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(1)
#     reset_cancel = driver_function.find_element(By.ID, value="reset-cancel")
#     reset_cancel.click()
#     assert page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     print('Нажатие на кнопку "Вернуться назад" при восстановлении '
#           'пароля клиента по Почте приводит на страницу ввода контактных данных')
#
#
# # ТК41 - Ошибка при восстановлении пароля клиента по Почте при НЕкорректно введенном коде подтверждения
#
#
# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_email_and_incorrect_code(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("lgh4n@rustyload.com")
#     time.sleep(20) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
#     time.sleep(1)
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     code_input = driver_function.find_element(By.ID, value="rt-code-input")  # Ввод номера телефона в поле
#     code_input.click()
#     code_input.send_keys('123456')
#
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'code-input-container__error') and "
#                        f"text()='Неверный код. Повторите попытку']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')
#
# # ТК42 - Ошибка при восстановлении пароля клиента по Почте при создании нового пароля НЕсогласно парольной политике
#
#
# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_email_and_wrong_password(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("lgh4n@rustyload.com")
#     time.sleep(15) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     time.sleep(60) #время для ввода кода вручную
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     password_new = driver_function.find_element(By.ID, value="password-new")
#     password_new.send_keys('123')
#     password_confirm = driver_function.find_element(By.ID, value="password-confirm")
#     password_confirm.send_keys('123')
#     button_save = driver_function.find_element(By.ID, value="t-btn-reset-pass")
#     button_save.click()
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
#                        f"text()='Длина пароля должна быть не менее 8 символов']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')
#
# # ТК43 - Ошибка при восстановлении пароля клиента по Почте при создании нового
# # пароля, совпадающего с любым из трех предыдущих паролей
#
# @pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
# def test_error_recovery_password_with_email_and_repeat_pwd(driver_function, page_waiter_function):
#     # Ожидание загрузки страницы
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'forgot_password')))  # Ожидание, пока поле ввода станет доступным
#     # Находим кнопку и кликаем на нее
#     button = driver_function.find_element(By.ID, 'forgot_password')
#     button.click()  # Клик на кнопку
#     # Ожидание перехода на новую страницу
#     title_forgot_pwd = page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
#     username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
#     username.send_keys("lgh4n@rustyload.com")
#     time.sleep(15) #время для ввода капчи вручную
#     button = driver_function.find_element(By.ID, value="reset")
#     button.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     time.sleep(60) #время для ввода кода вручную
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     password_new = driver_function.find_element(By.ID, value="password-new")
#     password_new.send_keys('Tyfryrn3636')
#     password_confirm = driver_function.find_element(By.ID, value="password-confirm")
#     password_confirm.send_keys('Tyfryrn3636')
#     button_save = driver_function.find_element(By.ID, value="t-btn-reset-pass")
#     button_save.click()
#     page_waiter_function.until(expected_conditions.presence_of_element_located(
#         (By.ID, 'card-title')))
#     error_message = page_waiter_function.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'card-error__message') and "
#                        f"text()='Этот пароль уже использовался, укажите другой пароль']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')
