from datetime import datetime
from uuid import UUID, uuid4

from shared.dbs.postgres.models.task import Tasks

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, update, delete


class TaskRepository:
    def __init__(self, session: sessionmaker):
        self.session = session

    def get_task_by_id(self, task_id: UUID):
        with self.session() as session:
            stmt = select(Tasks).where(Tasks.task_id == task_id)
            task = session.scalars(stmt)
            return task.first()

    def insert_task(self, user_id: int, date_from: datetime, date_to: datetime, commission: float) -> UUID:
        task_id = uuid4()
        with self.session() as session:
            session.add(
                Tasks(
                    task_id=task_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    commission=commission
                )
            )
            session.commit()
            return task_id

    def update_task_result(self, task_id: UUID, result: dict):
        with self.session() as session:
            stmt = update(Tasks).where(Tasks.task_id == task_id).values(result=result)
            session.execute(stmt)
            session.commit()


class AsyncTaskRepository:
    def __init__(self, session: async_sessionmaker):
        self.session = session

    async def get_tasks_by_user(self, user_id: int):
        async with self.session() as session:
            stmt = select(Tasks).where(Tasks.user_id == user_id)
            tasks = await session.scalars(stmt)
            return tasks.all()

    async def get_task_by_id(self, task_id: UUID) -> Tasks:
        async with self.session() as session:
            stmt = select(Tasks).where(Tasks.task_id == task_id)
            task = await session.scalars(stmt)
            return task.first()

    async def remove_task_by_id(self, task_id: UUID) -> None:
        async with self.session() as session:
            stmt = delete(Tasks).where(Tasks.task_id == task_id)
            await session.execute(stmt)
            await session.commit()

    async def insert_task(self, user_id: int, date_from: datetime, date_to: datetime, commission: float)  -> UUID:
        task_id = uuid4()
        async with self.session() as session:
            session.add(
                Tasks(
                    task_id=task_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    commission=commission
                )
            )
            await session.commit()
            return uuid4()

    async def update_task_result(self, task_id: UUID, result: dict):
        async with self.session() as session:
            stmt = update(Tasks).where(Tasks.task_id == task_id).values(result=result)
            await session.execute(stmt)
            await session.commit()
