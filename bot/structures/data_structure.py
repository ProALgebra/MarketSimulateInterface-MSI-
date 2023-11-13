from typing import Callable, TypedDict

from aiogram import Bot

from sqlalchemy.ext.asyncio import AsyncSession

from bot.cache import Cache
from bot.data_base import Database


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    db: Database
    bot: Bot
    cache: Cache
