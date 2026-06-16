import asyncio
import logging
from dotenv import load_dotenv
import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

from handlers import router
from database import Database

# Загрузить переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def init_db():
    """Инициализация базы данных с примерами вакансий"""
    db = Database()
    
    # Добавить примеры вакансий если их нет
    vacancies = db.get_vacancies()
    if not vacancies:
        db.add_vacancy(
            title="Оператор БПЛА",
            category="БПЛА",
            description="Требуется опытный оператор беспилотных летательных аппаратов для работы в составе высокотехнологичного подразделения РФ.",
            requirements="• Опыт работы с БПЛА\n• Высокая концентрация внимания\n• Физическая выносливость\n• Воинская подготовка приветствуется",
            salary="От 150 000 руб."
        )
        
        db.add_vacancy(
            title="Водитель КАМАЗ",
            category="КАМАЗ",
            description="Квалифицированный водитель КАМАЗ для служебных автотранспортных операций. Требуется надёжный и ответственный специалист.",
            requirements="• Категория прав C, D или E\n• Опыт вождения грузовиков\n• Отличное здоровье\n• Преданность и ответственность",
            salary="От 120 000 руб."
        )
        
        db.add_vacancy(
            title="Специалист по ИТ",
            category="ИТ",
            description="Специалист в области информационных технологий для работы с современными системами. Требуется знание сетевых технологий и киберзащиты.",
            requirements="• Опыт в IT (минимум 2 года)\n• Знание Linux/Windows\n• Основы сетевых технологий\n• Знание основ кибербезопасности",
            salary="От 180 000 руб."
        )
        
        db.add_vacancy(
            title="Оператор БПЛА (опытный)",
            category="БПЛА",
            description="Вакансия для опытных операторов с большим стажем. Работа на элитных направлениях с использованием самого современного оборудования.",
            requirements="• 3+ года опыта с БПЛА\n• Опыт в боевых условиях\n• Сертификаты и допуски\n• Высокий уровень подготовки",
            salary="От 250 000 руб."
        )
        
        db.add_vacancy(
            title="Водитель КАМАЗ (опытный)",
            category="КАМАЗ",
            description="Опытный водитель КАМАЗ для сложных логистических операций и специальных заданий.",
            requirements="• 5+ лет опыта вождения КАМАЗ\n• Опыт в экстремальных условиях\n• Знание техническое обслуживание\n• Отличная физическая форма",
            salary="От 180 000 руб."
        )
        
        logger.info("✅ Примеры вакансий добавлены в базу данных")

async def main():
    """Главная функция бота - Polling режим"""
    # Инициализация БД
    await init_db()
    
    # Получить токен бота
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("❌ BOT_TOKEN не установлен в .env файле")
    
    # Инициализация бота и диспетчера
    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Подключить маршруты
    dp.include_router(router)
    
    logger.info("🤖 Бот КОНТАНТА запущен...")
    logger.info(f"📊 БД инициализирована: kontanta.db")
    logger.info("📡 Режим: Polling (всегда готов к работе)")
    
    try:
        # Запуск polling с оптимальными параметрами для стабильности
        await dp.start_polling(
            bot, 
            allowed_updates=dp.resolve_used_update_types(),
            timeout=30,  # Таймаут для подключения
            relax=0.1    # Задержка между проверками (для снижения нагрузки)
        )
    except KeyboardInterrupt:
        logger.info("⛔ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()
        logger.info("✅ Сессия закрыта")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот завершён")
