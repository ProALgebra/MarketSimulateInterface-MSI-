from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.dispatcher.flags import get_flag


import keyboards as kb
from structures.data_structure import TransferData

from shared.dbs.postgres.repositories.users import UserRepo


class RegistrationsMiddleware(BaseMiddleware):
    """ Checking whether the users are registered in the database """
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: TransferData,
    ) -> Any:
        enable_registrations = get_flag(data, "registrations")

        if enable_registrations is not None and not enable_registrations:
            return await handler(event, data)

        bot: Bot = data.get("bot")
        async with data.get("pool")() as session:
            user_repo: UserRepo = UserRepo(session)
            exists = await user_repo.exists_check_by_tg_id(event.from_user.id)
            if not exists:
                await bot.send_message(chat_id=event.from_user.id,
                                       text=_('REGISTRATIONS_MESSAGE'),
                                       reply_markup=kb.registrations())
                return False

        return await handler(event, data)
