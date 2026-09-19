from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import user_handlers, admin_handlers, main_admin_handlers
from database import models
from bot_broadcast import broadcast
from keyboards import user_keyboards
from handlers.user_handlers import router as user_router
from handlers.main_admin_handlers import router as admin_router
import os
import asyncio



file = load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    # 1. Сначала запускаем базу данных и обновляем ссылки в клавиатурах
    await models.init_db()

    # 2. Инициализируем бота
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()

    dispatcher.include_router(user_router)
    dispatcher.include_router(admin_router)
    # 3. Запускаем бесконечный опрос серверов Telegram
    dispatcher.startup.register(broadcast.main)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


