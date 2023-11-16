from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from bot.commands.commandName import (START_COMMAND, GET_PROFILE, GET_HISTORY, CHANGE_NAME,
                                      CORE_START, CHANGE_LANGUAGE, CANCEL_COMMAND)


async def set_bot_commands(bot: Bot):
    data = [
        (
            [
                BotCommand(command=START_COMMAND, description="Registrations"),
                BotCommand(command=CORE_START, description="Start core"),
                BotCommand(command=GET_PROFILE, description="Get profile"),
                BotCommand(command=GET_HISTORY, description="Get history"),
                BotCommand(command=CHANGE_NAME, description="Change name"),
                BotCommand(command=CHANGE_LANGUAGE, description="Change language"),
                BotCommand(command=CANCEL_COMMAND, description="Cancle state")
            ],
            BotCommandScopeAllPrivateChats(),
            None
        )
    ]

    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)
