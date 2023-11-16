from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.commands.commandName import CANCEL_COMMAND

cancel_button = InlineKeyboardButton(text='TO_CANCEL_MESSAGE', callback_data=CANCEL_COMMAND)
cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
