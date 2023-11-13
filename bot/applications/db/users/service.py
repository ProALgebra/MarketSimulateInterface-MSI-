import logging

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Intonation, User, Digest


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_intonation_id(self, intonation: str):
        logging.error(intonation)
        stmt = select(Intonation.id)
        stmt = stmt.where(Intonation.intonation == intonation)
        response = await self.session.execute(stmt)
        intonation_id = response.scalars().first()
        logging.error(intonation_id)
        return intonation_id

    async def create_user(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        language_code: str,
        source: str | None = None,
    ):
        values = {
            'id': telegram_id,
            'username': username or '',
            'first_name': first_name,
            'last_name': last_name or '',
            'language_code': language_code,
            'intonation_id': 1,
            'digest_hours': list(range(0, 24, 3)),
            'last_digest_at': None,
            'disabled_at': None,
            'source': source,
        }
        stmt = insert(User)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing()
        await self.session.execute(stmt)

        stmt = select(Digest)
        stmt = stmt.where(Digest.user_id == telegram_id)
        stmt = stmt.where(Digest.is_current)
        response = await self.session.execute(stmt)
        digests = response.scalars().first()

        if not digests:
            stmt = insert(Digest)
            stmt = stmt.values(user_id=telegram_id)
            await self.session.execute(stmt)

    async def update_language(self, telegram_id: int, language_code: str):
        stmt = update(User)
        stmt = stmt.values(language_code=language_code)
        stmt = stmt.where(User.id == telegram_id)
        await self.session.execute(stmt)

    async def update_intonation(self, telegram_id: int, intonation: str):
        intonation_id = await self._get_intonation_id(intonation)
        stmt = update(User)
        stmt = stmt.values(intonation_id=intonation_id)
        stmt = stmt.where(User.id == telegram_id)
        await self.session.execute(stmt)

    async def update_name(self, telegram_id: int, first_name: str):
        stmt = update(User)
        stmt = stmt.values(first_name=first_name)
        stmt = stmt.where(User.id == telegram_id)
        await self.session.execute(stmt)

    async def update_digest_hours(
        self,
        telegram_id: int,
        digest_hours: list[int]
    ):
        stmt = update(User)
        stmt = stmt.values(digest_hours=digest_hours)
        stmt = stmt.where(User.id == telegram_id)
        await self.session.execute(stmt)

    async def get_all_active_users(self):
        stmt = select(User.id).where(User.disabled_at.is_(None))
        response = await self.session.execute(stmt)
        user_ids: list[int] = list(response.scalars().all())
        return user_ids
