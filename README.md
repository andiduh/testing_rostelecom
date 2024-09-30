# Тесты для авторизации, регистрации и восстановления пароля в Ростелеком.

## Важно !
 - Проверьте что бы все пути до файлов не содержали кириллицу

## Установка
### Linux
1. Склонируйте репозиторий и перейдите в него:
```bash
git clone git@github.com:andiduh/testing_rostelecom.git
cd testing_rostelecom
```

2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите библиотеки для работы программы:
```bash
pip install -r requirements.txt
```

### Windows
1. Установите [Python 3.12.4](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe).
Обязательно поставьте галочку около поля "Add python.exe to PATH" и нажмите "Install Now":
![Screen3](https://github.com/user-attachments/assets/c0e9fc49-9bc0-468d-8d7b-59c44aa1461f)

2. Установите GitHub Desktop:
https://desktop.github.com/download/

3. Откройте GitHub Desktop и клонируйте репозиторий:
![Screen1](https://github.com/user-attachments/assets/0969895d-6003-4be7-aad3-4800353e6ab6)

4. Откройте созданную папку при клонировни в терминале:
![Screen2](https://github.com/user-attachments/assets/d8db7103-f335-4c82-9d44-14e46b4b7721)

5. Выполните команду для разрешения политики запуска скриптов (для активации виртуального окружения):
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

6. Создайте и активируйте виртуальное окружение:
```bash
py -m venv venv
venv/Scripts/activate.ps1
```

7. Установите библиотеки для работы программы:
```bash
pip install -r requirements.txt
```

## Запуск тестов с активированным виртуальным окружением
Поскольку тесты запускаются c использованием библиотеки selenium и Chrome Driver, то необходимо скачать и установить браузер [chrome](https://www.google.com/intl/ru_ru/chrome/).

Затем активировать виртуальное окружение в Windows:
```bash
venv/Scripts/activate.ps1
```
или в Linux:
Активация виртуального окружения (Linux):
```bash
source venv/bin/activate
```

Затем запустите pytest:
```bash
pytest -v -s
```

## Если chrome не установлен и вы не планируете его устанавливать, есть алтернативный путь:
Скачать и разархивировать в отдельную папку сhromedriver:
- [Windows (64 bit)](https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/win64/chromedriver-win64.zip)
- [Windows (32 bit)](https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/win32/chromedriver-win32.zip)

![image](https://github.com/user-attachments/assets/1ffc6d06-6a99-4a5a-b013-88524f447d2f)

Далее с активированным виртуальным окружением нужно запустить pytest с указанием пути до этого драйвера (важно что бы в пути до chrome driver не было кириллицы), например:
Windows
```bash
pytest --driver-path 'C:\path\to\chrome\driver\chromedriver.exe'
```
## Технологии

- ![Python](https://img.shields.io/badge/python-3.12.4-purple)
- ![Pytest](https://img.shields.io/badge/pytest-8.3.3-green)
- ![Selenium](https://img.shields.io/badge/selenium-4.25.0-blue)

## Описание тестов:
### autorization_with_password_test.py
1. - `test_tab_displayed_autorization_with_password`: проверка наличия элементов на странице авторизации с паролем.
   - `test_input_and_tab_switching_autorization_with_password`: проверка автоматической активации таба при вводе соответствующего значения в поле username (невозможно проверить смену таба на Лицевой счет, так как отсутствуют требования к данному полю).
   - `test_active_tab_autorization_with_password`: проверка того, что таб Номер является активным по умолчанию (проверка происходит через таб Телефон).
2. `test_correct_authorization_with_number`: проверка авторизации клиента по Номеру телефона при вводе корректной связки Номер+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
3. `test_incorrect_authorization_with_number_and_wrong_password`: проверка Ошибки при авторизации клиента по Номеру телефона при вводе НЕкорректной связки Номер+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
4. `test_incorrect_authorization_with_incorrect_number`: проверка Ошибки при авторизации клиента по Номеру телефона при вводе НЕкорректного Номера.
5. `test_correct_authorization_with_email`: проверка Авторизации клиента по Почте при вводе корректной связки Почта+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
6. `test_incorrect_authorization_with_email_and_wrong_password`: проверка Ошибки при авторизации клиента по Почте при вводе НЕкорректной связки Почта+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
7. `test_incorrect_authorization_with_incorrect_email`: проверка Ошибки при авторизации клиента по Почте при вводе НЕкорректной Почты.
8. `test_correct_authorization_with_login`: Авторизация клиента по Логину при вводе корректной связки Логин+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
9. `test_incorrect_authorization_with_login_and_wrong_password`: Ошибка при авторизации клиента по Логину при вводе НЕкорректной связки Логин+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
10. `test_incorrect_authorization_with_incorrect_login`: Ошибка при авторизации клиента по Логину при вводе НЕкорректного Логина. **Тест закомментирован, так как нет возможности проверить появление ошибки из-за отсутствия требрваний к значению Логина.**
11. `test_correct_authorization_with_licevoy_schet`: Авторизация клиента по Лицевому счету при вводе корректной связки Логин+Пароль - тест не активен, т.к. нет доступа к лицевому счету.
12. `test_incorrect_authorization_with_licevoy_schet_and_wrong_password`: Ошибка при авторизации клиента по Лицевому счету при вводе НЕкорректной связки Логин+Пароль - тест не активен, т.к. нет доступа к лицевому счету.
13. `test_incorrect_authorization_with_incorrect_licevoy_schet`: Ошибка при авторизации клиента по Лицевому счету при вводе НЕкорректного Лицевого счета - тест не активен, т.к. нет доступа к лицевому счету.
### autorization_with_code_test.py
14. `test_element_displayed_autorization_with_code`: проверка наличия элементов на странице авторизации с кодом. Тест проводится для двух URL, так как по ссылке, предсталвенной в документе отсутствует кнопка "Войти по временному коду". Данная кнопка присутствует только по прямым ссылкам с продуктов ЕЛК WEB и т.д.
15. `test_authorization_with_phone_for_new_user`: Авторизация НОВОГО клиента по Временному коду с помощью Номера телефона. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). Для авторизации по коду необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
16. `test_incorrect_authorization_with_code_and_incorrect_phone`: Ошибка при авторизации клиента по Временному коду с помощью Номера телефона, введенного НЕкорректно. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
17. `test_authorization_with_email_for_new_user`: Авторизация НОВОГО клиента по Временному коду с помощью Почты. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). Для авторизации по коду необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
18. `test_incorrect_authorization_with_code_and_incorrect_email`: Ошибка при авторизации клиента по Временному коду с помощью Почты, введенной НЕкорректно. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
19. `test_authorization_with_code_and_change_phone`: Изменение Номера телефона при Авторизации клиента по Временному коду с помощью Номера телефона. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). Для авторизации по коду необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
20. `test_authorization_with_code_and_change_email`: Изменение Почты при Авторизации клиента по Временному коду с помощью Почты. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). Для авторизации по коду необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
21. `test_incorrect_authorization_with_wrong_code_and_correct_phone`: Ошибка при авторизации клиента по Временному коду с помощью Номера телефона и НЕверным значением Кода подтверждения. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
22. `test_authorization_with_resend_code_and_correct_phone`: Получение нового Кода подтверждения с помощью Номера телефона. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). В тесте есть пауза на 123 секунды - для формирования нового кода.
23. `test_incorrect_authorization_with_wrong_code_and_correct_email`: Ошибка при авторизации клиента по Временному коду с помощью Почты и НЕверным значением Кода подтверждения. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15).
24. `test_authorization_with_resend_code_and_correct_email`: Получение нового Кода подтверждения с помощью Почты. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). В тесте есть пауза на 123 секунды - для формирования нового кода.
25. `test_authorization_with_phone`: Авторизация СУЩЕСТВУЮЩЕГО клиента по Временному коду с помощью Номера телефона. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). Для авторизации по коду необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
26. `test_authorization_with_email`: Авторизация СУЩЕСТВУЮЩЕГО клиента по Временному коду с помощью Почты. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы`: time.sleep(15). Для авторизации по коду необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
### password_recovery_test.py
27. `test_form_of_recovery_password`: Проверка элементов на странице Восстановления пароля.
28. `test_recovery_password_with_phone`: Восстановление пароля клиента по Номеру телефона. При восстановлении пароля есть поле капча и поле ввода кода, которые необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
29. `test_error_recovery_password_witn_phone_and_wrong_code`: Ошибка при восстановлении пароля клиента по Номеру телефона при НЕверно введенном коде подтвержденияю. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
30. `test_error_recovery_password_with_phone_and_timeout_code`: Ошибка при восстановлении пароля клиента по Номеру телефона при вводе Кода подтверждения с истекшим временем ожидания. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
31. `test_recovery_password_with_phone_and_resend_code`: Получение повторного кода при восстановлении пароля клиента по Номеру телефона. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
32. `test_recovery_password_with_phone_and_reset_cancel`: Нажатие на кнопку "Вернуться назад" при восстановлении пароля клиента по номеру телефона приводит на страницу ввода контактных данных. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
33. `test_error_recovery_password_with_phone_and_incorrect_code`: Ошибка при восстановлении пароля клиента по Номеру телефона при НЕкорректно введенном коде подтверждения. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
34. `test_error_recovery_password_with_phone_and_wrong_password`: Ошибка при восстановлении пароля клиента по Номеру телефона при создании нового пароля НЕсогласно парольной политике. При восстановлении пароля есть поле капча и поле ввода кода, которые необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
35. `test_error_recovery_password_with_phone_and_repeat_pwd`: Ошибка при восстановлении пароля клиента по Номеру телефона при создании нового пароля, совпадающего с любым из трех предыдущих паролей. При восстановлении пароля есть поле капча и поле ввода кода, которые необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
36. `test_recovery_password_with_email`: Восстановление пароля клиента по Почте. При восстановлении пароля есть поле капча и поле ввода кода, которые необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
37. `test_error_recovery_password_with_email_and_wrong_code`: Ошибка при восстановлении пароля клиента по Почте при НЕверно введенном коде подтверждения. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
38. `test_error_recovery_password_with_email_and_timeout_code`: Ошибка при восстановлении пароля клиента по Почте при вводе Кода подтверждения с истекшим временем ожидания. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
39. `test_recovery_password_with_email_and_resend_code`: Получение повторного кода при восстановлении пароля клиента по Почте. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
40. `test_recovery_password_with_email_and_reset_cancel`: Нажатие на кнопку "Вернуться назад" при восстановлении пароля клиента по Почте приводит на страницу ввода контактных данных. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
41. `test_error_recovery_password_with_email_and_incorrect_code`: Ошибка при восстановлении пароля клиента по Почте при НЕкорректно введенном коде подтверждения. При восстановлении пароля есть поле капча, которое необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
42. `test_error_recovery_password_with_email_and_wrong_password`: Ошибка при восстановлении пароля клиента по Почте при создании нового пароля НЕсогласно парольной политике. При восстановлении пароля есть поле капча и поле ввода кода, которые необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
43. `test_error_recovery_password_with_email_and_repeat_pwd`: Ошибка при восстановлении пароля клиента по Почте при создании нового пароля, совпадающего с любым из трех предыдущих паролей. При восстановлении пароля есть поле капча и поле ввода кода, которые необходимо вводить вручную. **Тест закомментирован, так как не является полностью автоматизированным.**
### registration_test.py
44. `test_form_of_registration`: Проверка элементов на странице Регистрации.
45. `test_error_of_registration_with_incorrect_name`: Ошибка при регистрации с НЕкорректно заполненным полем Имя.
46. `test_error_of_registration_with_incorrect_surname`: Ошибка при регистрации с НЕкорректно заполненным полем Фамилия.
47. `test_error_of_registration_with_incorrect_phone`: Ошибка при регистрации с НЕкорректно заполненным полем Номер телефона.
48. `test_error_of_registration_with_incorrect_email`: Ошибка при регистрации с НЕкорректно заполненным полем Почта.
49. `test_error_of_registration_with_incorrect_password`: Ошибка при регистрации с НЕкорректно заполненным полем Пароль.
50. `test_error_of_registration_with_incorrect_password_confirm`: Ошибка при регистрации с НЕсовпадающими полями Пароль и Подтверждение пароля.
51. `test_registration_with_used_email`: Попытка регистрации на уже имеющуюся УЗ по Почте.
52. `test_registration_with_used_phone`: Попытка регистрация на уже имеющуюся УЗ по Номеру телефона.
53. `test_registration_error_with_phone_and_incorrect_code`: Ошибка при регистрации по Номеру телефона при НЕкорректно введенном Коде подтверждения.
54. `test_registration_error_with_email_and_incorrect_code`: Ошибка при регистрации по Почте при НЕкорректно введенном Коде подтверждения.
55. `test_registration_error_with_email_and_timeout_code`: Ошибка при регистрации по Почте при введенном Коде подтверждения с истекшим временем ожидания. В тесте есть пауза на 123 секунды - для формирования нового кода.
56. `test_registration_error_with_phone_and_timeout_code`: Ошибка при регистрации по Номеру телефона при введенном Коде подтверждения с истекшим временем ожидания. В тесте есть пауза на 123 секунды - для формирования нового кода.
57. `test_registration_with_email_and_resend_code`: Получение повторного кода при регистрации по Почте. В тесте есть пауза на 123 секунды - для формирования нового кода.
58. `test_registration_with_phone_and_resend_code`: Получение повторного кода при регистрации по Номеру. В тесте есть пауза на 123 секунды - для формирования нового кода.
59. `test_registration_with_changed_email`: Изменение почты через Кнопку "Изменить почту" при регистрации по Почте.
60. `test_registration_with_changed_phone`: Изменение номера через Кнопку "Изменить номер" при регистрации по Номеру телефона.
61. `test_registration_with_phone`: Регистрация по Номеру телефона. Для регистрации необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
62. `test_registration_with_email`: Регистрация по Почте. Для регистрации необходимо ввести код, отправленный пользователю вручную, так как доступа к бэку для оформления автотеста нет, поэтому установлена пауза в тесте в 60 секунд, чтобы тестировщик смог ввести код руками на странице. **Тест закомментирован, так как не является полностью автоматизированным.**
### cookie_test.py
63. `test_cookie`: Форма авторизации с настройкой cookies.
### products_form_test.py
64. `test_elk_web_autorization`: Форма авторизации для продукта ЕЛК Web.
65. `test_elk_web_registration`: Форма регистрации для продукта ЕЛК Web.
66. `test_elk_web_recovery_password`: Форма восстановления пароля для продукта ЕЛК Web.
67. `test_onlime_web_autorization`: Форма авторизации для продукта Онлайм Web.
68. `test_onlime_web_registration`: Форма регистрации для продукта Онлайм Web.
69. `test_onlime_web_recovery_password`: Форма восстановления пароля для продукта Онлайм Web.
70. `test_start_web_autorization`: Форма авторизации для продукта Start Web.
71. `test_start_web_registration`: Форма регистрации для продукта Start Web.
72. `test_start_web_recovery_password`: Форма восстановления пароля для продукта Start Web.
73. `test_umny_dom_web_autorization`: Форма авторизации для продукта Умный дом Web.
74. `test_umny_dom_web_registration`: Форма регистрации для продукта Умный дом Web.
75. `test_umny_dom_web_recovery_password`: Форма восстановления пароля для продукта Умный дом Web.
76. `test_kluch_web_autorization`: Форма авторизации для продукта Ключ Web.
77. `test_kluch_web_registration`: Форма регистрации для продукта Ключ Web.
78. `test_kluch_web_recovery_password`: Форма восстановления пароля для продукта Ключ Web.
