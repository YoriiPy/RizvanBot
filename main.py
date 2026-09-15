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
    # 1. Сначала запускаем базу данных и обновляем ссылки в клавиатурах
    await models.init_db()
    await user_keyboards.get_url()

    # 2. Инициализируем бота
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()

    dispatcher.include_router(broadcast.router)

    # 3. Запускаем бесконечный опрос серверов Telegram
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(models.init_db())
    asyncio.run(user_keyboards.get_url())
