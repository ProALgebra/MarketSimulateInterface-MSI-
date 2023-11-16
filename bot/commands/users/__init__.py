from os import getenv

from aiogram import Router

from .start import user_start_router
from .cancel import user_cancel_router
from .account import account_router
from .core import core_router
from .gpt import gpt_router

from middlewares import (UserConnectionsMiddleware, TasksConnectionsMiddleware, RegistrationsMiddleware)

user_router = Router(name="User")

user_router.message.middleware(RegistrationsMiddleware())
user_router.message.middleware(UserConnectionsMiddleware())
user_router.message.middleware(TasksConnectionsMiddleware())

user_router.callback_query.middleware(RegistrationsMiddleware())
user_router.callback_query.middleware(UserConnectionsMiddleware())
user_router.callback_query.middleware(TasksConnectionsMiddleware())

user_router.include_routers(user_start_router, user_cancel_router, account_router,
                            core_router, gpt_router)
