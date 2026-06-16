@echo off
REM Скрипт для запуска бота КОНТАНТА на Windows

echo.
echo ========================================================
echo   🎖️  KONTANTA TELEGRAM BOT - LAUNCHER
echo ========================================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен или не добавлен в PATH
    echo Скачайте Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python найден
echo.

REM Проверка виртуального окружения
if not exist "venv\" (
    echo 📦 Создание виртуального окружения...
    python -m venv venv
    echo ✅ Виртуальное окружение создано
)

echo.
echo 🔄 Активация виртуального окружения...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Ошибка активации виртуального окружения
    pause
    exit /b 1
)

echo ✅ Виртуальное окружение активировано
echo.

REM Проверка зависимостей
echo 📥 Проверка зависимостей...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo ✅ Зависимости установлены
echo.

REM Проверка конфигурации
echo 🔍 Проверка конфигурации...
python check_config.py

if errorlevel 1 (
    echo ❌ Ошибки конфигурации
    echo Отредактируйте файл .env и попробуйте снова
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   🚀 ЗАПУСК БОТА
echo ========================================================
echo.

REM Запуск бота
python bot.py

REM Если бот завершился с ошибкой
if errorlevel 1 (
    echo.
    echo ❌ Бот завершился с ошибкой
    echo Проверьте логи выше
    pause
    exit /b 1
)
