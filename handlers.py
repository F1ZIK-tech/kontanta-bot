from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json

from keyboards import (
    main_menu_keyboard, back_menu_keyboard, categories_keyboard,
    vacancy_details_keyboard, confirmation_keyboard, faq_keyboard,
    contact_keyboard, vacancy_list_keyboard, phone_options_keyboard
)
from database import Database
from content import (
    WELCOME_MESSAGE_TEMPLATE, ABOUT_SECTION, VACANCIES_INTRO, CATEGORIES,
    TRAINING_SECTION, BENEFITS_SECTION, FAQ_SECTION, FAQ_DATA,
    HELP_SECTION, CONTACTS_SECTION
)

router = Router()
db = Database()

class ApplicationForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_experience = State()
    waiting_for_confirmation = State()

@router.message(Command("start", "s"))
async def start_handler(message: Message):
    """Обработчик команды /start с приветствием по имени пользователя"""
    db.add_user(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or "",
        username=message.from_user.username or ""
    )
    
    # Формируем имя пользователя для приветствия
    user_name = ""
    if message.from_user.first_name:
        user_name = message.from_user.first_name
    if message.from_user.last_name:
        user_name += " " + message.from_user.last_name
    if not user_name.strip() and message.from_user.username:
        user_name = "@" + message.from_user.username
    if not user_name.strip():
        user_name = "Боец"
    
    # Форматируем приветственное сообщение с именем пользователя
    welcome_text = WELCOME_MESSAGE_TEMPLATE.format(user_name=user_name)
    
    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

# ============== РАЗДЕЛЫ ==============

@router.callback_query(F.data == "section_about")
async def about_handler(callback: CallbackQuery):
    """Раздел 'О нас'"""
    await callback.message.edit_text(
        ABOUT_SECTION,
        reply_markup=back_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "section_vacancies")
async def vacancies_handler(callback: CallbackQuery):
    """Раздел вакансий - выбор вакансии"""
    await callback.message.edit_text(
        "📋 ВАКАНСИИ - ВЫБОР\n\n✈️ Выберите интересующую должность:",
        reply_markup=categories_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("vac_"))
async def vacancy_details_handler(callback: CallbackQuery):
    """Показать детали вакансии"""
    vac_code = callback.data.replace("vac_", "")
    
    vac_map = {
        "bpla": db.get_vacancies(category="БПЛА")[0] if db.get_vacancies(category="БПЛА") else None,
        "reb": db.get_vacancies(category="РЭБ")[0] if db.get_vacancies(category="РЭБ") else None,
        "it": db.get_vacancies(category="ИТ")[0] if db.get_vacancies(category="ИТ") else None,
        "driver": db.get_vacancies(category="КАМАЗ")[0] if db.get_vacancies(category="КАМАЗ") else None,
        "medic": db.get_vacancies(category="Медицина")[0] if db.get_vacancies(category="Медицина") else None,
        "engineer": db.get_vacancies(category="Инженерия")[0] if db.get_vacancies(category="Инженерия") else None,
    }
    
    vacancy = vac_map.get(vac_code)
    
    if not vacancy:
        await callback.answer("Вакансия не найдена", show_alert=True)
        return
    
    text = f"""🎖️ {vacancy['title']}

{vacancy['description']}

📋 Требования:
{vacancy['requirements']}

💰 {vacancy['salary']}
"""
    
    await callback.message.edit_text(text, reply_markup=vacancy_details_keyboard(vac_code))
    await callback.answer()

@router.callback_query(F.data.startswith("apply_"))
async def apply_handler(callback: CallbackQuery, state: FSMContext):
    """Начать процесс подачи заявки"""
    vacancy_id = int(callback.data.split("_")[1])
    vacancy = db.get_vacancy_by_id(vacancy_id)
    
    await state.set_state(ApplicationForm.waiting_for_name)
    await state.update_data(vacancy_id=vacancy_id, vacancy_title=vacancy['title'])
    
    await callback.message.edit_text("📝 ЗАПОЛНИТЕ ФОРМУ ЗАЯВКИ\n\n✏️ Введите ваше полное имя:")
    await callback.answer()

