import time
import pytest
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from conftest import URL_ELK_WEB, URL_Onlime_WEB, URL_Start_WEB, URL_Umny_dom_WEB, URL_Kluch_WEB


# ТК64 - Форма авторизации для продукта ЕЛК Web

# Тестовые данные для Формы авторизации клиента с паролем
elements_for_test_tab_displayed_all = (
    ("div", "rt-tab", "Телефон"),
    ("div", "rt-tab", "Почта"),
    ("div", "rt-tab", "Логин"),
    ("div", "rt-tab", "Лицевой счёт"),
    )


@pytest.mark.parametrize("page_waiter_module", [URL_ELK_WEB], indirect=True)
def test_elk_web_autorization(driver_module, page_waiter_module):
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='E-mail или мобильный телефон']")
        )
    )
    address = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    # Проверка ввода номера
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_module.find_element(By.ID, value="address")  # Очистка поля
    address.click()
    driver_module.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')     # Ввод Почты
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    # Проверка ввода почты
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')
    # Переход на страницу авторизации с паролем
    standard_auth_btn_button = driver_module.find_element(By.ID, "standard_auth_btn")
    standard_auth_btn_button.click()
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    # Проверка наличия элементов
    test_results = {element: False for element in elements_for_test_tab_displayed_all}
    for tag, div, element in elements_for_test_tab_displayed_all:
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


# ТК65 - Форма регистрации для продукта ЕЛК Web


@pytest.mark.parametrize("page_waiter_function", [URL_ELK_WEB], indirect=True)
def test_elk_web_registration(driver_function, page_waiter_function):
    page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='E-mail или мобильный телефон']")
        )
    )
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.click()
    driver_function.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    kc_register = driver_function.find_element(By.ID, 'kc-register')
    kc_register.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_function.find_element(By.ID, value="address")  # Ввод почты в поле
    address.click()
    driver_function.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')


# ТК66 - Форма восстановления пароля для продукта ЕЛК Web


@pytest.mark.parametrize("page_waiter_function", [URL_ELK_WEB], indirect=True)
def test_elk_web_recovery_password(driver_function, page_waiter_function):
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация по коду')]")))
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    forgot_password = driver_function.find_element(By.ID, 'forgot_password')
    forgot_password.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
    # Ожидание загрузки страницы
    username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
    username.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    username = driver_function.find_element(By.ID, value="username")  # Очистка поля
    username.click()
    driver_function.execute_script("arguments[0].value = '';", username)
    time.sleep(1)
    username = driver_function.find_element(By.ID, value="username")  # Ввод почты в поле
    username.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе Почты сообщение об ошибке НЕ всплыло.')

# ТК67 - Форма авторизации для продукта Онлайм Web


# Тестовые данные для Формы авторизации клиента с паролем
elements_for_test_tab_displayed_Onlime = (
    ("div", "rt-tab", "Телефон"),
    ("div", "rt-tab", "Почта"),
    ("div", "rt-tab", "Логин"),
    )


@pytest.mark.parametrize("page_waiter_module", [URL_Onlime_WEB], indirect=True)
def test_onlime_web_autorization(driver_module, page_waiter_module):
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    back_to_otp_btn = driver_module.find_element(By.ID, value='back_to_otp_btn')
    back_to_otp_btn.click()
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='E-mail или мобильный телефон']")
        )
    )
    address = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.click()
    driver_module.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')
    standard_auth_btn_button = driver_module.find_element(By.ID, "standard_auth_btn")
    standard_auth_btn_button.click()
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    test_results = {element: False for element in elements_for_test_tab_displayed_Onlime}
    for tag, div, element in elements_for_test_tab_displayed_Onlime:
        try:
            checking_element = page_waiter_module.until(
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


# ТК68 - Форма регистрации для продукта Онлайм Web

@pytest.mark.parametrize("page_waiter_function", [URL_Onlime_WEB], indirect=True)
def test_onlime_web_registration(driver_function, page_waiter_function):
    page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container__title') and text()='Авторизация']")
        )
    )
    try:
        assert driver_function.find_element(By.XPATH, "//h1[contains(text(), 'Регистрация')]")
    except NoSuchElementException:
        print('Кнопка Зарегистрироваться отсутствует.')


# ТК69 - Форма восстановления пароля для продукта Онлайм Web


