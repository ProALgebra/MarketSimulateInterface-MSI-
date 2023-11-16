from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject, CallbackQuery

from bot.structures.data_structure import TransferData


class FSMStateMiddleware(BaseMiddleware):
    """ A class for clear FSM state """
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: TransferData,
    ) -> Any:
        state: FSMContext = data.get("state")
        await state.clear()
        return await handler(event, data)
