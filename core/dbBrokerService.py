from shared.dbs.postgres.ticker_repository import TickerHistoryRepository
from sandbox import Broker

from dateutil.relativedelta import relativedelta
class DbBrokerService:

    def __init__(self, broker: Broker, repository : TickerHistoryRepository):
        self.broker = broker
        self.repository = repository

    def getHistory(self,month: int):
        _from = self.broker.get_date() - relativedelta(days = month*31)
        history = {}
        allTicketHistory = self.repository.get_tickers_in_range(_from, self.broker.get_date())
        date = allTicketHistory[0].day
        disc = {}
        i = 0
        for j in allTicketHistory:
            if (date != allTicketHistory[j].day and i != 4):
                # print(str(date))
                disc = {}
                i = 0

            if (i == 4):
                i = 0
                # print(disc)
                history[date] = disc
                disc = {}
            disc[allTicketHistory[j].ticket] = allTicketHistory[j].price
            i += 1
            date = allTicketHistory[j].day

