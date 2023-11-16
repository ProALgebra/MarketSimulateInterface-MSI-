from uuid import UUID

from aiogram.filters.callback_data import CallbackData

class LanguageData(CallbackData, prefix='language'):
    language_code: str

class TasksData(CallbackData, prefix='task'):
    task_id: UUID

class PaginationData(CallbackData, prefix='page'):
    direction: str
