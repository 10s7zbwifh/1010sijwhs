from telethon import TelegramClient, functions
from telethon.tl.types import InputReportReasonOther
from aiogram.types import Message
from aiogram.enums import ParseMode
import config
import aiosmtplib
from email.mime.text import MIMEText
import random
async def send_complaints_from_all_accounts(session_files, link, message):
    link_parts = link.split('/')
    chat_username = link_parts[-2]
    message_id = int(link_parts[-1])
    
    progress_message = await message.answer("<b>⏳ Начинаем отправку жалоб...</b>", parse_mode=ParseMode.HTML)
    
    total_complaints = len(session_files) * 150
    complaint_texts = ["Hello dear telegram support, today I want to complain about this person for violating the telegram rules, I ask you to ban this person in telegram, thanks in advance.", "Здравствуйте, уважаемая поддержка Telegram! Сегодня я хочу пожаловаться на данного человека за нарушение правил Telegram. Прошу вас заблокировать этого человека в Telegram. Заранее благодарю!"]
    complaint_text = random.choice(complaint_texts)
    
    for session_file in session_files:
        client = TelegramClient(session_file, config.API_ID, config.API_HASH)

        async with client:
            try:
                chat = await client.get_entity(chat_username)

                for i in range(150):
                    await client(functions.messages.ReportRequest(
                        peer=chat,
                        id=[message_id],
                        reason=InputReportReasonOther(),
                        message=complaint_text
                    ))
                    await progress_message.edit_text(f"<b>✅ Отправлено жалоб: {i + 1 + (session_files.index(session_file) * 150)}/{total_complaints}</b>", parse_mode=ParseMode.HTML)

            except ValueError as e:
                if "No user has" in str(e):
                    await message.answer(f"<b>❌ Ошибка: {chat_username} не найден.</b>")
                else:
                    await message.answer(f"<b>❌ Произошла ошибка: {str(e)}</b>")
            except Exception as e:
                await message.answer(f"<b>❌ Произошла неизвестная ошибка: {str(e)}</b>")

    await progress_message.edit_text(f"<b>🎉 Все {total_complaints} жалоб отправлены успешно!</b>", parse_mode=ParseMode.HTML)

async def send_email(smtp_host, smtp_port, sender_email, sender_password, recipient_email, subject, message):
    msg = MIMEText(message)
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    try:
        await aiosmtplib.send(
            msg,
            hostname=smtp_host,
            port=smtp_port,
            start_tls=True,
            username=sender_email,
            password=sender_password,
        )
        return True, None
    except Exception as e:
        return False, str(e)