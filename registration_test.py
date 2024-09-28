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
import re


# ТК44 - Форма Регистрации
elements_for_test_tab_displayed = (
        ("span", "rt-input", "Имя"),
        ("span", "rt-input", "Фамилия"),
        ("span", "rt-input", "Регион"),
        ("span", "rt-input", "E-mail или мобильный телефон"),
        ("span", "rt-input", "Пароль"),
        ("span", "rt-input", "Подтверждение пароля"),
        ("button", "rt-btn", "Продолжить"),
        ("a", "rt-link", "пользовательского соглашения"),
        ("a", "rt-link", "политика конфиденциальности"),
        ("h2", "what-is__title", "Личный кабинет"),
        ("p", "what-is__desc", "Персональный помощник в цифровом мире Ростелекома"),
)

# Тестовые данные для Формы авторизации клиента с паролем


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_form_of_registration(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    title_kc_register = page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
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
            print(f"Элемент [{element}] с тегом [{tag}] класса [{div}] НЕ отображается или НЕ найден на странице.")
    assert all(test_results.values())


# ТК45 - Ошибка при регистрации с НЕкорректно заполненным полем Имя


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_error_of_registration_with_incorrect_name(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input = driver_function.find_element(By.NAME, value="firstName")
    input.send_keys("Я")
    button = driver_function.find_element(By.ID, "card-title")
    button.click()
    time.sleep(2)

    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
                       f"text()='Необходимо заполнить поле кириллицей. От 2 до 30 символов.']")
        )
    )
    assert error_message.is_displayed()
    print('При некорректно введенном Имени сообщение об ошибке всплыло.')


# ТК46 - Ошибка при регистрации с НЕкорректно заполненным полем Фамилия


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_error_of_registration_with_incorrect_surname(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input = driver_function.find_element(By.NAME, value="lastName")
    input.send_keys("Я")
    button = driver_function.find_element(By.ID, "card-title")
    button.click()
    time.sleep(2)

    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
                       f"text()='Необходимо заполнить поле кириллицей. От 2 до 30 символов.']")
        )
    )
    assert error_message.is_displayed()
    print('При некорректно введенной Фамилии сообщение об ошибке всплыло.')



# ТК47 - Ошибка при регистрации с НЕкорректно заполненным полем Номер телефона


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_error_of_registration_with_incorrect_phone(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input = driver_function.find_element(By.ID, value="address")
    input.send_keys("987")
    button = driver_function.find_element(By.ID, "card-title")
    button.click()
    time.sleep(2)

    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
                       f"text()='Введите телефон в формате +7ХХХХХХХХХХ или "
                       f"+375XXXXXXXXX, или email в формате example@email.ru']")
        )
    )
    assert error_message.is_displayed()
    print('При некорректно введенном Номере сообщение об ошибке всплыло.')


# ТК48 - Ошибка при регистрации с НЕкорректно заполненным полем Почта


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_error_of_registration_with_incorrect_email(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input = driver_function.find_element(By.ID, value="address")
    input.send_keys("@hf.n")
    button = driver_function.find_element(By.ID, "card-title")
    button.click()
    time.sleep(2)

    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
                       f"text()='Введите телефон в формате +7ХХХХХХХХХХ или "
                       f"+375XXXXXXXXX, или email в формате example@email.ru']")
        )
    )
    assert error_message.is_displayed()
    print('При некорректно введенной Почте сообщение об ошибке всплыло.')


# ТК49 - Ошибка при регистрации с НЕкорректно заполненным полем Пароль


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_error_of_registration_with_incorrect_password(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input = driver_function.find_element(By.ID, value="password")
    input.send_keys("33")
    button = driver_function.find_element(By.ID, "card-title")
    button.click()
    time.sleep(2)

    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
                       f"text()='Длина пароля должна быть не менее 8 символов']")
        )
    )
    assert error_message.is_displayed()
    print('При некорректно введенном Пароле сообщение об ошибке всплыло.')


# ТК50 - Ошибка при регистрации с НЕсовпадающими полями Пароль и Подтверждение пароля


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_error_of_registration_with_incorrect_password_confirm(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("12345Password")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("12345Passwo")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(2)

    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input-container__meta--error') and "
                       f"text()='Пароли не совпадают']")
        )
    )
    assert error_message.is_displayed()
    print('При некорректно введенном Подтверждении пароля сообщение об ошибке всплыло.')


