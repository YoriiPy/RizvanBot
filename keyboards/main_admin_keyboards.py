from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🚀 Поменять YouTube канал", callback_data="edit_stream_url")
    keyboard.button(text="👀 Проверить статус эфира", callback_data="check_stream")
    keyboard.button(text="🤖 Поменять Telegram канал", callback_data="edit_tg_channel")

    keyboard.adjust(1, 1, 1)
    return keyboard.as_markup()

def return_start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Назад", callback_data="back_start")
    return keyboard.as_markup()