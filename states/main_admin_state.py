from aiogram.fsm.state import StatesGroup, State


class states(StatesGroup):
    wait_new_url = State()