# ТК51 - Попытка регистрации на уже имеющуюся УЗ по Почте


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_used_email(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("diduh6@gmail.com")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(2)

    popup = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'base-modal-wrapper card-modal')]")
        )
    )
    assert popup.is_displayed()
    print("Отображается оповещающая форма.")

    button_submit = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'rt-btn' and text()='Войти']")
        )
    )
    assert button_submit.is_displayed()
    print("Отображается кнопка Войти")

    button_recovery_pwd = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'rt-btn' and text()=' Восстановить пароль ']")
        )
    )
    assert button_recovery_pwd.is_displayed()
    print("Отображается кнопка Восстановить пароль")

    close_popup = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'rt-btn' and text()='Выйти']")
        )
    )
    assert close_popup.is_displayed()
    print("Отображается кнопка Крестик")


# ТК52 - Попытка регистрация на уже имеющуюся УЗ по Номеру телефона


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_used_phone(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("+79819536526")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(2)

    popup = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'base-modal-wrapper card-modal')]")
        )
    )
    assert popup.is_displayed()
    print("Отображается оповещающая форма.")

    button_cancel = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'rt-btn' and text()='Отмена']")
        )
    )
    assert button_cancel.is_displayed()
    print("Отображается кнопка Отмена")

    button_registration = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'rt-btn' and text()='Зарегистрироваться']")
        )
    )
    assert button_registration.is_displayed()
    print("Отображается кнопка Зарегистрироваться")


# ТК53 - Ошибка при регистрации по Номеру телефона при НЕкорректно введенном Коде подтверждения


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_error_with_phone_and_incorrect_code(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("+79811111112")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    rt_code_input = page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'rt-code-input')))  # Ожидание, пока поле ввода станет доступным
    rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
    rt_code_input.send_keys('123456')
    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
                       f"and text()='Неверный код. Повторите попытку']")
        )
    )
    assert error_message.is_displayed()
    print("Отображается ошибка: 'Неверный код. Повторите попытку'.")


# ТК54 - Ошибка при регистрации по Почте при НЕкорректно введенном Коде подтверждения


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_error_with_email_and_incorrect_code(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("tttest111@gmail.com")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    rt_code_input = page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'rt-code-input')))  # Ожидание, пока поле ввода станет доступным
    rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
    rt_code_input.send_keys('123456')
    error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
                       f"and text()='Неверный код. Повторите попытку']")
        )
    )
    assert error_message.is_displayed()
    print("Отображается ошибка: 'Неверный код. Повторите попытку'.")


# ТК55 - Ошибка при регистрации по Почте при введенном Коде подтверждения с истекшим временем ожидания


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_error_with_email_and_timeout_code(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("tessst6@gmail.com")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'rt-code-input')))  # Ожидание, пока поле ввода станет доступным
    rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
    time.sleep(123)
    rt_code_input.send_keys('123456')
    try:
        error_message = page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
                       f"and text()='Время жизни кода истекло']")
        )
    )
        assert error_message.is_displayed()
        print("Отображается ошибка: 'Время жизни кода истекло'.")
    except TimeoutException:
        print("Ошибка: 'Время жизни кода истекло' НЕ отображается.")


# ТК56 - Ошибка при регистрации по Номеру телефона при введенном Коде подтверждения с истекшим временем ожидания


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_error_with_phone_and_timeout_code(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("+79811111114")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'rt-code-input')))  # Ожидание, пока поле ввода станет доступным
    rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
    time.sleep(123)
    rt_code_input.send_keys('123456')
    try:
        error_message = page_waiter_function.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[contains(@class, 'code-input-container__error') "
                           f"and text()='Время жизни кода истекло']")
            )
        )
        assert error_message.is_displayed()
        print("Отображается ошибка: 'Время жизни кода истекло'.")
    except TimeoutException:
        print("Ошибка: 'Время жизни кода истекло' НЕ отображается.")


# ТК57 - Получение повторного кода при регистрации по Почте


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_email_and_resend_code(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("test23@gmail.com")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'rt-code-input')))  # Ожидание, пока поле ввода станет доступным
    rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
    time.sleep(123)
    element = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "otp-resend-code"))
    )
    element.click()  # Элемент стабилен, можно кликнуть
    code_input = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "rt-code-input"))
    )
    code_input.click()
    code_input.send_keys('123456')

    otp_code_timeout = page_waiter_function.until(expected_conditions.presence_of_element_located
                                                ((By.ID, 'otp-code-timeout')))
    assert otp_code_timeout.is_displayed()
    print('Код подтверждения отправлен повторно.')


