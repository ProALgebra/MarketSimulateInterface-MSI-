from shared.dbs.postgres.repositories.ticker import TickerHistoryRepository
from core.sandbox import Broker,Share

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
            if (date != j.day and i != 4):
                disc = {}
                i = 0

            if (i == 4):
                i = 0
                history[date] = disc
                disc = {}
            disc[j.ticket] = Share(j.ticket,j.price)
            i += 1
            date = j.day
        return history
