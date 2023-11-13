from .base_model import Base

from sqlalchemy import (Integer, String, FLOAT)
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )

    telegram_id: Mapped[int] = mapped_column(
        'tg_id',
        Integer,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        'name',
        String
    )

    language: Mapped[str] = mapped_column(
        'language',
        String,
        default='ru'
    )

    commisions: Mapped[float] = mapped_column(
        'commisions',
        FLOAT,
        default=0.03
    )
