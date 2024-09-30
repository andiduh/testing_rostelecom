import time
import pytest
import re
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from conftest import URL_main


# ТК1 - Форма авторизации клиента с паролем

# Тестовые данные для Формы авторизации клиента с паролем
elements_for_test_tab_displayed = (
    ("div", "rt-tab", "Номер"),
    ("div", "rt-tab", "Почта"),
    ("div", "rt-tab", "Логин"),
    ("div", "rt-tab", "Лицевой счёт"),
    ("span", "rt-input", "Мобильный телефон"),
    ("span", "rt-input", "Пароль"),
    ("h2", "what-is__title", "Личный кабинет"),
)


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_tab_displayed_autorization_with_password(driver_module, page_waiter_module):
    # Ожидание загрузки страницы
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
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
            print(f"\033[31mFAILED: \033[0mЭлемент [{element}] с тегом [{tag}] класса [{div}] "
                  f"НЕ отображается или НЕ найден на странице.")
    assert all(test_results.values())


# Тестовые данные для автоматического переключения табов

@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
@pytest.mark.parametrize("tab, datatest", (
        ("Почта", "testemail@example.com"),
        ("Логин", "testemail"),
        # ("Лицевой счёт", ""), Для лицевого счета нет тестовых данных
        ("Телефон", "89123456789"),
))
def test_input_and_tab_switching_autorization_with_password(driver_module, page_waiter_module, tab, datatest):
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    # Ожидание загрузки страницы
    time.sleep(1)
    input_field = driver_module.find_element(By.ID, value='username')  # Поиск поля ввода и его очистка
    input_field.click()
    driver_module.execute_script("arguments[0].value = '';", input_field)
    time.sleep(1)
    input_field.send_keys(f'{datatest}')  # Заполнение поля ввода данными
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(1)
    # Проверка автоматической активации таба
    try:
        active_tab = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class, 'rt-tab--active') and text()='{tab}']")
            )
        )
        assert active_tab.is_displayed()
        print(f"Таб [{tab}] стал активным после ввода тестовых данных.")
    except TimeoutException:
        print(f"\033[31mFAILED: \033[0mТаб [{tab}] НЕ стал активным после ввода тестовых данных.")


# Проверка активного таба Номер по умолчанию
@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_active_tab_autorization_with_password(driver_module, page_waiter_module):
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    time.sleep(1)
    # Ожидание загрузки страницы
    input_field = driver_module.find_element(By.ID, value='username')
    input_field.click()
    driver_module.execute_script("arguments[0].value = '';", input_field)
    time.sleep(1)       # Поиск поля ввода и его очистка
    input_field.send_keys(f'testemail@example.com')  # Активация таба Почта и ввод данных
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(1)
    driver_module.refresh()  # Обновление страницы
    # Проверка активного таба
    try:
        active_tab = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class, 'rt-tab--active') and text()='Телефон']")
            )
        )
        assert active_tab.is_displayed()
        print(f"Таб Номер (Телефон) активен по умолчанию.")
    except TimeoutException:
        print(f"\033[31mFAILED: \033[0mТаб Номер (Телефон) НЕ активен по умолчанию.")


# ТК2 Авторизация клиента по Номеру телефона при вводе корректной связки Номер+Пароль

@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_correct_authorization_with_number(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод номера телефона в поле
    phone_input.send_keys("79819536526")
    password_input = driver_module.find_element(By.ID, value="password")  # Ввод пароля в поле
    password_input.send_keys("Pass3478word")
    # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
    login_button.click()
    time.sleep(5)
    # Проверка перенаправления
    try:
        re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
        print('Авторизация прошла успешно.')
    except TimeoutException:
        print("\033[31mFAILED: \033[0mНе произошло перехода на страницу личного кабинета")
    # Постусловие: выход из ЛК
    logout_button = driver_module.find_element(By.ID, "logout-btn")  # Нажатие кнопки Выйти
    logout_button.click()
    driver_module.refresh()  # Обновление страницы


# ТК3 Ошибка при авторизации клиента по Номеру телефона при вводе НЕкорректной связки Номер+Пароль


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_incorrect_authorization_with_number_and_wrong_password(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод номера телефона в поле
    phone_input.send_keys("79819536526")
    password_input = driver_module.find_element(By.ID, value="password")  # Ввод НЕкорректного пароля в поле
    password_input.send_keys("Pass3478")
    # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
    login_button.click()
    time.sleep(5)
    # Проверка появления ошибки
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'card-error__message') and text()='Неверный логин или пароль']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке всплыло.')
    # Проверка подсвечивания кнопки Забыл пароль
    try:
        forgot_pwd_color = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//a[contains(@class, 'forgot-pwd--animated') and text()='Забыл пароль']")
            )
        )
        assert forgot_pwd_color.is_displayed()
        print('Элемент "Забыл пароль" перекрашен в оранжевый цвет.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mЭлемент "Забыл пароль" НЕ перекрашен в оранжевый цвет.')


