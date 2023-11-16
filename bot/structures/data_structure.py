from typing import Callable, TypedDict

from aiogram import Bot

from sqlalchemy.ext.asyncio import AsyncSession

from bot.cache import Cache


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    bot: Bot
    cache: Cache
