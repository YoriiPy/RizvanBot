from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import main_admin_keyboards as mdkb
import database
from database import requests
router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await requests.add_user(message.from_user.id, message.from_user.first_name)
    if message.from_user.id != 8461039529:
        await message.answer("🦍 Вас приветствует бот Ризвана\n"
                             "💫 Я сообщу когда начнется стрим\n"
                             "🚀 Вы не пропустите ни одного стрима")
        return
    await message.answer("🦍 Вас приветствует бот Ризвана\n"
                         "💫 Я сообщу когда начнется стрим\n"
                         "🚀 Вы не пропустите ни одного стрима", reply_markup=mdkb.start_keyboard())
