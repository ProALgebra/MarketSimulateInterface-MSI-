from typing import Any, Awaitable, Callable, Dict, Union

import logging

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.structures.data_structure import TransferData

from shared.dbs.postgres.repositories.task import AsyncTaskRepository

class TasksConnectionsMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler"""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: TransferData,
    ) -> Any:
        # it doesn't fit well, but I won't rewrite it
        data["task_repo"] = AsyncTaskRepository(data.get("pool"))
        return await handler(event, data)

