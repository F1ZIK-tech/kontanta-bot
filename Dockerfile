FROM python:3.11-slim

WORKDIR /app

# Установить зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Скопировать requirements
COPY requirements.txt .

# Установить Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать код приложения
COPY . .

# Создать директорию для БД
RUN mkdir -p /app/data

# Переменная окружения для SQLite БД
ENV DATABASE_PATH=/app/data/kontanta.db

# Запустить бота
CMD ["python", "bot.py"]
