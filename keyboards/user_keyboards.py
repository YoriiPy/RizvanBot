from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import requests as rq
import asyncio

async def get_url():
    url = await rq.get_channel_name()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Стрим 🦍", url=f"{url}")
    return keyboard.as_markup()

async def get_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="👀 Состояние стрима", callback_data="check_stream")
    return keyboard.as_markup()