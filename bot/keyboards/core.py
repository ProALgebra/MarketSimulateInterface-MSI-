from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup)

from callbacks import CoreStepData
from commands.commandName import (CORE_COMMISIONS, CORE_CASH, CORE_SOURCE, CORE_TEST)

def core_step(locale: str = None, commsisons: bool = True, source: bool = True, cash: bool = True):
    keyboard = [ [ ], [ ], [ ] ]

    if commsisons:
        keyboard[0].append(
               InlineKeyboardButton(
                      text=_(CORE_COMMISIONS, locale=locale),
                      callback_data=CoreStepData(step=CORE_COMMISIONS).pack()
                    )
        )

    if cash:
        keyboard[0].append(
               InlineKeyboardButton(
                      text=_(CORE_CASH, locale=locale),
                      callback_data=CoreStepData(step=CORE_CASH).pack()
                    )
        )

    if source:
        keyboard[1].append(
               InlineKeyboardButton(
                      text=_(CORE_SOURCE, locale=locale),
                      callback_data=CoreStepData(step=CORE_SOURCE).pack()
                    )
        )

    if source:
        keyboard[2].append(
               InlineKeyboardButton(
                      text=_(CORE_TEST, locale=locale),
                      callback_data=CoreStepData(step=CORE_TEST).pack()
                    )
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
