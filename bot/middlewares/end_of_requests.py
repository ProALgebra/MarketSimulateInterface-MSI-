from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.cache import Cache
from bot.structures.data_structure import TransferData

import logging

class EndOfRequestsMiddleware(BaseMiddleware):
    """ This class is responsible for the end of the previous request to GPT """
    REQUESTS_WORK = 1
    REQUESTS_DONE = 0
    SENT_THROTTLED_MESSAGE = 2

    TIME_OUT = 120

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: TransferData,
    ) -> Any:
        cache: Cache = data.get("cache")

        user_id = event.from_user.id
        radis_key = f"{user_id}_end_of_requests"

        user_session = await cache.user_client.get(radis_key)

        if user_session:
            user_session = int(user_session.decode())
            if user_session == self.REQUESTS_WORK:
                await event.answer(_('await_response_massage'))
                await cache.user_client.set(radis_key, self.SENT_THROTTLED_MESSAGE, self.TIME_OUT)
                return
            elif user_session == self.SENT_THROTTLED_MESSAGE:
                pass

        await cache.user_client.set(radis_key, self.REQUESTS_WORK, self.TIME_OUT)

        handler_continue = None

        try:
            handler_continue = await handler(event, data)
        except Exception as err:
            logging.exception(err)
        finally:
            await cache.user_client.delete(radis_key)
            return handler_continue
