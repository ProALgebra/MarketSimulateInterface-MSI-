import logging

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.dbs.postgres.models import Users


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
        telegram_id: int,
        first_name: str,
        language_code: str = 'ru',
        commisions: float = 0.03,
    ):
        logging.info(f"Create new users: {first_name}")
        values = {
            'telegram_id': telegram_id,
            'name': first_name,
            'language': language_code,
            'commisions': commisions,
        }
        stmt = insert(Users)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing()
        await self.session.execute(stmt)

    async def update_language(self, telegram_id: int, language_code: str):
        logging.info(f"Update users language: {telegram_id}")
        stmt = update(Users)
        stmt = stmt.values(language_code=language_code)
        stmt = stmt.where(Users.id == telegram_id)
        await self.session.execute(stmt)

    async def update_name(self, telegram_id: int, first_name: str):
        logging.info(f"Update users name: {first_name}")
        stmt = update(Users)
        stmt = stmt.values(first_name=first_name)
        stmt = stmt.where(Users.id == telegram_id)
        await self.session.execute(stmt)

    async def update_commisions(
        self,
        telegram_id: int,
        commisions: float
    ):
        logging.info(f"Update users commisions: {telegram_id}")
        stmt = update(Users)
        stmt = stmt.values(commisions=commisions)
        stmt = stmt.where(Users.id == telegram_id)
        await self.session.execute(stmt)

    async def get_all_users(self) -> list[int]:
        logging.info(f"Get all users")
        stmt = select(Users.id)
        response = await self.session.execute(stmt)
        user_ids: list[int] = list(response.scalars().all())
        return user_ids
