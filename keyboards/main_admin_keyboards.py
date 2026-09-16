from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🚀 Поменять значение URL", callback_data="edit_stream_url")
    return keyboard.as_markup()

def return_start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Назад", callback_data="back_start")
    return keyboard.as_markup()