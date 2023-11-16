import asyncio

import logging

from aiogram import Bot
from aiogram.enums import ParseMode

from structures.dispatcher import get_dispatcher, get_redis_storage
from structures.data_structure import TransferData
from cache import Cache
from structures import conf, set_bot_commands

from shared.dbs.postgres.postgresql import async_session


logger = logging.getLogger(__name__)


async def start_bot():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info("Starting bot")

    bot = Bot(token=conf.bot.token,
              parse_mode=ParseMode.HTML)
    cache: Cache = Cache()

    storage = get_redis_storage(redis=cache.fsm_client.redis_client)

    dp = get_dispatcher(storage=storage)

    transfer_data: TransferData = TransferData(pool=async_session, cache=cache)

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
