from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup)

from shared.dbs.postgres.models.task import Tasks
from callbacks import LanguageData, TasksData, PaginationData
from commands.commandName import (GET_PROFILE, GET_HISTORY, CORE_START, CHANGE_NAME, CHANGE_LANGUAGE, START_COMMAND,
                                  SET_RU_LANGUAGE, SET_EN_LANGUAGE)


def main(locale: str = None):
    keyboard = [
        [
            (KeyboardButton(text=_(GET_PROFILE, locale=locale))),
            (KeyboardButton(text=_(GET_HISTORY, locale=locale))),
        ],
        [
            (KeyboardButton(text=_(CHANGE_NAME, locale=locale))),
            (KeyboardButton(text=_(CHANGE_LANGUAGE, locale=locale))),
        ],
        [
            (KeyboardButton(text=_(CORE_START, locale=locale))),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def registrations(locale: str = None):
    registrations_button = InlineKeyboardButton(text=_('REGISTRATIONS', locale=locale), callback_data=START_COMMAND)
    return InlineKeyboardMarkup(inline_keyboard=[[registrations_button]])

def language():
    keyboard = [
        [
            InlineKeyboardButton(
                text='🇷🇺 Русский',
                callback_data=LanguageData(language_code=SET_RU_LANGUAGE).pack(),
            ),
            InlineKeyboardButton(
                text='🇺🇸 English',
                callback_data=LanguageData(language_code=SET_EN_LANGUAGE).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)

def tasks(tasks: list[Tasks], limit: int = 3, offset: int = 0):
    keyboard = []
    for task in tasks[offset: offset + limit]:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=_('task_infi') + ' ' + str(task.date_to) + '-' + str(task.date_from) + '-' + str(task.start_cash),
                    callback_data=TasksData(
                        task_id=task.task_id
                    ).pack(),
                )
            ]
        )
    if len(tasks) > limit:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text='<',
                    callback_data=PaginationData(direction='prev').pack(),
                ),
                InlineKeyboardButton(
                    text=str(offset // limit + 1),
                    callback_data=PaginationData(direction='keep').pack(),
                ),
                InlineKeyboardButton(
                    text='>',
                    callback_data=PaginationData(direction='next').pack(),
                ),
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def keep_name():
    keyboard = [[KeyboardButton(text=_('keep_name'))]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
