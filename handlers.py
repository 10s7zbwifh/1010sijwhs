from aiogram import types, Router, Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from markups import *
from states import Form
from database import *
from datetime import datetime, timedelta
from aiogram.enums import ParseMode
from utils import send_complaints_from_all_accounts, send_email
from config import admins, TOKEN
from get_id import get_sender_id
import aiosmtplib
from email.mime.text import MIMEText
import logging
import random
import requests
from faker import Faker
faker = Faker()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
router = Router()

def register_handlers(dp: Dispatcher, bot):
    dp.include_router(router)
    router.message.register(start_command, Command("start"))
    router.callback_query.register(handle_botnetsnos, lambda c: c.data == 'botnetsnos')
    router.message.register(handle_link_submission, Form.waiting_for_link)
    router.callback_query.register(handle_back, lambda c: c.data == 'back')
    router.callback_query.register(handle_profile, lambda c: c.data == 'profile')
    router.message.register(add_subscription_command, Command("addsub"))
    router.message.register(whitelist_command, Command("whitelist"))
    router.message.register(subscribe, Command("subscribe"))
    router.callback_query.register(emailsnos, lambda c: c.data == "emailsnos")
    router.message.register(handle_email_text_submission, Form.waiting_for_email_text)

@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext = None):
    user_id = message.from_user.id
    add_to_db(user_id)

    await state.clear()
    keyboard = start_keyboard()
    await message.answer(
        "<b>👋 Приветствую в сносер бот.</b>\n"
        "<blockquote>Купить подписку: @RainSu, @archihz</blockquote>",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@router.callback_query(lambda c: c.data == 'admin_panel')
async def handle_admin_panel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    keyboard = admin_panel_keyboard()
    
    if user_id not in admins:
        await callback_query.answer("<b>⛔ У вас нет доступа к этой функции.</b>", parse_mode=ParseMode.HTML)
    else:
        await callback_query.message.edit_text("⚙ Админ панель:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data == 'add_whitelist')
async def handle_add_whitelist(callback_query: types.CallbackQuery):
    users = get_all_users_from_db()
    keyboard = whitelist_users_keyboard(users)
    await callback_query.message.edit_text("Выберите пользователя для вайт-листа:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data == 'give_subscription')
async def handle_give_subscription(callback_query: types.CallbackQuery):
    users = get_all_users_from_db()
    keyboard = subscription_users_keyboard(users)
    await callback_query.message.edit_text("Выберите пользователя для подписки:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('whitelist_user_'))
async def handle_whitelist_user_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[-1]
    keyboard = whitelist_actions_keyboard(user_id)
    await callback_query.message.edit_text(f"Выберите действие для пользователя {user_id}:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('add_to_whitelist_'))
async def handle_add_to_whitelist(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[-1]
    add_to_whitelist(user_id)
    await callback_query.message.answer(f"✅ Пользователь {user_id} добавлен в вайт-лист.")

@router.callback_query(lambda c: c.data.startswith('remove_from_whitelist_'))
async def handle_remove_from_whitelist(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[-1]
    remove_from_whitelist(user_id)
    await callback_query.message.answer(f"❌ Пользователь {user_id} удалён из вайт-листа.")

@router.callback_query(lambda c: c.data.startswith('subscription_user_'))
async def handle_subscription_user_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[-1]
    keyboard = subscription_actions_keyboard(user_id)
    await callback_query.message.edit_text(f"Выберите действие для пользователя {user_id}:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('give_subscription_'))
async def handle_give_subscription_to_user(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[-1]
    keyboard = subscription_duration_keyboard(user_id)
    await callback_query.message.edit_text(f"Выберите длительность подписки для {user_id}:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('subscribe_'))
async def handle_subscription_duration(callback_query: types.CallbackQuery):
    user_id, duration = callback_query.data.split('_')[1], callback_query.data.split('_')[2]
    if duration == '1d':
        expiration_date = datetime.now() + timedelta(days=1)
    elif duration == '7d':
        expiration_date = datetime.now() + timedelta(days=7)
    elif duration == '30d':
        expiration_date = datetime.now() + timedelta(days=30)
    elif duration == 'forever':
        expiration_date = datetime.now() + timedelta(days=365 * 100)  # Навсегда
    add_subscription(user_id, expiration_date)
    await callback_query.message.answer(f"🎁 Пользователь {user_id} получил подписку на {duration}.")

@router.callback_query(lambda c: c.data.startswith('remove_subscription_'))
async def handle_remove_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[-1]
    remove_subscription(user_id)
    await callback_query.message.answer(f"❌ Подписка пользователя {user_id} удалена.")

@router.callback_query(lambda c: c.data == 'botnetsnos')
async def handle_botnetsnos(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id in admins or check_subscription(user_id):
        if callback_query.message and hasattr(callback_query.message, 'delete'):
            await callback_query.message.delete()
        keyboard = back_button_keyboard()
        await callback_query.message.answer(
            "<b>📨 Введите ссылку на нарушение:</b>",
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
        await state.set_state(Form.waiting_for_link)
    else:
        await callback_query.answer(
            text="❌ У вас нет активной подписки!",
            show_alert=True
        )

@router.message(Form.waiting_for_link)
async def handle_link_submission(message: types.Message, state: FSMContext):
    link = message.text
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    sender_id = await get_sender_id(link)
    session_files = ["+77713208646.session", "+77773030299.session", "+77787130376.session", "+77073823408.session", "+77029244504.session"]
    if sender_id is None:
        await message.answer("Не удалось извлечь ID отправителя.")
        return
    if is_whitelisted(sender_id):
        await message.answer(f"<b>Этот пользователь в вайт листе, невозможно снести его.</b>", parse_mode=ParseMode.HTML)
        await state.clear()
        await bot.send_message(
            sender_id,
            f"<b>🚨 Тебе хотел снести <a href='tg://openmessage?user_id={user_id}'>{first_name}</a>, но попытка не удалась.</b>",
            parse_mode=ParseMode.HTML
        )
        await state.clear()
    else:
        await send_complaints_from_all_accounts(session_files, link, message)
        await state.clear()

@router.callback_query(lambda c: c.data == 'back')
async def handle_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await start_command(callback_query.message, state)

@router.callback_query(lambda c: c.data == 'profile')
async def handle_profile(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    user_id = callback_query.from_user.id
    subscription_status = "Активная" if user_id in admins or check_subscription(user_id) else "Неактивная"
    keyboard = back_button_keyboard()
    await callback_query.message.answer(
        f"<b>🆔 ID:</b> <code>{user_id}</code>\n<b>⭐️ Ваша подписка:</b> <code>{subscription_status}</code>",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@router.callback_query(lambda c: c.data == 'emailsnos')
async def emailsnos(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(Form.waiting_for_email_text)
    keyboard = back_button_keyboard()
    await callback_query.message.answer(
        "<b>✉️ Введите текст для отправки на почту:</b>",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@router.message(Form.waiting_for_email_text)
async def handle_email_text_submission(message: types.Message, state: FSMContext):
    subject = "Тест"
    email_text = message.text
    user_id = message.from_user.id

    await state.clear()

    emails_file = 'emails.txt'
    receivers = ["support@telegram.org", "abuse@telegram.org"]

    with open(emails_file, 'r') as file:
        lines = file.readlines()

    success_count = 0
    error_messages = []
    response_message = (
        f"<b>Ваш текст:</b> <code>{email_text}</code>\n"
        f"Письма отправлены: {success_count}"
    )
    sent_message = await message.answer(response_message, parse_mode=ParseMode.HTML)

    for line in lines:
        sender_email, sender_password = line.strip().split(':')
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        success, error_message = await send_email(smtp_host, smtp_port, sender_email, sender_password, receivers[0], subject, email_text)

        if success:
            success_count += 1
            response_message = (
                f"<b>Ваш текст:</b> <code>{email_text}</code>\n"
                f"Письма отправлены: {success_count}"
            )
            await sent_message.edit_text(response_message, parse_mode=ParseMode.HTML)
        else:
            error_messages.append(f"Ошибка при отправке от {sender_email}: {error_message}")
    if success_count == len(lines):
        final_message = f"🎉 Все {success_count} письма отправлены успешно!"
        await sent_message.delete()
        await message.answer(final_message)

    if error_messages:
        await message.answer("\n".join(error_messages))

@router.callback_query(lambda c: c.data == "websnos")
async def websnos(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(Form.waiting_for_support_message)
    keyboard = back_button_keyboard()
    await callback_query.message.answer(
        "<b>✉️ Введите сообщение для отправки в поддержку:</b>",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@router.message(Form.waiting_for_support_message)
async def handle_support_message_submission(message: types.Message, state: FSMContext):
    support_message = message.text
    user_id = message.from_user.id

    await state.clear()

    response_message = (
        f"<b>Ваше сообщение для поддержки:</b>\n<code>{support_message}</code>"
    )

    sent_message = await message.answer(response_message, parse_mode=ParseMode.HTML)

    for count in range(1, 51):
        email = faker.email()
        phone = faker.phone_number()
        url = 'https://telegram.org/support'
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
                'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            ]),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'email': email,
            'phone': phone,
            'message': support_message
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            edit_message = f"Ваше сообщение отправлено на поддержки телеграм\nВсего: {count}"
            await sent_message.edit_text(edit_message, parse_mode=ParseMode.HTML)

@router.message(Command("addsub"))
async def add_subscription_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    if user_id not in admins:
        await message.answer("❌ У вас нет прав для выполнения этой команды.")
        return
    args = message.text.split()
    if len(args) < 3 or len(args) > 4:
        await message.answer("❌ Неправильное использование. Пример: /addsub <id> <тип 1d, 7d или 30d>")
        return
    target_user_id = args[1]
    duration = args[2]
    try:
        if duration.endswith('d'):
            days = int(duration[:-1])
            expiration_date = datetime.now() + timedelta(days=days)
        else:
            await message.answer("❌ Неправильный тип. Используйте 1d, 7d или 30d.")
            return
    except ValueError:
        await message.answer("❌ Неправильный тип. Используйте 1d, 7d или 30d.")
        return
    add_subscription(target_user_id, expiration_date)
    await message.answer(f"✅ Подписка на пользователя <code>{target_user_id}</code> успешно добавлена до <code>{expiration_date.isoformat()}</code>.", parse_mode=ParseMode.HTML)

@router.message(Command("whitelist"))
async def whitelist_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in admins:
        await message.answer("❌ У вас нет прав для выполнения этой команды.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.answer("❌ Неправильное использование. Пример: /whitelist <id>")
        return
    target_user_id = args[1]
    if is_whitelisted(target_user_id):
        await message.answer(f"✅ Пользователь <code>{target_user_id}</code> уже в вайт-листе.", parse_mode=ParseMode.HTML)
    else:
        add_to_whitelist(target_user_id)
        await message.answer(f"✅ Пользователь <code>{target_user_id}</code> добавлен в вайт-лист.", parse_mode=ParseMode.HTML)

@router.message(Command("subscribe"))
async def subscribe(message: types.Message, state: FSMContext):
    subscription_info = """
    <b>💰 Цены на подписку сносер:

☀ 1d - 2$
⭐️ 7d - 4$
⚡️ 1month - 6$
🔥 6month - 10$
💥 1 year - 20$

📋 white list - 3$

❔ Что такое white list?

White list - при покупке данной функции вас нельзя будет снести через нашего бота, а так же вам придет уведомление с юзернеймом человека, который попытается это сделать.

За покупкой чего либо из списка обращаться только к: @RainSu , @archihz , @Banzaikzfd

Оплату принимаем только: @send , kaspi kz.</b>
    """
    await message.answer(subscription_info, parse_mode=ParseMode.HTML)