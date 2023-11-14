import io
from uuid import UUID

import zipfile

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from sandbox_worker.settings import MQ_HOST

from shared.dbs.minio.client import client as minio_client
from shared.dbs.minio.zip_repository import ZipRepository
from shared.dbs.postgres.postgresql import sync_session
from shared.dbs.postgres.task_repository import TaskRepository

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

    zip = zip_repo.get_zip_by_task_id(task_id)

    client_source_code: str = unzip_to_string(zip, "MarketAlgorythm.py")

    task_data = task_repo.get_task_by_id(task_id)



    ...
    ...
    ...


def unzip_to_string(zip: bytes, filename: str) -> str:
    zip = zipfile.ZipFile(io.BytesIO(zip))
    try:
        unzipped_bytes = zip.read(filename)
    except FileNotFoundError as e:
        raise Exception("файл должен называться 'MarketAlgorythm.py'", e)
    return str(unzipped_bytes)





