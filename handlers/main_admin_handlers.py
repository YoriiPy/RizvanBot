from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards import main_admin_keyboards as kb
from states import main_admin_state as st
from database import requests as rq

router = Router()

# ПОМЕНЯТЬ URL
@router.callback_query(F.data == "edit_stream_url")
async def data_url(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text("✅ Отправьте URL стрима нового канала", reply_markup=kb.return_start_keyboard())
    await state.set_state(st.states.wait_new_url)

@router.message(st.states.wait_new_url)
async def update_url(message: Message, state: FSMContext):
    URL = message.text
    if URL.isdigit():
        await rq.edit_url_stream(URL)
        await message.answer("✅ Успешно сохранено", reply_markup=kb.return_start_keyboard())
        await state.clear()
    else:
        await message.answer("❌ Отправьте строку", reply_markup=kb.return_start_keyboard())
        await state.clear()

