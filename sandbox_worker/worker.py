import asyncio
import zipfile
from uuid import UUID

import dramatiq
from dramatiq import actor as dramatiq_actor
from aiogram import Bot
from aiogram.utils.i18n import gettext as _
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, InputMediaPhoto
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from core.sandbox import *
from core.dbBrokerService import DbBrokerService
from core.marketSimulator import MarketSimulator
from core.sandbox import Broker
from graphics.graph import *
from metrics_module.metrics import Metrics
from sandbox_worker.settings import MQ_HOST
from shared.dbs.minio.client import client as minio_client
from shared.dbs.minio.plot_repository import PlotRepository
from shared.dbs.minio.zip_repository import ZipRepository
from shared.dbs.postgres.models.task import Tasks
from shared.dbs.postgres.postgresql import sync_session
from shared.dbs.postgres.repositories.task import TaskRepository
from shared.dbs.postgres.repositories.ticker import TickerHistoryRepository
from shared.settings import TELEGRAM_TOKEN

broker = RabbitmqBroker(host=MQ_HOST)
dramatiq.set_broker(broker)

@dramatiq_actor
def run_sandbox(task_id: str):
    try:
        task_id: UUID = UUID(task_id)
    except ValueError:
        raise Exception("task_id должен быть валидным uuid")

    zip_repo = ZipRepository(minio_client)
    task_repo = TaskRepository(sync_session)
    plot_repo = PlotRepository(minio_client)

    zip = zip_repo.get_zip_by_task_id(task_id)

    client_source_code: str = unzip_to_string(zip, "MarketAlgorythm.py")

    task_data = task_repo.get_task_by_id(task_id)

    # запустить песок с параметрами из task_data
    broker = Broker(task_data.date_from, task_data.start_cash, TickerHistoryRepository(sync_session))

    try:
        exec(client_source_code, globals())
        algos = MarketAlgorithm(broker, DbBrokerService(broker, TickerHistoryRepository(sync_session)))
        simulator = MarketSimulator(Broker=broker, dateEnd=task_data.date_to, algorithm=algos)
        sandbox_output = simulator.simulate()

        # обработать результат песка, сохранить
        metrics = Metrics(logs=sandbox_output, task_id=task_id, dataBase=TickerHistoryRepository(sync_session), comis = float(task_data.commission))

        task_repo.update_task_result(task_id, {"total_at_first_day": metrics.total_at_first_day,
                                               "total_at_last_day": metrics.total_at_last_day,
                                               "total_commissions": metrics.total_commission,
                                               "total_pnl": metrics.pnl,
                                               "return_message": 0
                                               })

        # нарисовать графики и положить в хранилище

        graph = GraphInterface(metrics=metrics, idTask=task_id, client=plot_repo)

        graph.plot_relatire_Total()
        graph.plot_balance()
        graph.plot_DPNL()
        graph.plot_Total()
        graph.plot_comissions()
        graph.save_plots()
    except Exception as e:
        task_repo.update_task_result(task_id, {"total_at_first_day": None,
                                               "total_at_last_day": None,
                                               "total_commissions": None,
                                               "total_pnl": None,
                                               "return_message": str(e)
                                               })

    send_tg_result.send(str(task_id))


def unzip_to_string(zip: bytes, filename: str) -> str:
    zip = zipfile.ZipFile(io.BytesIO(zip))
    try:
        unzipped_bytes = zip.read(filename)
    except FileNotFoundError as e:
        raise Exception("файл должен называться 'MarketAlgorythm.py'", e)
    return unzipped_bytes.decode("UTF-8")


bot: Bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)


plot_repo: PlotRepository = PlotRepository(client=minio_client)


@dramatiq_actor
def send_tg_result(task_id: str):
    try:
        task_id = UUID(task_id)
    except ValueError:
        raise Exception("task_id должен быть валидным UUID")

    task: Tasks = TaskRepository(session=sync_session).get_task_by_id(task_id=task_id)
    images: [bytes] = plot_repo.get_plots_by_task_id(task_id=task_id)

    if task.result["return_message"] != 0:
        asyncio.run(bot.send_message(chat_id=task.user_id, text="Не удалось запустить твой код, дружище!"))
        return
    tatal_at_first_day, tatal_at_last_day = task.result['total_at_first_day'], task.result['total_at_last_day']
    total_commissions, total_pnl = task.result['total_commissions'], task.result['total_pnl']

    text: str = '''⭐️Первый день: {}
        🌚Последний день: {}
        🤬Комиссия: {}
        🐸Итог: {}
        '''.format(tatal_at_first_day, tatal_at_last_day, total_commissions, total_pnl)

    bf: list[InputMediaPhoto] = [InputMediaPhoto(media=BufferedInputFile(file=image, filename='def')) for image in images]
    # asyncio.run(bot.send_message(chat_id=task.user_id, text=text))
    # asyncio.run(bot.send_media_group(chat_id=task.user_id, media=bf))
    asyncio.run(tg_result(chat_id=task.user_id, media=bf, text=text))


async def tg_result(chat_id, media, text):
    await bot.send_message(chat_id=chat_id, text=text)
    await bot.send_media_group(chat_id=chat_id, media=media)