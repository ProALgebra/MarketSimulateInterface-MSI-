from datetime import datetime

from .base_model import Base

from sqlalchemy import (Integer, String, DateTime, FLOAT)
from sqlalchemy.orm import Mapped, mapped_column


class TicketHistory(Base):
    __tablename__ = 'ticket'

    id: Mapped[int] = mapped_column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )

    day: Mapped[datetime] = mapped_column(
        'day',
        DateTime
    )

    ticket: Mapped[str] = mapped_column(
        'ticket',
        String
    )

    price: Mapped[float] = mapped_column(
        'price',
        FLOAT
    )
