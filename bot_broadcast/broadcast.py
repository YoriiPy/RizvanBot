import datetime
import os

import dotenv
from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message
from dotenv import load_dotenv

from database import requests as rq, models
from keyboards import  user_keyboards
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_broadcast import func
import asyncio

router = Router()
IsLive = False
db = False

async def broadcast_to_users(bot: Bot):
    if db is False:
        await models.init_db()
    global IsLive
    users = await rq.get_users_broadcast()

    if not users:
        return

    checking = await func.is_live()

    # Стрим начался
    if not IsLive and checking:
        url_markup = await user_keyboards.get_url()
        channel_name = await rq.get_channel_name()
        text = (
            "✅ Началась трансляция Ризвана 🦍\n"
            "👀 Заходи на стрим\n\n"
            f'<b>💫 Ссылка на стрим</b> - <a href="https://www.youtube.com/@{channel_name}/live">Смотреть</a>'
        )

        for user_id in users:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    parse_mode="HTML",
                    reply_markup=url_markup
                )
                await asyncio.sleep(0.05)  # Защита от лимитов Telegram
            except (TelegramBadRequest, TelegramForbiddenError):
                continue  # Пропускаем тех, кто заблокировал бота

        IsLive = True

    # Стрим закончился
    elif IsLive and not checking:
        IsLive = False


async def main():
    load_dotenv("../.env")
    TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=broadcast_to_users, trigger="interval", seconds=60, kwargs={"bot": bot}, next_run_time=datetime.datetime.now())
    scheduler.start()
    await asyncio.Event().wait()