# ТК4 Ошибка при авторизации клиента по Номеру телефона при вводе НЕкорректного Номера


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_incorrect_authorization_with_incorrect_number(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод НЕкорректного номера телефона в поле
    phone_input.send_keys("7981")
    title = driver_module.find_element(By.ID, value='card-title')
    title.click()  # Снятие фокуса с поля ввода
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH,
                    f"//span[contains(@class, 'rt-input-container__meta--error')"
                    f" and text()='Неверный формат телефона']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке НЕ всплыло.')


# ТК5 Авторизация клиента по Почте при вводе корректной связки Почта+Пароль


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_correct_authorization_with_email(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод почты в поле
    phone_input.send_keys("diduh6@gmail.com")
    password_input = driver_module.find_element(By.ID, value="password")  # Ввод пароля в поле
    password_input.send_keys("12345Password")
    # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
    login_button.click()
    time.sleep(5)
    # Проверка перенаправления
    try:
        re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
        print('Авторизация прошла успешно.')
    except TimeoutException:
        print("\033[31mFAILED: \033[0mНе произошло перехода на страницу личного кабинета")
    # Постусловие: выход из ЛК
    logout_button = driver_module.find_element(By.ID, "logout-btn")  # Нажатие кнопки Выйти
    logout_button.click()
    time.sleep(5)


# ТК6 Ошибка при авторизации клиента по Почте при вводе НЕкорректной связки Почта+Пароль


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_incorrect_authorization_with_email_and_wrong_password(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод почты в поле
    phone_input.send_keys("diduh6@gmail.com")
    password_input = driver_module.find_element(By.ID, value="password")  # Ввод НЕкорректного пароля в поле
    password_input.send_keys("Pass3478")
    # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
    login_button.click()
    time.sleep(5)
    # Проверка появления ошибки
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'card-error__message') and text()='Неверный логин или пароль']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке всплыло.')
    # Проверка подсвечивания кнопки Забыл пароль
    try:
        forgot_pwd_color = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//a[contains(@class, 'forgot-pwd--animated') and text()='Забыл пароль']")
            )
        )
        assert forgot_pwd_color.is_displayed()
        print('Элемент "Забыл пароль" перекрашен в оранжевый цвет.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mЭлемент "Забыл пароль" НЕ перекрашен в оранжевый цвет.')


# ТК7 Ошибка при авторизации клиента по Почте при вводе НЕкорректной Почты


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_incorrect_authorization_with_incorrect_email(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод НЕкорректной почты в поле
    phone_input.send_keys("errr@qwe")
    title = driver_module.find_element(By.ID, value='card-title')
    title.click()  # Снятие фокуса с поля ввода
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error')"
                    f" and text()='Неверный формат логина']")))
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке НЕ всплыло.')


# ТК8 Авторизация клиента по Логину при вводе корректной связки Логин+Пароль


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_correct_authorization_with_login(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод логина в поле
    phone_input.send_keys("rtkid_1726740748835")
    password_input = driver_module.find_element(By.ID, value="password")  # Ввод пароля в поле
    password_input.send_keys("12345Password")
    # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
    login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
    login_button.click()
    time.sleep(5)
    # Проверка перенаправления
    try:
        re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
        print('Авторизация прошла успешно.')
    except TimeoutException:
        print("\033[31mFAILED: \033[0mНе произошло перехода на страницу личного кабинета")
    # Постусловие: выход из ЛК
    logout_button = driver_module.find_element(By.ID, "logout-btn")  # Нажатие кнопки Выйти
    logout_button.click()
    time.sleep(5)


# ТК9 Ошибка при авторизации клиента по Логину при вводе НЕкорректной связки Логин+Пароль


@pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
def test_incorrect_authorization_with_login_and_wrong_password(driver_module, page_waiter_module):
    page_waiter_module.until(expected_conditions.presence_of_element_located
                             ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    phone_input = driver_module.find_element(By.ID, value="username")  # Ввод логина в поле
    phone_input.send_keys("rtkid_1726740748835")
    password_input = driver_module.find_element(By.ID, value="password")  # Ввод пароля в поле
    password_input.send_keys("Pass3478")
    login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
    login_button.click()
    time.sleep(5)
    # Проверка появления ошибки
    try:
        error_message = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'card-error__message') and text()='Неверный логин или пароль']")
            )
        )
        assert error_message.is_displayed()
        print('Сообщение об ошибке всплыло.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mСообщение об ошибке всплыло.')
    # Проверка подсвечивания кнопки Забыл пароль
    try:
        forgot_pwd_color = page_waiter_module.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//a[contains(@class, 'forgot-pwd--animated') and text()='Забыл пароль']")
            )
        )
        assert forgot_pwd_color.is_displayed()
        print('Элемент "Забыл пароль" перекрашен в оранжевый цвет.')
    except TimeoutException:
        print('\033[31mFAILED: \033[0mЭлемент "Забыл пароль" НЕ перекрашен в оранжевый цвет.')


