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
    logger = logging.getLogger('bot')
    logger.info('Starting...')

    bot = Bot(os.getenv("TELEGRAM_TOKEN"), parse_mode='html')

    dp = Dispatcher()

    logger.info('Routers included')
    
    response = await bot.set_my_commands(
        commands=[
            BotCommand(command='menu', description='Main menu'),
        ],
        scope=BotCommandScopeAllPrivateChats()
    )
    logger.info(response)
    logger.info('Starting polling...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