@pytest.mark.parametrize("page_waiter_function", [URL_Onlime_WEB], indirect=True)
def test_onlime_web_recovery_password(driver_function, page_waiter_function):
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    forgot_password = driver_function.find_element(By.ID, 'forgot_password')
    forgot_password.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
    # Ожидание загрузки страницы
    username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
    username.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    username = driver_function.find_element(By.ID, value="username")  # Очистка поля
    username.click()
    driver_function.execute_script("arguments[0].value = '';", username)
    time.sleep(1)
    username = driver_function.find_element(By.ID, value="username")  # Ввод почты в поле
    username.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')

# ТК70 - Форма авторизации для продукта Start Web


@pytest.mark.parametrize("page_waiter_module", [URL_Start_WEB], indirect=True)
def test_start_web_autorization(driver_module, page_waiter_module):
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='E-mail или мобильный телефон']")
        )
    )
    address = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_module.find_element(By.ID, value="address")  # Очистка поля
    address.click()
    driver_module.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')  # Ввод почты
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')
    standard_auth_btn_button = driver_module.find_element(By.ID, "standard_auth_btn")
    standard_auth_btn_button.click()
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    test_results = {element: False for element in elements_for_test_tab_displayed_all}
    for tag, div, element in elements_for_test_tab_displayed_all:
        try:
            checking_element = page_waiter_module.until(
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


# ТК71 - Форма регистрации для продукта Start Web


@pytest.mark.parametrize("page_waiter_function", [URL_Start_WEB], indirect=True)
def test_start_web_registration(driver_function, page_waiter_function):
    page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='E-mail или мобильный телефон']")
        )
    )
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_function.find_element(By.ID, value="address")  # Очистка поля
    address.click()
    driver_function.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')     # Ввод почты
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    kc_register = driver_function.find_element(By.ID, 'kc-register')
    kc_register.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_function.find_element(By.ID, value="address")  # Очистка  поля
    address.click()
    driver_function.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')

# ТК72 - Форма восстановления пароля для продукта Start Web


@pytest.mark.parametrize("page_waiter_function", [URL_Start_WEB], indirect=True)
def test_start_web_recovery_password(driver_function, page_waiter_function):
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация по коду')]")))
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    forgot_password = driver_function.find_element(By.ID, 'forgot_password')
    forgot_password.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
    # Ожидание загрузки страницы
    username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
    username.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    username = driver_function.find_element(By.ID, value="username")
    username.click()
    driver_function.execute_script("arguments[0].value = '';", username)
    time.sleep(1)
    username = driver_function.find_element(By.ID, value="username")
    username.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')


# ТК73 - Форма авторизации для продукта Умный дом Web


@pytest.mark.parametrize("page_waiter_module", [URL_Umny_dom_WEB], indirect=True)
def test_umny_dom_web_autorization(driver_module, page_waiter_module):
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='Мобильный телефон']")
        )
    )
    address = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    standard_auth_btn_button = driver_module.find_element(By.ID, "standard_auth_btn")
    standard_auth_btn_button.click()
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    test_results = {element: False for element in elements_for_test_tab_displayed_Onlime}
    for tag, div, element in elements_for_test_tab_displayed_Onlime:
        try:
            checking_element = page_waiter_module.until(
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


# ТК74 - Форма регистрации для продукта Умный дом Web


@pytest.mark.parametrize("page_waiter_function", [URL_Umny_dom_WEB], indirect=True)
def test_umny_dom_web_registration(driver_function, page_waiter_function):
    page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='Мобильный телефон']")
        )
    )
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    kc_register = driver_function.find_element(By.ID, 'kc-register')
    kc_register.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')


# ТК75 - Форма восстановления пароля для продукта Умный дом Web


@pytest.mark.parametrize("page_waiter_function", [URL_Umny_dom_WEB], indirect=True)
def test_umny_dom_web_recovery_password(driver_function, page_waiter_function):
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация по коду')]")))
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    forgot_password = driver_function.find_element(By.ID, 'forgot_password')
    forgot_password.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
    # Ожидание загрузки страницы
    username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
    username.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    username = driver_function.find_element(By.ID, value="username")
    username.click()
    driver_function.execute_script("arguments[0].value = '';", username)
    time.sleep(1)
    username = driver_function.find_element(By.ID, value="username")
    username.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')

# ТК76 - Форма авторизации для продукта Ключ Web


