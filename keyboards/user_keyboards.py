from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_url():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Стрим 🦍", url="https://www.youtube.com/@SkyNews/live")
    return keyboard
