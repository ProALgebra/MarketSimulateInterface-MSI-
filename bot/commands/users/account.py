from typing import Union

from aiogram import F, Router, types
from aiogram import types, Router, Bot
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from filters.chat_type_filter import ChatTypeFilter
from shared.dbs.postgres.repositories.users import UserRepo
from shared.dbs.postgres.repositories.task import AsyncTaskRepository
from shared.dbs.postgres.models.users import Users
from shared.dbs.postgres.models.task import Tasks
from commands.commandName import (GET_PROFILE, CHANGE_LANGUAGE, GET_HISTORY, CHANGE_NAME)
from callbacks import LanguageData, PaginationData, TasksData
from states import SetName
import keyboards as kb


account_router = Router()


@account_router.message(Command(GET_PROFILE), flags={"chat_action": "typing"})
@account_router.message(F.text==__(GET_PROFILE), flags={"chat_action": "typing"})
async def get_profile(message: types.Message, user_repo: UserRepo):
    user: Users = await user_repo.get_by_tg_id(message.from_user.id)
    profile: str = _(GET_PROFILE + " {}: {}").format(user.name, user.commisions)
    await message.answer(text=profile)

@account_router.message(Command(GET_HISTORY), flags={"chat_action": "typing"})
@account_router.message(F.text==__(GET_HISTORY), flags={"chat_action": "typing"})
async def get_history(message: types.Message, task_repo: AsyncTaskRepository, state: FSMContext):
    tasks: list[Tasks] = await task_repo.get_tasks_by_user(message.from_user.id)

    if not tasks:
        await message.answer(text=_('NO_HISTORY'))
        return

    await state.update_data({'limit': 3, 'offset': 0})
    await message.answer(text=_(GET_HISTORY), reply_markup=kb.tasks(tasks=tasks))

@account_router.callback_query(PaginationData.filter(), flags={"chat_action": "typing"})
async def channel_navigation(
    callback: types.CallbackQuery,
    callback_data: PaginationData,
    task_repo: AsyncTaskRepository,
    state: FSMContext
):
    await callback.answer()
    data = await state.get_data()

    tasks: list[Tasks] = await task_repo.get_tasks_by_user(callback.from_user.id)

    offset = data['offset']
    limit = data['limit']

    if callback_data.direction == 'prev':
        if offset == 0:
            return

        offset -= limit

        await state.update_data({'offset': offset})
        await callback.message.edit_reply_markup(
            reply_markup=kb.tasks(tasks, offset=offset)
        )
    if callback_data.direction == 'next':
        if offset + limit >= len(tasks):
            return

        offset += limit

        await state.update_data({'offset': offset})
        await callback.message.edit_reply_markup(
            reply_markup=kb.tasks(tasks, offset=offset)
        )

@account_router.callback_query(TasksData.filter(), flags={"chat_action": "typing"})
async def research_task_info(
    callback: types.CallbackQuery,
    task_repo: AsyncTaskRepository,
    callback_data: TasksData,
    state: FSMContext,
):
    await callback.answer()
    data = await state.get_data()

    offset = data['offset']
    limit = data['limit']

    task: Tasks = await task_repo.get_task_by_id(callback_data.task_id)
    tasks: list[Tasks] = await task_repo.get_tasks_by_user(callback.from_user.id)

    await callback.message.edit_text(
        text=str(task.result),
        reply_markup=kb.tasks(tasks=tasks, offset=offset, limit=limit)
    )

@account_router.message(Command(CHANGE_LANGUAGE), flags={"chat_action": "typing"})
@account_router.message(F.text==__(CHANGE_LANGUAGE), flags={"chat_action": "typing"})
async def change_local(message: types.Message):
    await message.answer(text=_('ask_for_language'),
                         reply_markup=kb.language())

@account_router.callback_query(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    LanguageData.filter(),
    flags={"chat_action": "typing", "registrations": False})
async def cmd_set_local(callback: types.CallbackQuery,
                        callback_data: LanguageData,
                        state: FSMContext,
                        bot: Bot):
    locale = callback_data.language_code
    await callback.answer(locale)
    await state.update_data({'locale': locale})
    await bot.send_message(chat_id=callback.from_user.id,
                           text=_('language_set', locale=locale),
                           reply_markup=kb.main(locale=locale))

@account_router.message(Command(CHANGE_NAME), flags={"chat_action": "typing"})
@account_router.message(F.text==__(CHANGE_NAME), flags={"chat_action": "typing"})
async def change_name_start(message: types.Message, state: FSMContext):
    await message.answer(text=_('READ_NAME'),
                         reply_markup=kb.keep_name())
    await state.set_state(SetName.reading_name)

@account_router.message(F.text == __('keep_name'),
                        SetName.reading_name,
                        flags={"chat_action": "typing"})
async def keep_name(message: types.Message, state: FSMContext, user_repo: UserRepo):
    user: Users = await user_repo.get_by_tg_id(message.from_user.id)
    user.name = message.from_user.first_name

    first_name = message.from_user.first_name
    text = _('new_name_accepted {first_name}')
    text = text.format(first_name=first_name)

    await state.set_state()
    await message.answer(text,
                         reply_markup=kb.main())

@account_router.message(SetName.reading_name, flags={"chat_action": "typing"})
async def read_name(message: types.Message, state: FSMContext, user_repo: UserRepo):
    user: Users = await user_repo.get_by_tg_id(message.from_user.id)
    user.name = message.text

    text = _('new_name_accepted {first_name}')
    text = text.format(first_name=message.text)

    await state.set_state()
    await message.answer(text=text,
                         reply_markup=kb.main())
