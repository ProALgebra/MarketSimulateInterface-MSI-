from typing import Union

from aiogram import types, Router, Bot
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F, Router, types
from aiogram.utils.i18n import gettext as _

from bot.commands.commandName import CANCEL_COMMAND
from bot.filters import ChatTypeFilter

user_cancel_router = Router()


@user_cancel_router.message(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    Command(CANCEL_COMMAND),
    flags={"chat_action": "typing"})
@user_cancel_router.callback_query(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    F.text==CANCEL_COMMAND,
    flags={"chat_action": "typing"})
async def cmd_cancel(event: Union[types.Message, types.CallbackQuery], state: FSMContext, bot: Bot):
    """ Cancel FSM """
    data = await state.get_data()
    await state.clear()

    await state.update_data({'locale': data['locale']})

    await bot.send_message(chat_id=event.from_user.id,
                           text=_('CANCEL_MESSAGE'),
                           disable_notification=True)
