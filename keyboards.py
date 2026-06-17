from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Главное меню с кнопками в стиле РФ"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            # Ряд 1: О нас + Вакансии
            [
                InlineKeyboardButton(text="🏛️ О КОНТАНТА ⚔️", callback_data="section_about"),
                InlineKeyboardButton(text="📋 ВАКАНСИИ 💪", callback_data="section_vacancies"),
            ],
            # Ряд 2: Обучение + Льготы
            [
                InlineKeyboardButton(text="🎖️ ОБУЧЕНИЕ 🎓", callback_data="section_training"),
                InlineKeyboardButton(text="💰 ЛЬГОТЫ 🏆", callback_data="section_benefits"),
            ],
            # Ряд 3: FAQ + Контакты
            [
                InlineKeyboardButton(text="❓ ВОПРОСЫ 📚", callback_data="section_faq"),
                InlineKeyboardButton(text="☎️ КОНТАКТЫ 📍", callback_data="section_contacts"),
            ],
            # Ряд 4: Связь + Канал
            [
                InlineKeyboardButton(text="💬 СВЯЗАТЬСЯ 🤝", callback_data="section_help"),
                InlineKeyboardButton(text="📢 НАШ КАНАЛ ❓", url="https://t.me/kontanta_kontanta"),
            ],
        ]
    )
    return keyboard

def back_menu_keyboard(callback_data="back_to_menu"):
    """Кнопка возврата в главное меню"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ", callback_data=callback_data)]
        ]
    )
    return keyboard

def categories_keyboard():
    """Клавиатура категорий вакансий"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚁 ОПЕРАТОРЫ БПЛА ❓", callback_data="cat_bpla")],
            [InlineKeyboardButton(text="🚛 ВОДИТЕЛИ КАМАЗ 💪", callback_data="cat_kamaz")],
            [InlineKeyboardButton(text="💻 СПЕЦИАЛИСТЫ ИТ ⚔️", callback_data="cat_it")],
            [InlineKeyboardButton(text="◀️ НАЗАД В МЕНЮ", callback_data="back_to_menu")]
        ]
    )
    return keyboard

def vacancy_details_keyboard(vacancy_id: int):
    """Клавиатура для деталей вакансии"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ ПОДАТЬ ЗАЯВКУ", callback_data=f"apply_{vacancy_id}"),
            ],
            [
                InlineKeyboardButton(text="◀️ К ВАКАНСИЯМ", callback_data="back_to_vacancies")
            ]
        ]
    )
    return keyboard

def confirmation_keyboard():
    """Клавиатура подтверждения"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ ПОДТВЕРДИТЬ", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ ОТМЕНИТЬ", callback_data="confirm_no")
            ]
        ]
    )
    return keyboard

def faq_keyboard():
    """Клавиатура FAQ"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📮 Как подать заявку?", callback_data="faq_q1")],
            [InlineKeyboardButton(text="📋 Какие требования?", callback_data="faq_q2")],
            [InlineKeyboardButton(text="🔄 Процедура контрактации", callback_data="faq_q3")],
            [InlineKeyboardButton(text="💵 Размер зарплаты", callback_data="faq_q4")],
            [InlineKeyboardButton(text="📅 Сроки контракта", callback_data="faq_q5")],
            [InlineKeyboardButton(text="👨‍👩‍👧 Для семейных?", callback_data="faq_q6")],
            [InlineKeyboardButton(text="◀️ В ГЛАВНОЕ МЕНЮ", callback_data="back_to_menu")]
        ]
    )
    return keyboard

def contact_keyboard():
    """Клавиатура для связи"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="☎️ +7 (495) 415-25-64", url="https://t.me/kontanta_kontanta"),
                InlineKeyboardButton(text="📱 TELEGRAM", url="https://t.me/kontanta_kontanta"),
            ],
            [
                InlineKeyboardButton(text="🌐 НА САЙТ", url="https://www.kontanta.ru"),
            ],
            [
                InlineKeyboardButton(text="◀️ В ГЛАВНОЕ МЕНЮ", callback_data="back_to_menu")
            ]
        ]
    )
    return keyboard

def vacancy_list_keyboard(vacancies):
    """Динамическая клавиатура списка вакансий"""
    keyboard_list = []
    
    for vacancy in vacancies:
        # Красивый текст кнопки с эмодзи
        button_text = f"⭐ {vacancy['title']}"
        keyboard_list.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"vacancy_{vacancy['id']}"
            )
        ])
    
    # Добавляем кнопку возврата
    keyboard_list.append([
        InlineKeyboardButton(text="◀️ НАЗАД", callback_data="back_to_vacancies")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_list)
