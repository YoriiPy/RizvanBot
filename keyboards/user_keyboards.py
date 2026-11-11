from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import func as fc
import asyncio

async def get_url():
    url = await fc.get_url()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Стрим 🦍", url=f"{url}")
    return keyboard.as_markup()

async def get_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="👀 Проверить статус эфира", callback_data="check_stream")
    return keyboard.as_markup()