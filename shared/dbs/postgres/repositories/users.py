import logging

from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from shared.dbs.postgres.models.users import Users
from shared.dbs.postgres.repositories.abstract import Repository

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
