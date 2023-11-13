# import database
import numpy as np
import datetime
from graphics.graph import *
from data import *


class database():
    def __init__(self):
        self.logs = logs

    @staticmethod
    def getTicketsPricesAtDay(ticket, data):
        return mass[data]


class Metrics():
    def __init__(self, logs):
        self.totals = None
        self.DPNL = None
        self.relative_totals = None
        self.balance = None
        # self.all_tickers = database.getAllTickers()
        self.all_tickers = ["TMOS"]
        self.logs = logs
        self.createTotals()
        # print(self.totals)
        self.relativeTotal()
        print(self.relative_totals)
        self.balancee()
        print(self.balance)
        self.createDPNL()
        # print(self.DPNL)
        # self.Sharp()

    def totalAtDay(self, data):
        portfel = self.logs[data].copy()
        free_money = portfel["FREE"]
        portfel.pop("FREE")
        ticker_ndarray = list(portfel.keys())
        ticker_to_absolute_costs = database.getTicketsPricesAtDay(ticker_ndarray, data)
        money_in_tickers = 0
        for ticker in ticker_ndarray:
            money_in_tickers += portfel[ticker] * ticker_to_absolute_costs[ticker]
        total = free_money + money_in_tickers
        return total

    def createTotals(self):
        self.totals = {}
        days = self.logs.keys()
        for day in days:
            self.totals[day] = self.totalAtDay(day)

    def createDPNL(self):
        self.DPNL = {}
        days = sorted(list(self.logs.keys()))[1:]
        for i in range(1, len(self.logs)-1):
            self.DPNL[days[i]] = (self.totalAtDay(days[i])- self.totalAtDay(days[i-1])) / self.totalAtDay(days[i-1])

    def relativeTotal(self):
        self.relative_totals = {}
        days = sorted(list(self.logs.keys()))
        total_at_first_day = self.totals[days[0]]
        for day in days:
            self.relative_totals[day] = self.totals[day] / total_at_first_day

    def balancee(self):
        self.balance = {}
        portfel = self.logs
        ticker_ndarray = list(portfel.values())

        for day in self.logs:
            day_balance = {}
            day_tickers = self.all_tickers
            ticker_to_absolute_costs = database.getTicketsPricesAtDay(ticker_ndarray, day)
            for ticker in day_tickers:
                money_in_that_ticker = portfel[day][ticker] * ticker_to_absolute_costs[ticker]
                day_balance[ticker] = money_in_that_ticker/self.totalAtDay(day)

            free_money = portfel[day]["FREE"]
            day_balance["FREE"] = free_money/self.totalAtDay(day)

            self.balance[day] = day_balance


    def Sharp(self):
        pass


def main():
    metrics = Metrics(logs = logs)

    # graph_interface_1 = GraphInterface(metrics.totals, label='Total')
    # graph_interface_2 = GraphInterface(metrics.DPNL, label='DPNL')
    graph_interface_3 = GraphInterface(metrics.balance, label='Balances')

    # graph_interface_1.plot_Total()
    # graph_interface_2.plot_DPNL()
    graph_interface_3.plot_balance()



if __name__ == "__main__":
    main()


