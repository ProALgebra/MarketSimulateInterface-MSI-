import io
from uuid import UUID

from minio import Minio


class PlotRepository:

    def __init__(self, client: Minio):
        self.client = client

    def put_plots(self, task_id: UUID, plots: [bytes]):
        if not self.client.bucket_exists(str(task_id)):
            self.client.make_bucket(str(task_id))
        for i, plot in enumerate(plots):
            self.client.put_object(str(task_id), str(i), io.BytesIO(plot), len(plot))

    def get_plots_by_task_id(self, task_id: UUID) -> [bytes]:
        plots = []
        for plot in self.client.list_objects(str(task_id)):
            plots.append(
                self.client.get_object(str(task_id), plot.object_name).data
            )
        return plots
