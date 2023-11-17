from aiogram.fsm.state import State, StatesGroup

class CoreSetup(StatesGroup):
    source = State()
    data_start = State()
    data_end = State()
    choise = State()
    start_cash = State()
    commission = State()
