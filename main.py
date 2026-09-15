from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import asyncio


file = load_dotenv(dotenv_path="secretfiles/TOKEN.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():

    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()

    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())