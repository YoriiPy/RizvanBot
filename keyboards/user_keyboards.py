from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import requests as rq
import asyncio

def get_url():
    url = asyncio.run(rq.get_url_stream())
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Стрим 🦍", url=f"{url}")
    return keyboard.as_markup()
