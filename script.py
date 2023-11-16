import sqlite3
from datetime import datetime, timedelta

from pandas import DataFrame
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle
import time
import pandas as pd

from core.dbBrokerService import DbBrokerService
from datetime import datetime, date, time, timezone, timedelta
from shared.dbs.postgres.ticker_repository import TickerHistoryRepository
from shared.dbs.postgres.postgresql import sync_session
from core.sandbox import Broker,Share,Ticker
from core.marketSimulator import MarketSimulator
from metrics_module.metrics import Metrics
from graphics.graph import *

ticker_repo = TickerHistoryRepository(sync_session)

def slippingAverage(db, amount_of_days:int, tikers : [Ticker]):
    needed_month = amount_of_days // 31 + 1
    interesting_dates_over = db.getHistory(needed_month)
    interesting_dates_map = sorted(list(set(interesting_dates_over)))[-amount_of_days:]
    ans = {}
    for tiker in tikers:
        tiker_sum = 0
        for date in interesting_dates_over:
            if tiker in interesting_dates_over[date]:
                tiker_sum += interesting_dates_over[date][tiker].price
            else:
                pass
        ans[tiker] = tiker_sum / amount_of_days

    return ans



class MarketAlgorithm:
    def __init__(self, market : Broker, db : DbBrokerService):
        self.market = market
        self.db = db

    def run(self):
        tikers = ["LKOH", "SBER", "ROSN", "TATN"]
        averages = slippingAverage(self.db, 10, tikers)

        for tiker in tikers:
            tiker_current_cost = self.market.get_share(Ticker(tiker)).price
            if averages[tiker] > tiker_current_cost:
                actions_cover_10_percent = 0.1 * self.market.get_portfolio().cash // tiker_current_cost
                if(actions_cover_10_percent>0):
                    try:
                        self.market.buy(Ticker(tiker), int(actions_cover_10_percent))
                    except:
                        print(f"При попытке купить {actions_cover_10_percent} "
                                         f"{tiker} произошла ошибка: на балансе кошелька недостаточно средств")
                else:
                    self.market.sell(Ticker(tiker), int(self.market.get_portfolio().shares[Ticker(tiker)]))
            else:
                actions_cover_10_percent = round(self.market.get_portfolio().shares[Ticker(tiker)])
                self.market.sell(Ticker(tiker), actions_cover_10_percent)


brocer = Broker(datetime.combine(date(2023, 7, 14),time(7)),400000,TickerHistoryRepository(sync_session))

algos = MarketAlgorithm(brocer, DbBrokerService(brocer,TickerHistoryRepository(sync_session)))
simulator = MarketSimulator(Broker = brocer, dateEnd=datetime.combine(date(2023, 11, 15),time(7)),algorithm=algos )
sandbox_output = simulator.simulate()
metrics = Metrics(logs=sandbox_output, task_id=11,dataBase=TickerHistoryRepository(sync_session))
graph = GraphInterface(metrics=metrics, idTask=11, client=111)

graph.plot_relatire_Total()
graph.plot_balance()
graph.plot_DPNL()
graph.plot_Total()
graph.plot_comissions()
print()