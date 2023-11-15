from shared.dbs.minio.client import client
from shared.dbs.minio import settings
from shared.dbs.minio.zip_repository import ZipRepository
from shared.dbs.minio.plot_repository import PlotRepository

__all__ = ["client", "settings", "ZipRepository", "PlotRepository"]
