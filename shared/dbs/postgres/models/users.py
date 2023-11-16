from .base_model import Base

from sqlalchemy import (Integer, String, FLOAT)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import BIGINT


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
        BIGINT,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        'name',
        String
    )

    commisions: Mapped[float] = mapped_column(
        'commisions',
        FLOAT,
        default=0.03
    )
