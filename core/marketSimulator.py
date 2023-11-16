from core.sandbox import Portfolio
from core.dbBrokerService import DbBrokerService
from shared.dbs.postgres.postgresql import sync_session
from shared.dbs.postgres.repositories.ticker import TickerHistoryRepository

class MarketSimulator:
    def __init__(self, Broker, dateEnd, algorithm):
        self.Broker = Broker  # market(dateStart,startValue,db)
        self.portfolioHistoryList = {}
        self.dateEnd = dateEnd
        self.db = DbBrokerService(self.Broker,TickerHistoryRepository(sync_session))
        self.algorithm = algorithm

    def dump_portfolio(self, portfolio: Portfolio):
        dump = {}
        dump['FREE'] = portfolio.cash
        for i in portfolio.shares:
            dump[i] = portfolio.shares[i]
        return dump

    def simulate(self):
        while (self.Broker.date <= self.dateEnd):
            self.algorithm.run()
            self.portfolioHistoryList[self.Broker.date] = self.dump_portfolio(self.Broker.get_portfolio())
            self.Broker.next_day()
        return self.portfolioHistoryList