import logging

from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from shared.dbs.postgres.models.users import Users
from shared.dbs.postgres.repositories.abstract import Repository

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update


class UserRepo(Repository[Users]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Users, session=session)

    async def new(
            self,
            telegram_id: int,
            first_name: str,
            commisions: float = 0.03,
    ) -> Users:
        new_user = await self.session.merge(
            Users(telegram_id=telegram_id,
                  name=first_name,
                  commisions=commisions
                )
        )

        return new_user

    async def get_by_tg_id(self, ident: Union[int, str]) -> Users:
        """
        Checking the presence of the indexer in the database
        :param ident: Primary key of the model
        :return: True if the model exists, False otherwise
        """
        return (await self.get_by_where(Users.telegram_id == ident))

    async def exists_check_by_tg_id(self, ident: Union[int, str]) -> bool:
        """
        Checking the presence of the indexer in the database
        :param ident: Primary key of the model
        :return: True if the model exists, False otherwise
        """
        return (await self.get_by_tg_id(ident)) is not None


class UserRepository:
    def __init__(self, session: sessionmaker):
        self.session = session

    def get_user_by_id(self, user_id: UUID):
        with self.session() as session:
            stmt = select(Users).where(Users.telegram_id == user_id)
            task = session.scalars(stmt)
            return task.first()
