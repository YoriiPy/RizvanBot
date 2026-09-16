from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_broadcast import func as fc
from database.requests import search_user, search_admin, search_main_admin
from keyboards import main_admin_keyboards as kb
from keyboards.user_keyboards import get_url
from keyboards import user_keyboards as userkb
from states import main_admin_state as st
from database import requests as rq

router = Router()

# ПОМЕНЯТЬ URL
@router.callback_query(F.data == "edit_stream_url")
async def data_url(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text("✅ Отправьте URL стрима нового канала", reply_markup=kb.return_start_keyboard())
    await state.set_state(st.states.wait_new_url)
    await state.update_data(message_id=callback.message.message_id)

@router.message(st.states.wait_new_url)
async def update_url(message: Message, state: FSMContext, bot: Bot):
    URL = message.text
    if not URL.isdigit():
        await rq.edit_url_stream(URL)

        data = await state.get_data()
        message_id = data.get("message_id")

        await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        await message.delete()


        await message.answer("✅ Успешно сохранено", reply_markup=kb.return_start_keyboard())
        await state.clear()
    else:
        await message.answer("❌ Отправьте строку", reply_markup=kb.return_start_keyboard())
        await state.clear()


@router.callback_query(F.data == "back_start")
async def back_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    if await search_main_admin(callback.from_user.id):
        await callback.message.edit_text(
            "🦍 Вас приветствует бот Ризвана\n"
            "💫 Я сообщу когда начнется стрим\n"
            "🚀 Вы не пропустите ни одного стрима",
            reply_markup=kb.start_keyboard()  # Клавиатура главного админа
        )


    elif await search_user(callback.from_user.id) or await search_admin(callback.from_user.id):
        await callback.message.edit_text(
            "🦍 Вас приветствует бот Ризвана\n"
            "💫 Я сообщу когда начнется стрим\n"
            "🚀 Вы не пропустите ни одного стрима",
            reply_markup=await userkb.get_keyboard()
        )


# СТРИМ

@router.callback_query(F.data == "check_stream")
async def send_state_stream(callback: CallbackQuery):
    url_keyboard = InlineKeyboardBuilder.from_markup(await get_url())
    back_keyboard = InlineKeyboardBuilder.from_markup(kb.return_start_keyboard())

    state_stream = await fc.is_live()
    if state_stream:
        keyboard = url_keyboard.attach(back_keyboard)
        keyboard = keyboard.as_markup()
        await callback.message.edit_text("✅ Стрим идет\nМожешь заходить", reply_markup=keyboard)
    else:

        await callback.message.edit_text("❌ Стрим выключен", reply_markup=back_keyboard.as_markup())

# ДОБАВЛЕНИЕ АДМИНОВ И ГЛАВ АДМИНОВ
@router.callback_query(F.data == "add_main_admin")
async def wait_send_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("👤 Отправьте ID для добавления в main admin", reply_markup=kb.return_start_keyboard())
    await state.set_state(st.states.wait_new_main_admin)

@router.callback_query(F.text == "add_admin")
async def wait_send_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("👤 Отправьте ID для добавления в main admin", reply_markup=kb.return_start_keyboard())
    await state.set_state(st.states.wait_new_main_admin)

@router.message(st.states.wait_new_main_admin)
async def add_main_admin_to_users(message: Message):
    user_id = message.from_user.id
    if await search_user(user_id) or await search_admin(user_id):
        await rq.add_main_admin(user_id, message.from_user.full_name)
        await message.answer("✅ Успешно добавлен")
    else:
        await message.answer("❌ Такого пользователя не существует")