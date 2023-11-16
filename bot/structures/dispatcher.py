from typing import Optional

import pathlib

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import FSMI18nMiddleware

from aioredis import Redis

from bot.middlewares import ThrottlingMiddleware, EndOfRequestsMiddleware
from bot.middlewares.callback_anwser import CallbackAnswerMiddleware

from bot.structures import conf
from bot.commands import routers

def get_redis_storage(redis: Redis, state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl):
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)

I18N_DOMAIN = 'mybot'
LOCALES_DIR = pathlib.Path(__file__).parents[1] / 'locales'

i18n = I18n(
    path=LOCALES_DIR,
    default_locale='ru',
    domain=I18N_DOMAIN
)

def get_dispatcher(
    storage: BaseStorage = MemoryStorage(),
    fsm_strategy: Optional[FSMStrategy] = FSMStrategy.CHAT,
    event_isolation: Optional[BaseEventIsolation] = None,
):
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=fsm_strategy,
        events_isolation=event_isolation
    )

    i18n_middleware = FSMI18nMiddleware(i18n)
    dp.message.outer_middleware.register(i18n_middleware)
    dp.callback_query.outer_middleware.register(i18n_middleware)

    dp.message.outer_middleware(EndOfRequestsMiddleware())
    dp.message.outer_middleware(ThrottlingMiddleware())

    dp.callback_query.outer_middleware(EndOfRequestsMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())

    dp.message.middleware(ChatActionMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())

    for router in routers:
        dp.include_router(router)

    return dp
