# import database
import numpy as np
import datetime

data = {datetime.datetime(2023, 10, 12, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002},
datetime.datetime(2023, 10, 13, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002},
datetime.datetime(2023, 10, 14, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 16, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 17, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 18, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 19, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 20, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 21, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 23, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 24, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 25, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 26, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 27, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 28, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 30, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 10, 31, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 1, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 2, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 3, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 4, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 6, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 7, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 8, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 9, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 10, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 11, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}, datetime.datetime(2023, 11, 13, 17, 33, 19, 375091): {'TMOS': 1, 'FREE': 112413.80400000002}}

print(data)

class Metrics():
    def __init__(self, logs):
        self.all_tickers = database.getAllTickers()
        self.logs = logs
        self.createTotals()
        self.relativeTotal()
        self.balance()
        self.createDPNL()

    def totalAtDay(self, data):
        portfel = self.logs[data]
        free_money = portfel["free"]
        ticker_ndarray = np.array(list(portfel.values()))
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
        days = self.logs.keys().sorted()[1:]
        for i in range(1, len(self.logs)):
            self.DPNL[days[i]] = (self.logs[days[i]] - self.logs[days[i-1]]) / self.logs[days[i-1]]

    def relativeTotal(self):
        self.relative_totals = {}
        days = self.logs.keys().sorted()
        total_at_first_day = self.logs[days[0]]
        for day in days:
            self.relative_totals[day] = self.totals[day] / total_at_first_day



    def balance(self):
        self.balance = {}
        portfel = self.logs[data]
        ticker_ndarray = np.array(list(portfel.values()))

        pass



    def Sharp(self):
        pass










