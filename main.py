import logging
import asyncio
from aiogram import Bot, Router, Dispatcher
from database import create_db
import config
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
router = Router()
dp = Dispatcher()

async def main():
    create_db()
    register_handlers(router, bot)
    dp.include_router(router)
    
    try:
        await dp.start_polling(bot)
    finally:
        pass

if __name__ == '__main__':
    asyncio.run(main())