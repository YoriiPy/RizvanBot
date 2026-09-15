from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import database
from database import requests
router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await requests.add_user(message.from_user.id, message.from_user.first_name)
    await message.answer("🦍 Вас приветствует бот Ризвана\n"
                         "💫 Я сообщу когда начнется стрим\n"
                         "🚀 Вы не пропустите ни одного стрима")
