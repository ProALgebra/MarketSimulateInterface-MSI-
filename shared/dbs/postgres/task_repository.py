from datetime import datetime
from uuid import UUID

from shared.dbs.postgres.models.task import Tasks

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select


class TaskRepository:
    def __init__(self, session: sessionmaker):
        self.session = session

    def get_task_by_id(self, task_id: UUID):
        with self.session() as session:
            stmt = select(Tasks).where(Tasks.task_id == task_id)
            task = session.scalars(stmt)
            return task.first()

    def insert_task(self, task_id: UUID, date_from: datetime, date_to: datetime, commission: float):
        with self.session() as session:
            session.add(
                Tasks(
                    task_id=task_id,
                    date_from=date_from,
                    date_to=date_to,
                    commission=commission
                )
            )
            session.commit()


class AsyncTaskRepository:
    def __init__(self, session: async_sessionmaker):
        self.session = session

    async def get_task_by_id(self, task_id: UUID):
        async with self.session() as session:
            stmt = select(Tasks).where(Tasks.task_id == task_id)
            task = await session.scalars(stmt)
            return task.first()

    async def insert_task(self, task_id: UUID, date_from: datetime, date_to: datetime, commission: float):
        async with self.session() as session:
            session.add(
                Tasks(
                    task_id=task_id,
                    date_from=date_from,
                    date_to=date_to,
                    commission=commission
                )
            )
            await session.commit()