@router.message(ApplicationForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Обработать имя"""
    await state.update_data(full_name=message.text)
    await state.set_state(ApplicationForm.waiting_for_phone)
    await message.answer("📞 Введите ваш номер телефона:")

@router.message(ApplicationForm.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Обработать телефон"""
    await state.update_data(phone=message.text)
    await state.set_state(ApplicationForm.waiting_for_email)
    await message.answer("📧 Введите вашу электронную почту:")

@router.message(ApplicationForm.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    """Обработать email"""
    await state.update_data(email=message.text)
    await state.set_state(ApplicationForm.waiting_for_experience)
    await message.answer("💼 Расскажите о вашем опыте (или напишите '-' для пропуска):")

@router.message(ApplicationForm.waiting_for_experience)
async def process_experience(message: Message, state: FSMContext):
    """Обработать опыт"""
    if message.text == "-":
        experience = "Не указан"
    else:
        experience = message.text
    
    await state.update_data(experience=experience)
    await state.set_state(ApplicationForm.waiting_for_confirmation)
    
    data = await state.get_data()
    
    text = f"""✅ ПРОВЕРЬТЕ ВАШИ ДАННЫЕ:

📝 Имя: {data['full_name']}
📞 Телефон: {data['phone']}
📧 Email: {data['email']}
💼 Опыт: {data['experience']}
🎖️ Должность: {data['vacancy_title']}

✈️ Всё верно? Отправить заявку?"""
    
    await message.answer(text, reply_markup=confirmation_keyboard())

@router.callback_query(F.data == "confirm_yes")
async def confirm_application(callback: CallbackQuery, state: FSMContext):
    """Подтвердить заявку"""
    data = await state.get_data()
    
    app_id = db.add_application(
        user_id=callback.from_user.id,
        vacancy_id=data['vacancy_id'],
        full_name=data['full_name'],
        phone=data['phone'],
        email=data['email'],
        experience=data['experience']
    )
    
    await callback.message.edit_text(
        f"""✅ ЗАЯВКА УСПЕШНО ОТПРАВЛЕНА!

🎖️ Номер заявки: #{app_id}
✈️ Должность: {data['vacancy_title']}

📞 Наша команда свяжется с вами:
{data['phone']}

Благодарим вас за доверие! 🚀""",
        reply_markup=back_menu_keyboard()
    )
    
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "confirm_no")
async def cancel_application(callback: CallbackQuery, state: FSMContext):
    """Отменить заявку"""
    await callback.message.edit_text(
        "❌ Заявка отменена.",
        reply_markup=back_menu_keyboard()
    )
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "section_training")
async def training_handler(callback: CallbackQuery):
    """Раздел 'Обучение'"""
    await callback.message.edit_text(
        TRAINING_SECTION,
        reply_markup=back_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "section_benefits")
async def benefits_handler(callback: CallbackQuery):
    """Раздел 'Льготы и выплаты'"""
    await callback.message.edit_text(
        BENEFITS_SECTION,
        reply_markup=back_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "section_faq")
async def faq_handler(callback: CallbackQuery):
    """Раздел 'Вопросы и ответы'"""
    await callback.message.edit_text(
        "❓ ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ\n\n✈️ Выберите интересующий вопрос:",
        reply_markup=faq_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("faq_q"))
async def faq_answer_handler(callback: CallbackQuery):
    """Показать ответ на FAQ"""
    # callback.data = "faq_q1", "faq_q2" и т.д.
    # Нужно вытащить "q1", "q2"
    question_key = callback.data.replace("faq_", "")
    
    try:
        if question_key in FAQ_DATA:
            faq = FAQ_DATA[question_key]
            text = f"""❓ {faq['question']}

{faq['answer']}"""
            
            await callback.message.edit_text(
                text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="◀️ ← К ВОПРОСАМ", callback_data="back_to_faq")],
                    [InlineKeyboardButton(text="🏠 → В ГЛАВНОЕ МЕНЮ", callback_data="back_to_menu")]
                ])
            )
        else:
            await callback.answer("Ошибка: вопрос не найден", show_alert=True)
    except Exception as e:
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)
    
    await callback.answer()

@router.callback_query(F.data == "section_help")
async def help_handler(callback: CallbackQuery):
    """Раздел 'Связаться с оператором'"""
    await callback.message.edit_text(
        HELP_SECTION,
        reply_markup=contact_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "section_contacts")
async def contacts_handler(callback: CallbackQuery):
    """Раздел 'Контакты'"""
    await callback.message.edit_text(
        CONTACTS_SECTION,
        reply_markup=contact_keyboard()
    )
    await callback.answer()

# ============== НАВИГАЦИЯ ==============

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery):
    """Вернуться в главное меню"""
    user_name = callback.from_user.first_name or "Боец"
    welcome_text = f"""🎖️ Здравствуйте, {user_name}!

Выберите интересующий раздел:"""
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_vacancies")
async def back_to_vacancies_handler(callback: CallbackQuery):
    """Вернуться к категориям вакансий"""
    await callback.message.edit_text(
        VACANCIES_INTRO,
        reply_markup=categories_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_faq")
async def back_to_faq_handler(callback: CallbackQuery):
    """Вернуться к FAQ"""
    await callback.message.edit_text(
        "❓ ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ\n\n✈️ Выберите интересующий вопрос:",
        reply_markup=faq_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "contact_phone")
async def contact_phone_handler(callback: CallbackQuery):
    """Меню способов связи по телефону"""
    await callback.message.edit_text(
        "☎️ СПОСОБЫ СВЯЗИ\n\n📢 +7 (495) 415-25-64",
        reply_markup=phone_options_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_help")
async def back_to_help_handler(callback: CallbackQuery):
    """Вернуться к меню связи"""
    await callback.message.edit_text(
        HELP_SECTION,
        reply_markup=contact_keyboard()
    )
    await callback.answer()

# ============== ОБРАБОТЧИК ТЕКСТА ==============

@router.message(ApplicationForm.waiting_for_name)
async def catch_all_handler(message: Message, state: FSMContext):
    """Обработчик для неожиданных сообщений"""
    current_state = await state.get_state()
    if current_state:
        await message.answer("Пожалуйста, следуйте инструкциям выше.")
    else:
        await message.answer(
            "Пожалуйста, используйте кнопки меню.",
            reply_markup=main_menu_keyboard()
        )