# ТК58 - Получение повторного кода при регистрации по Номеру


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_phone_and_resend_code(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("+79991122333")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'rt-code-input')))  # Ожидание, пока поле ввода станет доступным
    rt_code_input = driver_function.find_element(By.ID, 'rt-code-input')
    time.sleep(123)
    element = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "otp-resend-code"))
    )
    element.click()  # Элемент стабилен, можно кликнуть
    code_input = WebDriverWait(driver_function, 10, ignored_exceptions=[StaleElementReferenceException]).until(
        expected_conditions.presence_of_element_located((By.ID, "rt-code-input"))
    )
    code_input.click()
    code_input.send_keys('123456')

    otp_code_timeout = page_waiter_function.until(expected_conditions.presence_of_element_located
                                                ((By.ID, 'otp-code-timeout')))
    assert otp_code_timeout.is_displayed()
    print('Код подтверждения отправлен повторно.')


# ТК59 - Изменение почты через Кнопку "Изменить почту" при регистрации по Почте


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_changed_email(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("test23@gmail.com")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'otp-back')))  # Ожидание, пока поле ввода станет доступным
    otp_back = driver_function.find_element(By.ID, 'otp-back')
    otp_back.click()
    time.sleep(2)
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.click()
    driver_function.execute_script("arguments[0].value = '';", input_email)
    time.sleep(1)
    input_email.send_keys("1test234@gmail.com")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    try:
        otp_back = page_waiter_function.until(expected_conditions.presence_of_element_located
                                                  ((By.ID, 'otp-back')))
        assert otp_back.is_displayed()
    except TimeoutException:
        print('Не произошел переход на страницу ввода Кода подтверждения после изменения почты.')


# ТК60 - Изменение номера через Кнопку "Изменить номер" при регистрации по Номеру телефона


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_changed_phone(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("+79819819111")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'otp-back')))  # Ожидание, пока поле ввода станет доступным
    otp_back = driver_function.find_element(By.ID, 'otp-back')
    otp_back.click()
    time.sleep(2)
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.click()
    driver_function.execute_script("arguments[0].value = '';", input_email)
    time.sleep(1)
    input_email.send_keys("+79819819899")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(3)
    try:
        otp_back = page_waiter_function.until(expected_conditions.presence_of_element_located
                                                  ((By.ID, 'otp-back')))
        assert otp_back.is_displayed()
    except TimeoutException:
        print('Не произошел переход на страницу ввода Кода подтверждения после изменения почты.')



# ТК61 - Регистрация по Номеру телефона

@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_phone(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("+79873452323")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(60) # Время для ввода кода вручную на странице
    # Проверка перенаправления
    try:
        assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_function.current_url)
        print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
    except AssertionError:
        print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri НЕ произошла.')

# ТК62 - Регистрация по Почте


@pytest.mark.parametrize("page_waiter_function", [URL_main], indirect=True)
def test_registration_with_email(driver_function, page_waiter_function):
    # Ожидание загрузки страницы
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.ID, 'kc-register')))  # Ожидание, пока поле ввода станет доступным
    # Находим кнопку и кликаем на нее
    button = driver_function.find_element(By.ID, 'kc-register')
    button.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    input_name = driver_function.find_element(By.NAME, value="firstName")
    input_name.send_keys("Иван")
    input_surname = driver_function.find_element(By.NAME, value="lastName")
    input_surname.send_keys("Иванов")
    input_email = driver_function.find_element(By.ID, value="address")
    input_email.send_keys("8zpok@rustyload.com")
    input_password = driver_function.find_element(By.ID, value="password")
    input_password.send_keys("NewPassword1")
    input_password_confirm = driver_function.find_element(By.ID, value="password-confirm")
    input_password_confirm.send_keys("NewPassword1")
    button = driver_function.find_element(By.NAME, "register")
    button.click()
    time.sleep(60) # Время для ввода кода вручную на странице
    # Проверка перенаправления
    try:
        assert re.match(r"https://b2c\.passport\.rt\.ru/account_b2c/.+", driver_function.current_url)
        print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri.')
    except AssertionError:
        print('Аутентификация клиента, перенаправление клиента на страницу из redirect_uri НЕ произошла.')