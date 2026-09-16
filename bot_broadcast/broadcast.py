from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message
from database import requests
from keyboards import  user_keyboards
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_broadcast import func
import asyncio

router = Router()
IsLive = False

async def broadcast_to_users(bot: Bot):
    users = await requests.get_users_broadcast()
    global IsLive
    try:
        if users:
            checking = await func.is_live()
            if IsLive is False and checking is True:
                for user_id in users:
                    await bot.send_message(text=
                                           "✅ Началась трансляция Ризвана 🦍\n"
                                           "👀 Заходи на стрим\n\n"
                                           f'<b>💫 Ссылка на стрим</b> - <a href="https://www.youtube.com/@SkyNews/live>"', parse_mode="HTML", reply_markup=user_keyboards.get_url(), chat_id=user_id)
                    await asyncio.sleep(0.05)
                IsLive = True
            if IsLive is True and checking is False:
                IsLive = False
    except (TelegramBadRequest, TelegramForbiddenError):
        pass


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=broadcast_to_users, trigger="interval", seconds=60)
    scheduler.start()
    while True:
        await asyncio.sleep(1)