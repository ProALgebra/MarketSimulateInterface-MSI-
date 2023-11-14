from datetime import datetime
from uuid import UUID

from .base_model import Base

from sqlalchemy import (Integer, DateTime, Float)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.dialects.postgresql.json import JSON


class Tasks(Base):
    __tablename__ = 'task'

    user_id: Mapped[int] = mapped_column(
        'user_id',
        Integer,
        nullable=False
    )

    task_id: Mapped[UUID] = mapped_column(
        "task_id",
        pg_UUID,
        primary_key=True
    )

    date_from: Mapped[datetime] = mapped_column(
        "date_from",
        DateTime
    )

    date_to: Mapped[datetime] = mapped_column(
        "date_to",
        DateTime
    )

    commission: Mapped[float] = mapped_column(
        "commission",
        Float
    )

    result: Mapped[dict] = mapped_column(
        "result",
        JSON,
        nullable=True
    )

