from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from shared.dbs.postgres.models.ticket_history import TicketHistory


class TickerHistoryRepository:
    def __init__(self, session: sessionmaker):
        self.session = session

    def get_tickers_in_range(self, _from: datetime, _to: datetime):
        with self.session() as session:
            stmt = select(TicketHistory
                          ).where((TicketHistory.day >= _from) & (TicketHistory.day < _to)
                                  ).order_by(TicketHistory.day)
            tickets = session.scalars(stmt)
            return tickets.all()

    def get_tickers_by_day(self, day: datetime):
        with self.session() as session:
            stmt = select(TicketHistory).where(TicketHistory.day == day)
            ticket = session.scalars(stmt)
            return ticket.all()

    def insert_ticker(self, ticker: str, day: datetime, price: float):
        with self.session() as session:
            session.add(
                TicketHistory(
                    day=day,
                    ticket=ticker,
                    price=price
                )
            )
            session.commit()


class AsyncTickerHistoryRepository:
    def __init__(self, session: async_sessionmaker):
        self.session = session

    async def get_tickers_in_range(self, _from: datetime, _to: datetime):
        async with self.session() as session:
            stmt = select(TicketHistory).where((TicketHistory.day >= _from) & (TicketHistory.day < _to))
            tickets = await session.scalars(stmt)
            return tickets.all()

    async def get_tickers_by_day(self, day: datetime):
        async with self.session() as session:
            stmt = select(TicketHistory).where(TicketHistory.day == day)
            ticket = await session.scalars(stmt)
            return ticket.all()

    async def insert_ticker(self, ticker: str, day: datetime, price: float):
        async with self.session() as session:
            session.add(
                TicketHistory(
                    day=day,
                    ticket=ticker,
                    price=price
                )
            )
            await session.commit()
