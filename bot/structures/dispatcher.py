from typing import Optional

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.utils.chat_action import ChatActionMiddleware

from aioredis import Redis

from bot.middlewares import ThrottlingMiddleware, EndOfRequestsMiddleware
from bot.middlewares.callback_anwser import CallbackAnswerMiddleware
from bot.structures import conf
from bot.commands import routers


def get_redis_storage(redis: Redis, state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl):
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)


def get_dispatcher(
    storage: BaseStorage = MemoryStorage(),
    fsm_strategy: Optional[FSMStrategy] = FSMStrategy.CHAT,
    event_isolation: Optional[BaseEventIsolation] = None,
):
    dp = Dispatcher(
        storage=storage, fsm_strategy=fsm_strategy, events_isolation=event_isolation
    )

    dp.message.outer_middleware(EndOfRequestsMiddleware())
    dp.message.outer_middleware(ThrottlingMiddleware())

    dp.callback_query.outer_middleware(EndOfRequestsMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())

    dp.message.middleware(ChatActionMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())

    for router in routers:
        dp.include_router(router)

    return dp
