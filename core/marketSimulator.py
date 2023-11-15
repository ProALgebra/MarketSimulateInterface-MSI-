from core.dbBrokerService import DbBrokerService
from core.sandbox import Portfolio, MarketAlgorithm
from shared.dbs.postgres import TickerHistoryRepository
from shared.dbs.postgres import sync_session


class MarketSimulator:
    def __init__(self, Broker, dateEnd):
        self.Broker = Broker  # market(dateStart,startValue,db)
        self.portfolioHistoryList = {}
        self.dateEnd = dateEnd
        self.db = DbBrokerService(DbBrokerService(self.Broker, TickerHistoryRepository(sync_session)))

    def dump_portfolio(self, portfolio: Portfolio):
        dump = {}
        dump['FREE'] = portfolio.cash
        for i in portfolio.shares:
            dump[i] = portfolio.shares[i][1]
        return dump

    def simulate(self):
        algorithm = MarketAlgorithm(self.Broker, self.db)
        while (self.Broker.date <= self.dateEnd):
            algorithm.run()
            self.portfolioHistoryList[self.Broker.date] = self.dump_portfolio(self.Broker.getPortfolio())
            self.Broker.nextDate()
        return self.portfolioHistoryList
