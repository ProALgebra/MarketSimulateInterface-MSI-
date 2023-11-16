from typing import Union

import openai

import logging

from aiogram import F, Router, types
from aiogram import types, Router, Bot
from aiogram.enums import ChatType
from aiogram.types import ContentType

from filters.chat_type_filter import ChatTypeFilter
from shared.settings import API_KEY
from aiogram.utils.i18n import gettext as _

gpt_router = Router()


async def ask_gpt_instruct(api_key: str, promt: str, model: str = "gpt-3.5-turbo-instruct", max_token: int = 2000) -> str:
    try:

        response = await openai.Completion.acreate(
            api_key=api_key,
            model=model,
            prompt=promt[:max_token],
            max_tokens=max_token,
        )

        return response['choices'][0]['text']

    except Exception as e:
        logging.exception(f"Failed exctruct serarch questions, reason='{e}'")
        return _('GPT_ERROR')

@gpt_router.message(
    ChatTypeFilter(chat_type=[ChatType.PRIVATE]),
    F.content_type==ContentType.TEXT,
    flags={"chat_action": "typing", "registrations": False})
async def cmd_gpt(message: types.Message):
    promt: str = """
                 background:
                    - you help traders solve problems;
                    - answer in detail and politely;
                    - answer in the language of the question.

                 user: {}
                 """
    query: str = message.text

    opening_message = await message.answer('AWAIT_GPT')

    await message.reply(text=(await ask_gpt_instruct(promt=promt.format(query), api_key=API_KEY)))

    await opening_message.delete()
