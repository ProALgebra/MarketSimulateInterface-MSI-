from aiogram.fsm.state import State, StatesGroup

class SetName(StatesGroup):
    reading_name = State()

class CoreSetup(StatesGroup):
    source = State()
    data_start = State()
    data_end = State()
    start_cash = State()
    commission = State()
