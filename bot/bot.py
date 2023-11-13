import asyncio

import logging

import pathlib

import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import FSMI18nMiddleware


i18n = I18n(
    path=pathlib.Path(__file__).parent / 'locales',
)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    logging.info('Starting...')

    bot = Bot(os.getenv("TELEGRAM_TOKEN"), parse_mode='html')

    dp = Dispatcher()

    # internationalization setup
    i18n_middleware = FSMI18nMiddleware(i18n)
    dp.message.outer_middleware.register(i18n_middleware)
    dp.callback_query.outer_middleware.register(i18n_middleware)
    logging.info('i18n set up')

    logging.info('Routers included')
    
    response = await bot.set_my_commands(
        commands=[
            BotCommand(command='menu', description='Main menu'),
        ],
        scope=BotCommandScopeAllPrivateChats()
    )
    logging.info(response)
    logging.info('Starting polling...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


import asyncio

import logging

from aiogram import Bot

from bot.structures.dispatcher import get_dispatcher, get_redis_storage
from bot.structures.data_structure import TransferData
from bot.cache import Cache
from bot.structures import conf, set_bot_commands
from bot.data_base.data_base import create_session_maker


logger = logging.getLogger(__name__)


async def start_bot():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info("Starting bot")

    bot = Bot(token=conf.bot.token)
    cache: Cache = Cache()
    storage = get_redis_storage(redis=cache.fsm_client.redis_client)

    dp = get_dispatcher(storage=storage)

    transfer_data: TransferData = TransferData(pool=create_session_maker(), cache=cache)

    await set_bot_commands(bot)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            **transfer_data
        )
    finally:
        await bot.session.close()
        await cache.close()

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")