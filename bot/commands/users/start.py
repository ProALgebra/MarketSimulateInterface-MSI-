from typing import Union

from aiogram import F, Router, types
from aiogram import types, Router, Bot
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandObject

from bot.filters.chat_type_filter import ChatTypeFilter
from shared.dbs.postgres.repositories.users import UserRepo
from bot.commands.commandName import START_COMMAND
from aiogram.utils.i18n import gettext as _

user_start_router = Router()

@user_start_router.message(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    Command(START_COMMAND),
    flags={"chat_action": "typing", "registrations": False})
@user_start_router.callback_query(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    F.text==START_COMMAND,
    flags={"chat_action": "typing", "registrations": False})
async def cmd_start(message: Union[types.Message, types.CallbackQuery], user_repo: UserRepo, bot: Bot):
    """
       Registers the users if he has not been registered yet. It also outputs basic commands for the bot's operation.
       :return:
       """
    is_user_exists = await user_repo.exists_check_by_tg_id(message.from_user.id)
    if not is_user_exists:
        await user_repo.new(telegram_id=message.from_user.id,
                            first_name=message.from_user.first_name)

    await bot.send_message(text=_('START_MESSAGE'), chat_id=message.from_user.id)
