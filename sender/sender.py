from uuid import UUID

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

import asyncio

from shared.dbs.minio.client import client
from shared.dbs.minio.plot_repository import PlotRepository
from shared.dbs.postgres.models.users import Users
from shared.dbs.postgres.models.task import Tasks
from shared.dbs.postgres.repositories.task import TaskRepository
from shared.dbs.postgres.repositories.users import UserRepository
from shared.dbs.postgres.postgresql import sync_session
from shared.settings import TELEGRAM_TOKEN

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, InputMediaPhoto

from shared.settings import RABBITMQ_HOST


bot: Bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)

broker = RabbitmqBroker(host=RABBITMQ_HOST)

dramatiq.set_broker(broker)

plot_repo: PlotRepository = PlotRepository(client=client)

@dramatiq.actor()
def send_tg_result(task_id: str):

    try:
        task_id = UUID(task_id)
    except ValueError:
        raise Exception("task_id должен быть валидным UUID")

    task: Tasks = TaskRepository(session=sync_session).get_task_by_id(task_id=task_id)
    user: Users = UserRepository(session=sync_session).get_user_by_id(user_id=task.user_id)
    images: [bytes]= plot_repo.get_plots_by_task_id(task_id=task_id)

    bf: list[BufferedInputFile] = [BufferedInputFile(file=image, filename='def') for image in images]

    asyncio.run(bot.send_media_group(chat_id=task.user_id, media=bf))
