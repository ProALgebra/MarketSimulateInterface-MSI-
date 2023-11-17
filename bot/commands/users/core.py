from typing import Union

from datetime import datetime

from uuid import UUID

from sandbox_worker.worker import run_sandbox

from shared.dbs.minio.zip_repository import ZipRepository
from shared.dbs.minio.client import client

import io

from aiogram import F, types, Router, Bot
from aiogram.types import ContentType
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F, Router, types
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from shared.dbs.postgres.repositories.task import AsyncTaskRepository
from commands.commandName import (CORE_START, CORE_SOURCE, CORE_CASH, CORE_COMMISIONS, CORE_TEST)
from filters import ChatTypeFilter
from callbacks import CoreStepData
from states import CoreSetup
import keyboards as kb

core_router = Router()


@core_router.callback_query(CoreStepData.filter(), CoreSetup.choise)
@core_router.callback_query(CoreStepData.filter(), CoreSetup.start_cash)
@core_router.callback_query(CoreStepData.filter(), CoreSetup.commission)
async def choise(callback_query: types.CallbackQuery,
                 callback_data: CoreStepData,
                 state: FSMContext,
                 bot: Bot,
                 task_repo: AsyncTaskRepository):
    if callback_data.step == CORE_SOURCE:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=_('SOURCE'))
        await state.set_state(CoreSetup.source)
        return

    if callback_data.step == CORE_CASH:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=_('START_CASH'))
        await state.set_state(CoreSetup.start_cash)
        return

    if callback_data.step == CORE_COMMISIONS:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=_('COMMISSION'))
        await state.set_state(CoreSetup.commission)
        return

    if callback_data.step == CORE_TEST:
        data = await state.get_data()
        date_start: str = data['date_start']
        date_end: str = data['date_end']
        commission: float = data['commission']
        start_cash: float = data['start_cash']

        uuid4: UUID = await task_repo.insert_task(user_id=int(callback_query.from_user.id),
                                                  date_from=datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"),
                                                  date_to=datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S"),
                                                  commission=float(commission),
                                                  start_cash=float(start_cash))

        zip_repo: ZipRepository = ZipRepository(client=client)
        zip: bytes = zip_repo.get_zip_by_task_id("7f5ec5ba-cdf0-4ce9-939f-1ccc4308b968")
        zip_repo.put_zip(uuid4, io.BytesIO(zip), len(zip))

        run_sandbox.send(str(uuid4))

        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=_('CORE_GET_START_CALCULATE'))
        await state.set_state()
        return

@core_router.message(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    Command(CORE_START),
    flags={"chat_action": "typing"})
@core_router.message(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    F.text==__(CORE_START),
    flags={"chat_action": "typing"})
async def cmd_core_start(message: types.Message,
                         state: FSMContext):
    await state.set_state(CoreSetup.data_start)
    await message.answer(text=_('START_CORE_MESSAGE'),
                         reply_markup= await SimpleCalendar().start_calendar())

@core_router.callback_query(SimpleCalendarCallback.filter(), CoreSetup.data_start)
async def set_start_date(callback_query: CallbackQuery,
                         callback_data: CallbackData,
                         state: FSMContext,
                         bot: Bot):
    select, date_start = await SimpleCalendar().process_selection(callback_query, callback_data)

    if not select:
        return

    if date_start > datetime(day=12, month=11, year=2023):
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=_('INVALIDE_START_MESSAGE'),
                                    reply_markup= await SimpleCalendar().start_calendar())
        return

    def convert_to_date_format(date: datetime) -> str:
        date = date.replace(hour=7, minute=0, second=0, microsecond=0)
        return str(date)

    await state.update_data({'date_start': convert_to_date_format(date_start)})
    await state.set_state(CoreSetup.data_end)

    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=_('END_DATA_CORE'),
                                reply_markup= await SimpleCalendar().start_calendar())

