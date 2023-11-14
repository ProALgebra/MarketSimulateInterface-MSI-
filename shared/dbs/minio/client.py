import minio

from shared.dbs.minio import settings

client = minio.Minio(
    f"{settings.S3_HOST}:{settings.S3_PORT}",
    settings.S3_ACCESS_KEY,
    settings.s3_SECRET_KEY,
    secure=False  # у нас нет ssl поэтому используем так
)
