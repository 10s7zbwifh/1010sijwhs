from telethon import TelegramClient
import re

api_id = '14960174'
api_hash = '7200e9b88534a2101fc8657af3677b38'
session_name = '+972537097954'

client = TelegramClient(session_name, api_id, api_hash)

async def get_sender_id(link):
    try:
        await client.start()
        match = re.match(r'https://t.me/(.+?)/(\d+)', link)
        if match:
            channel = match.group(1)
            message_id = int(match.group(2))
            message = await client.get_messages(channel, ids=message_id)
            # Извлекаем ID отправителя (если он существует)
            return message.from_id.user_id if message.from_id else None
    except Exception as e:
        print(f"Error retrieving sender ID: {e}")
    return None