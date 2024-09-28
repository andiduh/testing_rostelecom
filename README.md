# Тесты для авторизации, регистрации и восстановления пароля в Ростелеком.

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

4. Запустите тесты:
```bash
pytest
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

5. Выполните команду для разрешения запуска скриптов (для активации виртуального окружения):
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

6. Создайте и активируйте виртуальное окружение:
```bash
py -m venv venv
source venv/bin/activate
```

7. Установите библиотеки для работы программы:
```bash
pip install -r requirements.txt
```

8. Запустите тесты:
```bash 
pytest
```

## Технологии

- ![Python](https://img.shields.io/badge/python-3.12.4-purple)
- ![Pytest](https://img.shields.io/badge/pytest-8.3.3-green)
- ![Selenium](https://img.shields.io/badge/selenium-4.25.0-blue)
