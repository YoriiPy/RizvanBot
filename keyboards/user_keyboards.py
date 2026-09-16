from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import requests as rq
import asyncio

async def get_url():
    url = await rq.get_url_stream()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Стрим 🦍", url=f"{url}")
    return keyboard.as_markup()
