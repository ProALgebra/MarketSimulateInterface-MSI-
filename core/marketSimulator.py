from sandbox import Portfolio,MarketAlgorithm
from dbBrokerService import DbBrokerService
from shared.dbs.postgres.postgresql import sync_session
from shared.dbs.postgres.ticker_repository import TickerHistoryRepository

class MarketSimulator:
    def __init__(self, Broker, dateEnd):
        self.Broker = Broker  # market(dateStart,startValue,db)
        self.portfolioHistoryList = {}
        self.dateEnd = dateEnd
        self.db = DbBrokerService(DbBrokerService(self.Broker,TickerHistoryRepository(sync_session)))

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