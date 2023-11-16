# import database
from graphics.graph import *
from metrics_module.data import *
from shared.dbs.postgres.repositories.ticker import TickerHistoryRepository

class Metrics:
    def __init__(self, logs, task_id, dataBase :TickerHistoryRepository):
        self.totals = None
        self.DPNL = None
        self.relative_totals = None
        self.balance = None
        self.commissions = None
        self.total_at_first_day = None
        self.total_at_last_day = None
        self.total_commission = None
        self.pnl = None

        self.dbService = dataBase

        self.all_tickers = ["LKOH", "SBER", "ROSN", "TATN"]
        self.logs = logs
        self.createTotals()
        self.relativeTotal()
        self.balancee()
        self.createDPNL()
        self.commission_coefficient = 0.004
        self.create_comissions()
        self.make_single_params()

    def make_single_params(self):
        self.total_at_first_day = self.totalAtDay(min(self.logs.keys))
        self.total_at_last_day = self.totalAtDay(max(self.logs.keys))
        self.total_commission = sum(self.commissions.values)
        self.pnl = (self.total_at_last_day - self.total_at_first_day) / self.total_at_first_day



    def totalAtDay(self, data):
        portfel = self.logs[data].copy()
        free_money = portfel["FREE"]
        portfel.pop("FREE")
        ticker_ndarray = list(portfel.keys())
        ticker_to_absolute_costs = self.dbService.get_tickers_by_day(data)
        money_in_tickers = 0
        for ticker in ticker_ndarray:
            cost = 0
            for i in ticker_to_absolute_costs:
                if(i.ticket == ticker):
                    cost = i.price
                    break
            money_in_tickers += portfel[ticker] * cost
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
        for i in range(1, len(self.logs) - 1):
            self.DPNL[days[i]] = (self.totalAtDay(days[i]) - self.totalAtDay(days[i - 1])) / self.totalAtDay(
                days[i - 1])

    def relativeTotal(self):
        self.relative_totals = {}
        days = sorted(list(self.logs.keys()))
        total_at_first_day = self.totals[days[0]]
        for day in days:
            self.relative_totals[day] = self.totals[day] / total_at_first_day

    def balancee(self):
        self.balance = {}
        portfel = self.logs
        for day in self.logs:
            day_balance = {}
            day_tickers = self.all_tickers
            ticker_to_absolute_costs = self.dbService.get_tickers_by_day(day)
            for ticker in day_tickers:
                if ticker in portfel[day]:
                    cost = 0
                    for i in ticker_to_absolute_costs:
                        if (i.ticket == ticker):
                            cost = i.price
                            break
                    money_in_that_ticker = portfel[day][ticker] * cost
                else:
                    money_in_that_ticker = 0
                day_balance[ticker] = money_in_that_ticker / self.totalAtDay(day)

            free_money = portfel[day]["FREE"]
            day_balance["FREE"] = free_money / self.totalAtDay(day)
            self.balance[day] = day_balance

    def sharp(self):
        pass

    def _comission_in_day(self, day, prev_day):
        self.logs[day].pop("FREE")
        tikers_on_current = self.logs[day].keys()
        ticker_to_absolute_costs = self.dbService.get_tickers_by_day( day)
        comission = 0
        for tiker in tikers_on_current:
            cost = 0
            for i in ticker_to_absolute_costs:
                if (i.ticket == tiker):
                    cost = i.price
                    break
            tiker_cost = cost
            tiker_count_current = self.logs[day][tiker]
            if tiker in self.logs[day]:
                tiker_count_prev = self.logs[prev_day][tiker]
            else:
                tiker_count_prev = 0
            tiker_diff = tiker_count_current - tiker_count_prev
            diff_cost = tiker_diff * tiker_cost
            comission += diff_cost

        comission = comission * self.comission_coefficient
        return comission


    def create_comissions(self):
        self.commissions = {}
        days = sorted(list(self.logs.keys()))
        for i in range(1, len(days)):
            cur_day = days[i]
            prev_day = days[i-1]
            self.commissions[days[i]] = abs(self._comission_in_day(cur_day, prev_day=prev_day))


def main():
    metrics = Metrics(logs=logs, task_id = 0)

    graph = GraphInterface(metrics, idTask=0)

    graph.plot_relatire_Total()
    graph.plot_balance()
    graph.plot_DPNL()
    graph.plot_Total()
    graph.plot_comissions()


if __name__ == "__main__":
    main()
