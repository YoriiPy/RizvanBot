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

lists = []
router = Router()
broadcast = False
db = False

async def broadcast_to_users(bot: Bot):
    global db, lists
    if db is False:
        await models.init_db()
        db = True
    global broadcast
    users = await rq.get_users_broadcast()

    if not users:
        return

    live = await func.is_live()

    # Стрим начался
    if not broadcast and live:
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
                continue


            # Пропускаем тех, кто заблокировал бота




        broadcast = True


        while broadcast and live:
            global lists
            message1 = await bot.send_message(chat_id=-1002198546061, text=text, parse_mode="HTML")
            message2 = await bot.send_message(chat_id=-1002179134100, text=text, parse_mode="HTML")
            lists.append(message1)
            lists.append(message2)
            live = await func.is_live()
            if not live:
                break
            await asyncio.sleep(2400)

    # Стрим закончился
    if broadcast and not live:
        global lists

        # Создаём список прямо с сообщениями:


        # Проходимся по каждому сообщению по очереди:
        for msg in lists:
            try:
                await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
            except Exception:
                pass

        # Сбрасываем флаг ОДИН РАЗ после того, как цикл завершился:
        lists.clear()
        broadcast = False








async def main():
    load_dotenv("../.env")
    TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=broadcast_to_users, trigger="interval", seconds=60, kwargs={"bot": bot}, next_run_time=datetime.datetime.now())
    scheduler.start()