@core_router.callback_query(SimpleCalendarCallback.filter(), CoreSetup.data_end)
async def set_end_date(callback_query: CallbackQuery,
                       callback_data: CallbackData,
                       state: FSMContext,
                       bot: Bot):
    select, date_end = await SimpleCalendar().process_selection(callback_query, callback_data)

    if not select:
        return

    data: dict = await state.get_data()
    date_start: datetime = data['date_start']

    if datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S") >= date_end:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=_('INVALIDE_END_MESSAGE'),
                                    reply_markup= await SimpleCalendar().start_calendar())
        return

    if date_end > datetime(day=12, month=11, year=2023):
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=_('INVALIDE_END_MESSAGE_FEUTERES'),
                                    reply_markup= await SimpleCalendar().start_calendar())
        return

    def convert_to_date_format(date: datetime) -> str:
        date = date.replace(hour=7, minute=0, second=0, microsecond=0)
        return str(date)

    await state.update_data({'date_end': convert_to_date_format(date_end)})
    await state.set_state(CoreSetup.choise)

    commisions = True if 'commission' in data.keys() else False
    cash = True if 'start_cash' in data.keys() else False

    await bot.send_message(text=_('CHOISE'),
                           chat_id=callback_query.message.chat.id,
                           reply_markup=kb.core_step(source=commisions and cash))

@core_router.message(CoreSetup.commission)
async def set_commission(message: types.Message, state: FSMContext):
    def isFloat(data):
        try:
            float(data)
            return True
        except:
            return False

    commission: float = message.text

    if not isFloat(commission):
        await message.answer(text=_('INVALID_COMMISION'))
        return

    await state.update_data({'commission': commission})
    await state.set_state(CoreSetup.start_cash)

    data: dict = await state.get_data()
    await state.set_state(CoreSetup.choise)

    commisions = True if 'commission' in data.keys() else False
    cash = True if 'start_cash' in data.keys() else False

    await message.answer(text=_('CHOISE'),
                         reply_markup=kb.core_step(source=commisions and cash))

@core_router.message(CoreSetup.start_cash)
async def set_start_cash(message: types.Message, state: FSMContext):

    def isFloat(data):
        try:
            float(data)
            return True
        except:
            return False

    start_cash: float = message.text

    if not isFloat(start_cash):
        await message.answer(text=_('INVALID_SOURCE'))
        return

    await state.update_data({'start_cash': start_cash})
    data: dict = await state.get_data()
    await state.set_state(CoreSetup.choise)

    commisions = True if 'commission' in data.keys() else False
    cash = True if 'start_cash' in data.keys() else False

    await message.answer(text=_('CHOISE'),
                         reply_markup=kb.core_step(source=commisions and cash))

@core_router.message(CoreSetup.source, F.content_type==ContentType.DOCUMENT)
async def set_source(message: types.Message,
                     bot: Bot,
                     state: FSMContext,
                     task_repo: AsyncTaskRepository):
    file_in_io = io.BytesIO()
    file = await bot.get_file(file_id=message.document.file_id)

    await message.bot.download_file(file_path=file.file_path,
                                    destination=file_in_io)

    data = await state.get_data()
    date_start: str = data['date_start']
    date_end: str = data['date_end']
    commission: float = data['commission']
    start_cash: float = data['start_cash']

    uuid4: UUID = await task_repo.insert_task(user_id=int(message.from_user.id),
                                              date_from=datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"),
                                              date_to=datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S"),
                                              commission=float(commission),
                                              start_cash=float(start_cash))

    zip_repo: ZipRepository = ZipRepository(client=client)
    zip_repo.put_zip(uuid4, file_in_io, file.file_size)

    run_sandbox.send(str(uuid4))

    await message.reply(_('CORE_GET_START_CALCULATE'))

    await state.set_state()

@core_router.message(CoreSetup.source)
async def set_source(message: types.Message):
    await message.reply(_('INVALID_SOURCE'))
