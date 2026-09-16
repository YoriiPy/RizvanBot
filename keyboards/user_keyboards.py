from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_url():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Стрим 🦍", url=f"{get_url()}")
    return keyboard
