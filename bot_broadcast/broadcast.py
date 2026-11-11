import datetime
import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import requests as rq, models
from keyboards import user_keyboards as userkb
from bot_broadcast import func

lists = []
router = Router()
broadcast = False
db = False
xz = 0


async def broadcast_to_users(bot: Bot):
    global db, lists, broadcast, xz

    if not db:
        await models.init_db()
        db = True

    users = await rq.get_users_broadcast()
    if not users:
        return

    live = await func.is_live()

    # Стрим начался
    if not broadcast and live:
        channel_name = await rq.get_channel_name()
        url = live if isinstance(live, str) and live.startswith("http") else f"https://www.youtube.com/@{channel_name}/live"
        url_markup = await userkb.get_url()

        text = (
            "✅ Началась трансляция Ризвана 🦍\n"
            "👀 Заходи на стрим\n\n"
           f'💫 Ссылка: {url}'
        )

        for user_id in users:
            try:
                message = await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    parse_mode="HTML",
                    reply_markup=url_markup
                )
                lists.append(message)
                await asyncio.sleep(0.05)
            except (TelegramBadRequest, TelegramForbiddenError):
                continue

        broadcast = True

        # Отправка в канал с защитой от прав администратора
        try:
            channel_id = await rq.get_channel_id()
            if channel_id:
                message = await bot.send_message(
                    chat_id=channel_id,
                    text=text,
                    reply_markup=url_markup,
                    parse_mode="HTML"
                )
                lists.append(message)
        except Exception as e:
            print(f"Ошибка отправки в канал: {e}")

    # Стрим идёт (счетчик напоминания)
    if broadcast and live:
        xz += 1

    # Напоминание через 90 минут
    if xz == 90:
        channel_name = await rq.get_channel_name()
        stream_url = f"https://www.youtube.com/@{channel_name}/live"
        url_markup = await userkb.get_url()

        try:
            channel_id = await rq.get_channel_id()
            if channel_id:
                message1 = await bot.send_message(
                    chat_id=channel_id,
                    text=(
                        "🤦 Не зашел на стрим\n"
                        "❌ Фатальная ошибка\n"
                        f'🦍 <a href="{stream_url}">Заходи на стрим</a> 🧆'
                    ),
                    parse_mode="HTML",
                    reply_markup=url_markup
                )
                lists.append(message1)
        except Exception as e:
            print(f"Ошибка отправки напоминания в канал: {e}")

        xz = 0

    # Стрим закончился
    if broadcast and not live:
        for msg in lists:
            try:
                await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
            except Exception:
                pass

        lists.clear()
        xz = 0
        broadcast = False


async def main():
    load_dotenv("../.env")
    TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=broadcast_to_users,
        trigger="interval",
        seconds=60,
        kwargs={"bot": bot},
        next_run_time=datetime.datetime.now()
    )
    scheduler.start()