@pytest.mark.parametrize("page_waiter_module", [URL_Kluch_WEB], indirect=True)
def test_kluch_web_autorization(driver_module, page_waiter_module):
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//a[contains(@class, 'go_kab') and text()='Войти']")
        )
    )
    login = driver_module.find_element(By.XPATH, f"//a[contains(@class, 'go_kab') and text()='Войти']")
    login.click()
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='E-mail или мобильный телефон']")
        )
    )
    address = driver_module.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_module.find_element(By.ID, value="address")
    address.click()
    driver_module.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')
    body = driver_module.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_module.find_element(By.XPATH, f"//span[contains(@class, "
                                                    f"'rt-input-container__meta--error') and "
                                                    f"text()='Введите телефон в формате "
                                                    f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                    f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')
    standard_auth_btn_button = driver_module.find_element(By.ID, "standard_auth_btn")
    standard_auth_btn_button.click()
    page_waiter_module.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//h1[contains(@class, 'card-container') and text()='Авторизация']")))
    test_results = {element: False for element in elements_for_test_tab_displayed_Onlime}
    for tag, div, element in elements_for_test_tab_displayed_Onlime:
        try:
            checking_element = page_waiter_module.until(
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


# ТК74 - Форма регистрации для продукта Ключ Web

@pytest.mark.parametrize("page_waiter_function", [URL_Kluch_WEB], indirect=True)
def test_kluch_web_registration(driver_function, page_waiter_function):
    page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//a[contains(@class, 'go_kab') and text()='Войти']")
        )
    )
    login = driver_function.find_element(By.XPATH, f"//a[contains(@class, 'go_kab') and text()='Войти']")
    login.click()
    page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//span[contains(@class, 'rt-input__placeholder') and text()='E-mail или мобильный телефон']")
        )
    )
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_function.find_element(By.ID, value="address")
    address.click()
    driver_function.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    kc_register = driver_function.find_element(By.ID, 'kc-register')
    kc_register.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Регистрация')]")))
    address = driver_function.find_element(By.ID, value="address")  # Ввод номера телефона в поле
    address.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    address = driver_function.find_element(By.ID, value="address")
    address.click()
    driver_function.execute_script("arguments[0].value = '';", address)
    time.sleep(1)
    address.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    time.sleep(5)  # Пауза до появления ошибки
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе почты сообщение об ошибке НЕ всплыло.')


# ТК75 - Форма восстановления пароля для продукта Ключ Web


@pytest.mark.parametrize("page_waiter_function", [URL_Kluch_WEB], indirect=True)
def test_kluch_web_recovery_password(driver_function, page_waiter_function):
    page_waiter_function.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//a[contains(@class, 'go_kab') and text()='Войти']")
        )
    )
    login = driver_function.find_element(By.XPATH, f"//a[contains(@class, 'go_kab') and text()='Войти']")
    login.click()
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация по коду')]")))
    standard_auth_btn = driver_function.find_element(By.NAME, 'standard_auth_btn')
    standard_auth_btn.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Авторизация')]")))
    forgot_password = driver_function.find_element(By.ID, 'forgot_password')
    forgot_password.click()  # Клик на кнопку
    # Ожидание перехода на новую страницу
    page_waiter_function.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Восстановление пароля')]")))
    # Ожидание загрузки страницы
    username = driver_function.find_element(By.ID, value="username")  # Ввод номера телефона в поле
    username.send_keys('+77778889999')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе номера сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
    username = driver_function.find_element(By.ID, value="username")
    username.click()
    driver_function.execute_script("arguments[0].value = '';", username)
    time.sleep(1)
    username = driver_function.find_element(By.ID, value="username")
    username.send_keys('test@gmail.com')
    body = driver_function.find_element(By.ID, value='card-title')
    body.click()  # Снятие фокуса с поля ввода
    try:
        assert driver_function.find_element(By.XPATH, f"//span[contains(@class, "
                                                      f"'rt-input-container__meta--error') and "
                                                      f"text()='Введите телефон в формате "
                                                      f"+7ХХХХХХХХХХ или +375XXXXXXXXX, "
                                                      f"или email в формате example@email.ru']")
        print('\033[31mFAILED: \033[0mПри вводе почты сообщение об ошибке всплыло.')
    except NoSuchElementException:
        print('При вводе номера сообщение об ошибке НЕ всплыло.')
