from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database import models
from bot_broadcast import broadcast
from keyboards import user_keyboards
import os
import asyncio


file = load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():

    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()

    await dispatcher.start_polling(bot)
    await dispatcher.include_router(broadcast.router)
if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(models.init_db())
    asyncio.run(user_keyboards.get_url())
