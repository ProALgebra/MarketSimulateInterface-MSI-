from typing import Any, Awaitable, Callable, Dict, Union

import logging

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from structures.data_structure import TransferData

from shared.dbs.postgres.repositories.users import UserRepo

class UserConnectionsMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler"""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: TransferData,
    ) -> Any:
        async with data.get("pool")() as session:
            try:
                data["user_repo"] = UserRepo(session)
                return await handler(event, data)
            except Exception as error:
                logging.exception(error)
            finally:
                await session.commit()
