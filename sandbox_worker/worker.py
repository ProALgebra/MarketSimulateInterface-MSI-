from uuid import UUID

import zipfile
from graphics.graph import *
import dramatiq
from dramatiq import actor as dramatiq_actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from metrics_module.metrics import Metrics
from sandbox_worker.settings import MQ_HOST

from shared.dbs.minio.client import client as minio_client
from shared.dbs.minio.plot_repository import PlotRepository
from shared.dbs.minio.zip_repository import ZipRepository
from shared.dbs.postgres.task_repository import TaskRepository

from datetime import datetime
from shared.dbs.postgres.ticker_repository import TickerHistoryRepository
from shared.dbs.postgres.postgresql import sync_session
from core.sandbox import Broker,Share,Ticker
from core.marketSimulator import MarketSimulator
from metrics_module.metrics import Metrics
from graphics.graph import *
from core.dbBrokerService import DbBrokerService

broker = RabbitmqBroker(host=MQ_HOST)
dramatiq.set_broker(broker)


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

      # запустить песок с параметрами из task_data
    broker = Broker(task_data.date_from, 400000, TickerHistoryRepository(sync_session))

    algos = MarketAlgorithm(broker, DbBrokerService(broker, TickerHistoryRepository(sync_session)))
    simulator = MarketSimulator(Broker=broker, dateEnd=task_data.date_to, algorithm=algos)
    sandbox_output = simulator.simulate()

      # обработать результат песка, сохранить
    metrics = Metrics(logs=sandbox_output, task_id=task_id, dataBase=TickerHistoryRepository(sync_session))

    
    task_repo.update_task_result(task_id, {"tatal_at_first_day":metrics.total_at_first_day,
                                           "tatal_at_last_day": metrics.total_at_last_day,
                                           "total_commissions": metrics.total_commission,
                                           "total_pnl": metrics.pnl
                                           })

     # нарисовать графики и положить в хранилище

    graph = GraphInterface(metrics=metrics, idTask=task_id, client=plot_repo)

    graph.plot_relatire_Total()
    graph.plot_balance()
    graph.plot_DPNL()
    graph.plot_Total()
    graph.plot_comissions()
    graph.save_plots()


def unzip_to_string(zip: bytes, filename: str) -> str:
    zip = zipfile.ZipFile(io.BytesIO(zip))
    try:
        unzipped_bytes = zip.read(filename)
    except FileNotFoundError as e:
        raise Exception("файл должен называться 'MarketAlgorythm.py'", e)
    return str(unzipped_bytes)





