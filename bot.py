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
    """Инициализация базы данных с вакансиями со страницы https://www.kontanta.ru/vacancies"""
    db = Database()
    
    # Добавить вакансии если их нет
    vacancies = db.get_vacancies()
    if not vacancies:
        # Вакансия 1: Операторы БПЛА (FPV и другие)
        db.add_vacancy(
            title="Операторы БПЛА (FPV и другие)",
            category="БПЛА",
            description="Управление, наведение, сборка и анализ данных в реальном времени. Работа со всем спектром ударных и разведывательных систем.\n\nЦентр «КРЕЧЕТ» | Ударное подразделение",
            requirements="• Опыт с беспилотными системами\n• Высокая концентрация внимания\n• Физическая выносливость\n• Готовность к дислокации",
            salary="От 240 000 ₽"
        )
        
        # Вакансия 2: Специалисты РЭБ, РЭР, ПВО
        db.add_vacancy(
            title="Специалисты РЭБ, РЭР, ПВО",
            category="РЭБ",
            description="Обеспечение превосходства в эфире, защита неба от вражеских беспилотников и подавление каналов связи противника.\n\nТехнический дивизион",
            requirements="• Знание радиочастотных технологий\n• Опыт в электромагнитной защите\n• Техническое образование\n• Готовность к дислокации",
            salary="От 210 000 ₽"
        )
        
        # Вакансия 3: IT-специалисты
        db.add_vacancy(
            title="IT-специалисты",
            category="ИТ",
            description="Ответственность за программное обеспечение, сети, кибербезопасность систем и внедрение ИИ-решений в беспилотные комплексы.\n\nЦентр разработки",
            requirements="• Опыт в разработке ПО или администрировании\n• Знание сетевых технологий\n• Основы кибербезопасности\n• Желательно высшее техническое образование",
            salary="От 190 000 ₽"
        )
        
        # Вакансия 4: Водители категории C, E
        db.add_vacancy(
            title="Водители категории C, E",
            category="КАМАЗ",
            description="Обеспечение мобильности и логистики, перевозка высокотехнологичного оборудования и личного состава подразделения.\n\nЛогистический корпус",
            requirements="• Категория прав C или E\n• Опыт вождения грузовиков\n• Отличное здоровье\n• Ответственность и надежность",
            salary="От 180 000 ₽"
        )
        
        # Вакансия 5: Военные медики
        db.add_vacancy(
            title="Военные медики",
            category="Медицина",
            description="Оказание помощи в формате высокотехнологичного подразделения. Использование современных протоколов тактической медицины.\n\nМедицинская служба",
            requirements="• Медицинское образование (минимум медбрат/сестра)\n• Знание тактической медицины\n• Психологическая устойчивость\n• Готовность к дислокации",
            salary="От 200 000 ₽"
        )
        
        # Вакансия 6: Связисты, сапёры
        db.add_vacancy(
            title="Связисты, сапёры",
            category="Инженерия",
            description="Обеспечение и развёртывание инфраструктуры связи в полевых условиях, инженерная разведка и разминирование.\n\nИнженерный корпус",
            requirements="• Опыт в области связи или инженерии\n• Знание полевых коммуникаций\n• Техническая подготовка\n• Физическая выносливость",
            salary="От 190 000 ₽"
        )
        
        logger.info("✅ Все вакансии добавлены в базу данных")

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
