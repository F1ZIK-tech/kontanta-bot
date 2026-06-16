#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
cp .env.example .env

echo ""
echo "==================== УСТАНОВКА ЗАВЕРШЕНА ===================="
echo ""
echo "📝 НЕОБХОДИМО ВЫПОЛНИТЬ:"
echo ""
echo "1. Откройте файл .env и добавьте ваш BOT_TOKEN:"
echo "   nano .env"
echo ""
echo "2. Получить токен можно здесь: https://t.me/botfather"
echo ""
echo "3. Запустите бота:"
echo "   python bot.py"
echo ""
echo "ИЛИ с Docker:"
echo "   docker-compose up -d"
echo ""
echo "==============================================================="
