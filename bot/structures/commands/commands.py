from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from bot.commands.command_name import START_COMMAND


async def set_bot_commands(bot: Bot):
    data = [
        (
            [
                BotCommand(command=START_COMMAND, description="Меню")
            ],
            BotCommandScopeAllPrivateChats(),
            None
        )
    ]

    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)
