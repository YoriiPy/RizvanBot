from re import search

from aiogram import Bot, Router
from aiogram.types import Message
from database import requests
from keyboards import  user_keyboards
import func
router = Router()

async def broadcast_to_users(bot: Bot):
    users = await requests.get_users_broadcast()
    if users:
        result = func.is_live()
        if result:
            for user_id in users:
                await bot.send_message(text=
                                       "✅ Началась трансляция Ризвана 🦍\n"
                                       "👀 Заходи на стрим\n\n"
                                       f"<b>💫 Ссылка на стрим</b> - <a href=https://www.youtube.com/@SkyNews/live>", parse_mode="HTML", reply_markup=user_keyboards.get_url(), chat_id=user_id)
                await requests.update_state_stream(1)
        else:
            await requests.update_state_stream(0)
