#!/bin/bash

# Скрипт для запуска бота КОНТАНТА на Linux/Mac

echo ""
echo "========================================================"
echo "   🎖️  KONTANTA TELEGRAM BOT - LAUNCHER"
echo "========================================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен"
    echo "Установите: sudo apt-get install python3 python3-pip (Ubuntu/Debian)"
    echo "Или: brew install python3 (macOS)"
    exit 1
fi

echo "✅ Python найден"
echo ""

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
fi

echo ""
echo "🔄 Активация виртуального окружения..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Ошибка активации виртуального окружения"
    exit 1
fi

echo "✅ Виртуальное окружение активировано"
echo ""

# Проверка зависимостей
echo "📥 Проверка зависимостей..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Ошибка установки зависимостей"
    echo "Попробуйте: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Зависимости установлены"
echo ""

# Проверка конфигурации
echo "🔍 Проверка конфигурации..."
python3 check_config.py

if [ $? -ne 0 ]; then
    echo "❌ Ошибки конфигурации"
    echo "Отредактируйте файл .env и попробуйте снова"
    exit 1
fi

echo ""
echo "========================================================"
echo "   🚀 ЗАПУСК БОТА"
echo "========================================================"
echo ""

# Запуск бота
python3 bot.py

# Если бот завершился с ошибкой
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Бот завершился с ошибкой"
    echo "Проверьте логи выше"
    exit 1
fi
