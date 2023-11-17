from aiogram.fsm.state import State, StatesGroup

class SetName(StatesGroup):
    reading_name = State()
