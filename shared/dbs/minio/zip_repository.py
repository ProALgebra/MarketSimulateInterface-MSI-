import io
from uuid import UUID

from minio import Minio


class ZipRepository:
    ZIPS_BUCKET_NAME = "zips"

    def __init__(self, client: Minio):
        self.client = client

    def put_zip(self, task_id: UUID, zip: io.BytesIO, size: int):
        if not self.client.bucket_exists(self.ZIPS_BUCKET_NAME):
            self.client.make_bucket(self.ZIPS_BUCKET_NAME)
        self.client.put_object(self.ZIPS_BUCKET_NAME, str(task_id), zip, size)

    def get_zip_by_task_id(self, task_id: UUID) -> bytes:
        response = self.client.get_object(self.ZIPS_BUCKET_NAME, str(task_id))
        return response.data
