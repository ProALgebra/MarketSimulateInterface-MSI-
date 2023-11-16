from typing import Union

from aiogram import F, types, Router, Bot
from aiogram.types import ContentType
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F, Router, types
from aiogram.utils.i18n import gettext as _
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from commands.commandName import CORE_START
from filters import ChatTypeFilter
from states import CoreSetup

core_router = Router()


@core_router.message(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    Command(CORE_START),
    flags={"chat_action": "typing"})
@core_router.message(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    F.text==CORE_START,
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

    await state.update_data({'date_start': str(date_start)})
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

    await state.update_data({'date_end': str(date_end)})
    await state.set_state(CoreSetup.commission)

    await bot.edit_message_text(text=_('COMMISSION'),
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id)

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

    await message.answer(text=_('START_CASH'))


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
    await state.set_state(CoreSetup.source)

    await message.answer(text=_('SOURCE'))

@core_router.message(CoreSetup.source, F.content_type==ContentType.DOCUMENT)
async def set_source(message: types.Message, bot: Bot, state: FSMContext):
    file_id = message.document.file_id
    file_name = message.document.file_name
    data = await state.get_data()
    file_info = await bot.get_file(file_id)
    file = file_info.file_path

    await message.reply('Документ zip был успешно обработан!')


@core_router.message(CoreSetup.source)
async def set_source(message: types.Message):
    await message.reply(_('INVALID_SOURCE'))
