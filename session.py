import os

# Получение пути к текущему файлу
current_file_path = os.path.abspath(__file__)

print(f"Путь к текущему файлу: {current_file_path}")

from telethon import TelegramClient

session_name = '+77029244504'  # Имя файла сессии без расширения
api_id = 21022746
api_hash = "b17d2c59286c767051098e348abe8503"

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await client.start()
    print("Вы вошли в систему!")

with client:
    client.loop.run_until_complete(main())
