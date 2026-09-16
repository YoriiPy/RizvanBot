from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from keyboards import main_admin_keyboards as mdkb
import database
from database import requests as rq
router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await rq.add_user(message.from_user.id, message.from_user.first_name)
    if await rq.search_admin(message.from_user.id) or await rq.search_user(message.from_user.id):
        await message.answer("🦍 Вас приветствует бот Ризвана\n"
                             "💫 Я сообщу когда начнется стрим\n"
                             "🚀 Вы не пропустите ни одного стрима")
        return
    await message.answer("🦍 Вас приветствует бот Ризвана\n"
                         "💫 Я сообщу когда начнется стрим\n"
                         "🚀 Вы не пропустите ни одного стрима", reply_markup=mdkb.start_keyboard())
