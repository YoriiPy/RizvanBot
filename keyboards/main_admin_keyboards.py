from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🚀 Поменять значение URL", callback_data="edit_stream_url")
    keyboard.button(text="👀 Состояние стрима", callback_data="check_stream")
    keyboard.button(text="👮 Добавить main admin", callback_data="add_main_admin")
    keyboard.as_markup(1, 1, 1)
    return keyboard.as_markup()

def return_start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Назад", callback_data="back_start")
    return keyboard.as_markup()