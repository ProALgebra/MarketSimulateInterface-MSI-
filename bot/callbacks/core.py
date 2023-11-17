from aiogram.filters.callback_data import CallbackData


class CoreStepData(CallbackData, prefix='core_step'):
    step: str
