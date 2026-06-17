from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Главное меню с кнопками в стиле РФ"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏛️ О КОНТАНТА ⚔️", callback_data="section_about"),
                InlineKeyboardButton(text="📋 ВАКАНСИИ 💪", callback_data="section_vacancies"),
            ],
            [
                InlineKeyboardButton(text="🎖️ ОБУЧЕНИЕ 🎓", callback_data="section_training"),
                InlineKeyboardButton(text="💰 ЛЬГОТЫ 🏆", callback_data="section_benefits"),
            ],
            [
                InlineKeyboardButton(text="❓ ВОПРОСЫ 📚", callback_data="section_faq"),
                InlineKeyboardButton(text="☎️ КОНТАКТЫ 📍", callback_data="section_contacts"),
            ],
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
    """Клавиатура всех 6 вакансий"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚁 Операторы БПЛА (FPV)", callback_data="vac_bpla")],
            [InlineKeyboardButton(text="📡 Специалисты РЭБ, РЭР, ПВО", callback_data="vac_reb")],
            [InlineKeyboardButton(text="💻 IT-специалисты", callback_data="vac_it")],
            [InlineKeyboardButton(text="🚛 Водители категории C, E", callback_data="vac_driver")],
            [InlineKeyboardButton(text="⚕️ Военные медики", callback_data="vac_medic")],
            [InlineKeyboardButton(text="📞 Связисты, сапёры", callback_data="vac_engineer")],
            [InlineKeyboardButton(text="◀️ НАЗАД В МЕНЮ", callback_data="back_to_menu")]
        ]
    )
    return keyboard

def vacancy_details_keyboard(vacancy_code):
    """Клавиатура для деталей вакансии"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ ПОДАТЬ ЗАЯВКУ", url="https://www.kontanta.ru/contacts"),
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
                InlineKeyboardButton(text="📞 ПОЗВОНИТЬ", callback_data="contact_phone"),
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

def phone_options_keyboard():
    """Меню способов связи по телефону"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ НАЗАД", callback_data="back_to_help")]
        ]
    )
    return keyboard

def vacancy_list_keyboard(vacancies):
    """Динамическая клавиатура списка вакансий"""
    keyboard_list = []
    
    for vacancy in vacancies:
        button_text = f"⭐ {vacancy['title']}"
        keyboard_list.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"vacancy_{vacancy['id']}"
            )
        ])
    
    keyboard_list.append([
        InlineKeyboardButton(text="◀️ НАЗАД", callback_data="back_to_vacancies")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_list)