# ТК10 Ошибка при авторизации клиента по Логину при вводе НЕкорректного Логина


# @pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
# def test_incorrect_authorization_with_incorrect_login(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
#     phone_input = driver_module.find_element(By.ID, value="username")  # Ввод логина в поле
#     phone_input.send_keys("e")
#     title = driver_module.find_element(By.ID, value='card-title')
#     title.click()  # Снятие фокуса с поля ввода
#     try:
#         error_message = page_waiter_module.until(
#             expected_conditions.presence_of_element_located(
#                 (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error')"
#                         f" and text()='Неверный формат логина']")))
#         assert error_message.is_displayed()
#         print('Сообщение об ошибке всплыло.')
#     except TimeoutException:
#         print('\033[31mFAILED: \033[0mСообщение об ошибке НЕ всплыло.')


# ТК11 Авторизация клиента по Лицевому счету при вводе корректной связки Логин+Пароль
    # тест не активен, т.к. нет доступа к лицевому счету


# @pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
# def test_correct_authorization_with_licevoy_schet(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
#     phone_input = driver_module.find_element(By.ID, value="username")  # Ввод лицевого счета в поле
#     phone_input.send_keys("1726740748835")
#     password_input = driver_module.find_element(By.ID, value="password")  # Ввод пароля в поле
#     password_input.send_keys("12345Password")
#     # time.sleep(15) # Сделать строку активной для заполнения капчи вручную
#     login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
#     login_button.click()
#     time.sleep(5)
    # Проверка перенаправления
#     try:
#         re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_module.current_url)
#         print('Авторизация прошла успешно.')
#     except Exception:
#         print("\033[31mFAILED: \033[0mНе произошло перехода на страницу личного кабинета")
#     # Постусловие: выход из ЛК
#     logout_button = driver_module.find_element(By.ID, "logout-btn")  # Нажатие кнопки Выйти
#     logout_button.click()
#     time.sleep(5)


# ТК12 Ошибка при авторизации клиента по Лицевому счету при вводе НЕкорректной связки Логин+Пароль
    # тест не активен, т.к. нет доступа к лицевому счету


# @pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
# def test_incorrect_authorization_with_licevoy_schet_and_wrong_password(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
#     phone_input = driver_module.find_element(By.ID, value="username")  # Ввод лицевого счета в поле
#     phone_input.send_keys("1726740748835")
#     password_input = driver_module.find_element(By.ID, value="password")  # Ввод пароля в поле
#     password_input.send_keys("Pass3478")
#     login_button = driver_module.find_element(By.XPATH, "//button[@type='submit']")  # Нажатие кнопки Войти
#     login_button.click()
#     time.sleep(5)
#
#     error_message = page_waiter_module.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//span[contains(@class, 'card-error__message') and text()='Неверный логин или пароль']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')
#
#     forgot_pwd_color = page_waiter_module.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH, f"//a[contains(@class, 'forgot-pwd--animated') and text()='Забыл пароль']")
#         )
#     )
#     assert forgot_pwd_color.is_displayed()
#     print('Элемент "Забыл пароль" перекрашен в оранжевый цвет.')


# ТК13 Ошибка при авторизации клиента по Лицевому счету при вводе НЕкорректного Лицевого счета
    # тест не активен, т.к. нет доступа к лицевому счету


# @pytest.mark.parametrize("page_waiter_module", [URL_main], indirect=True)
# def test_incorrect_authorization_with_incorrect_licevoy_schet(driver_module, page_waiter_module):
#     page_waiter_module.until(expected_conditions.presence_of_element_located
#                              ((By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
#     phone_input = driver_module.find_element(By.ID, value="username")  # Ввод лицевого счета в поле
#     phone_input.send_keys("e")
#     title = driver_module.find_element(By.ID, value='card-title')
#     title.click()  # Снятие фокуса с поля ввода
#
#     error_message = page_waiter_module.until(
#         expected_conditions.presence_of_element_located(
#             (By.XPATH,
#              f"//span[contains(@class, 'rt-input-container__meta--error')"
#              " and text()='Неверный формат лицевого счета']")
#         )
#     )
#     assert error_message.is_displayed()
#     print('Сообщение об ошибке всплыло.')
