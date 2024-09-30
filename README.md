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
Поскольку тесты запускаются c использованием библиотеки selenium, то необходимо скачать и разархивировать в отдельную папку сhromedriver:
- [Windows (64 bit)](https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/win64/chromedriver-win64.zip)
- [Windows (32 bit)](https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/win32/chromedriver-win32.zip)

![image](https://github.com/user-attachments/assets/1ffc6d06-6a99-4a5a-b013-88524f447d2f)

Далее с активированным виртуальным окружением нужно запустить pytest с указанием пути до этого драйвера:

Активация виртуального окружения (Windows):
```bash
venv/Scripts/activate.ps1
```

Активация виртуального окружения (Linux):
```bash
venv/Scripts/activate.ps1
```

Запуск pytest:
```bash
pytest
```

Папка с драйвером по умолчанию в windows: `C:\chromedriver-win64\chromedriver.exe`, в linux `~/chromedriver`. Если будет другая, то pytest нужно запустить с указанием пути до `chromedriver.exe`.

Windows
```bash
pytest --driver-path 'C:\path\to\chrome\driver\chromedriver.exe'
```

Linux
```bash
pytest --driver-path '~/path/to/chromedriver'
```

## Технологии

- ![Python](https://img.shields.io/badge/python-3.12.4-purple)
- ![Pytest](https://img.shields.io/badge/pytest-8.3.3-green)
- ![Selenium](https://img.shields.io/badge/selenium-4.25.0-blue)

## Описание тестов:
# autorization_with_password_test.py
1. - test_tab_displayed_autorization_with_password: проверка наличия элементов на странице авторизации с паролем.
   - test_input_and_tab_switching_autorization_with_password: проверка автоматической активации таба при вводе соответствующего значения в поле username (невозможно проверить смену таба на Лицевой счет, так как отсутствуют требования к данному полю).
   - test_active_tab_autorization_with_password: проверка того, что таб Номер является активным по умолчанию (проверка происходит через таб Телефон).
2. test_correct_authorization_with_number: проверка авторизации клиента по Номеру телефона при вводе корректной связки Номер+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы: time.sleep(15).
3. test_incorrect_authorization_with_number_and_wrong_password: проверка Ошибки при авторизации клиента по Номеру телефона при вводе НЕкорректной связки Номер+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы: time.sleep(15).
4. test_incorrect_authorization_with_incorrect_number: проверка Ошибки при авторизации клиента по Номеру телефона при вводе НЕкорректного Номера.
5. test_correct_authorization_with_email: проверка Авторизации клиента по Почте при вводе корректной связки Почта+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы: time.sleep(15).
6. test_incorrect_authorization_with_email_and_wrong_password: проверка Ошибки при авторизации клиента по Почте при вводе НЕкорректной связки Почта+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы: time.sleep(15).
7. test_incorrect_authorization_with_incorrect_email: проверка Ошибки при авторизации клиента по Почте при вводе НЕкорректной Почты.
8. test_correct_authorization_with_login: Авторизация клиента по Логину при вводе корректной связки Логин+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы: time.sleep(15).
9. test_incorrect_authorization_with_login_and_wrong_password: Ошибка при авторизации клиента по Логину при вводе НЕкорректной связки Логин+Пароль. При активном тестировании в форме авторизации появляется капча, которую необходимо ввести вручную, для этого нужно снять комментарий со строки паузы: time.sleep(15).
10. test_incorrect_authorization_with_incorrect_login: Ошибка при авторизации клиента по Логину при вводе НЕкорректного Логина. Тест закомментирован, так как нет возможности проверить появление ошибки из-за отсутствия требрваний к значению Логина.
11. test_correct_authorization_with_licevoy_schet: Авторизация клиента по Лицевому счету при вводе корректной связки Логин+Пароль - тест не активен, т.к. нет доступа к лицевому счету.
12. test_incorrect_authorization_with_licevoy_schet_and_wrong_password: Ошибка при авторизации клиента по Лицевому счету при вводе НЕкорректной связки Логин+Пароль - тест не активен, т.к. нет доступа к лицевому счету.
13. test_incorrect_authorization_with_incorrect_licevoy_schet: Ошибка при авторизации клиента по Лицевому счету при вводе НЕкорректного Лицевого счета - тест не активен, т.к. нет доступа к лицевому счету.
