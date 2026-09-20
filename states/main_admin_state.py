from aiogram.fsm.state import StatesGroup, State


class states(StatesGroup):
    wait_new_youtube_channel = State()
    wait_new_main_admin = State()
    wait_new_telegram_channel = State()