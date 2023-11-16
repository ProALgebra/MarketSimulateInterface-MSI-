from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, CallbackQuery

from bot.structures.data_structure import TransferData


class CallbackAnswerMiddleware(BaseMiddleware):
    """ Class for disabling "Loading" in CallBack """
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            callback: CallbackQuery,
            data: TransferData,
    ) -> Any:
        bot: Bot = data.get("bot")
        handler_continue = None
        try:
            handler_continue = await handler(callback, data)
        finally:
            await bot.answer_callback_query(callback.id)
            return handler_continue
