from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🤖 bot-net Sn0s", callback_data='botnetsnos')
        ],
        [
            InlineKeyboardButton(text="📧 Email Sn0s", callback_data='emailsnos'),
            InlineKeyboardButton(text="🌐 Веб Sn0s", callback_data='websnos')
        ],
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data='profile'),
            InlineKeyboardButton(text="🔒 Админ", callback_data='admin_panel')
        ]
    ])

def back_button_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ])

def admin_panel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить в вайт-лист", callback_data='add_whitelist')],
        [InlineKeyboardButton(text="🎁 Выдать подписку", callback_data='give_subscription')],
        [InlineKeyboardButton(text="◀️ Назад", callback_data='back')]
    ])

def whitelist_users_keyboard(users) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for user in users:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=user['name'], callback_data=f'whitelist_user_{user["id"]}')])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data='admin_panel')])
    return keyboard

def whitelist_actions_keyboard(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Добавить в вайт-лист", callback_data=f'add_to_whitelist_{user_id}'),
            InlineKeyboardButton(text="❌ Удалить из вайт-листа", callback_data=f'remove_from_whitelist_{user_id}')
        ],
        [InlineKeyboardButton(text="◀️ Назад", callback_data='add_whitelist')]
    ])

def subscription_users_keyboard(users) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for user in users:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=user['name'], callback_data=f'subscription_user_{user["id"]}')])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data='admin_panel')])
    return keyboard

def subscription_actions_keyboard(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎁 Выдать подписку", callback_data=f'give_subscription_{user_id}'),
            InlineKeyboardButton(text="❌ Удалить подписку", callback_data=f'remove_subscription_{user_id}')
        ],
        [InlineKeyboardButton(text="◀️ Назад", callback_data='give_subscription')]
    ])

def subscription_duration_keyboard(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 день", callback_data=f'subscribe_{user_id}_1d'),
            InlineKeyboardButton(text="7 дней", callback_data=f'subscribe_{user_id}_7d')
        ],
        [
            InlineKeyboardButton(text="30 дней", callback_data=f'subscribe_{user_id}_30d'),
            InlineKeyboardButton(text="Навсегда", callback_data=f'subscribe_{user_id}_forever')
        ],
        [InlineKeyboardButton(text="◀️ Назад", callback_data=f'subscription_user_{user_id}')]
    ])