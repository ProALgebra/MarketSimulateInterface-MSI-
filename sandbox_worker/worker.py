import io
from uuid import UUID

import zipfile

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from sandbox_worker.settings import MQ_HOST

from shared.dbs.minio.client import client as minio_client
from shared.dbs.minio.plot_repository import PlotRepository
from shared.dbs.minio.zip_repository import ZipRepository
from shared.dbs.postgres.postgresql import sync_session
from shared.dbs.postgres.task_repository import TaskRepository

from core.sandbox import Portfolio,Broker
from core.marketSimulator import MarketSimulator
from dbService import DbBrokerService
from shared.dbs.postgres.ticker_repository import TickerHistoryRepository
from shared.dbs.postgres.postgresql import sync_session

broker = RabbitmqBroker(host=MQ_HOST)
dramatiq.set_broker(MQ_HOST)


@dramatiq.actor()
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

    ...  # запустить песок с параметрами из task_data
    simulator = MarketSimulator(Broker = Broker(task_data.date_from,task_data.start_cash,TickerHistoryRepository(sync_session)), dateEnd=task_data.date_to, )
    pass
    pass
    pass

    ...  # обработать результат песка, сохранить
    pass
    pass
    pass
    task_repo.update_task_result(task_id, {}) # < ---  результат сюда

    ... # нарисовать графики и положить в хранилище
    pass
    pass
    pass


def unzip_to_string(zip: bytes, filename: str) -> str:
    zip = zipfile.ZipFile(io.BytesIO(zip))
    try:
        unzipped_bytes = zip.read(filename)
    except FileNotFoundError as e:
        raise Exception("файл должен называться 'MarketAlgorythm.py'", e)
    return str(unzipped_bytes)





