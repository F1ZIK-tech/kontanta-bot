#!/usr/bin/env python3
"""
Скрипт диагностики для проверки конфигурации бота КОНТАНТА
"""

import os
import sys
from pathlib import Path

def check_configuration():
    print("=" * 70)
    print("🔍 ДИАГНОСТИКА БОТА КОНТАНТА")
    print("=" * 70)
    print()

    # 1. Проверка файла .env
    print("1️⃣  Проверка файла .env...")
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ Файл .env найден")
        with open(".env", "r") as f:
            content = f.read()
            if "BOT_TOKEN=" in content:
                print("   ✅ BOT_TOKEN присутствует в .env")
                # Извлечь токен (без показа полного токена)
                for line in content.split("\n"):
                    if "BOT_TOKEN=" in line:
                        token = line.split("=")[1].strip()
                        if token and len(token) > 10:
                            print(f"   ✅ Токен начинается с: {token[:20]}...")
                        elif token:
                            print(f"   ⚠️  Токен слишком короткий: {token}")
                        else:
                            print("   ❌ Токен пуст!")
            else:
                print("   ❌ BOT_TOKEN не найден в .env")
    else:
        print("   ❌ Файл .env НЕ найден!")
        print("   📝 Создайте .env из .env.example")
        return False

    print()

    # 2. Проверка основных файлов
    print("2️⃣  Проверка основных файлов...")
    required_files = [
        "bot.py",
        "handlers.py",
        "keyboards.py",
        "database.py",
        "content.py",
        "requirements.txt"
    ]
    
    all_files_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} НЕ найден!")
            all_files_ok = False
    
    if not all_files_ok:
        return False

    print()

    # 3. Проверка Python
    print("3️⃣  Проверка Python...")
    version = sys.version_info
    print(f"   Python версия: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 11:
        print("   ✅ Python версия подходит (3.11+)")
    else:
        print(f"   ⚠️  Рекомендуется Python 3.11+, у вас {version.major}.{version.minor}")

    print()

    # 4. Проверка модулей
    print("4️⃣  Проверка установленных модулей...")
    required_modules = {
        "aiogram": "aiogram",
        "dotenv": "python-dotenv",
        "sqlite3": "sqlite3"
    }
    
    modules_ok = True
    for module_name, package_name in required_modules.items():
        try:
            __import__(module_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} НЕ установлен")
            modules_ok = False

    if not modules_ok:
        print()
        print("   📝 Установите недостающие пакеты:")
        print("   pip install -r requirements.txt")
        return False

    print()

    # 5. Проверка синтаксиса файлов
    print("5️⃣  Проверка синтаксиса Python файлов...")
    import py_compile
    files_to_check = ["bot.py", "handlers.py", "content.py", "keyboards.py", "database.py"]
    
    syntax_ok = True
    for file in files_to_check:
        try:
            py_compile.compile(file, doraise=True)
            print(f"   ✅ {file}")
        except py_compile.PyCompileError as e:
            print(f"   ❌ {file} - ошибка синтаксиса!")
            print(f"      {str(e)}")
            syntax_ok = False

    if not syntax_ok:
        return False

    print()
    print("=" * 70)
    print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 70)
    print()
    print("Теперь вы можете запустить бота:")
    print("   python bot.py")
    print()
    return True

if __name__ == "__main__":
    success = check_configuration()
    sys.exit(0 if success else 1)
