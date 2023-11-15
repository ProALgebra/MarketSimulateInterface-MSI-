from typing import Dict

from dateutil.relativedelta import relativedelta

from core.dbBrokerService import DbBrokerService


class Ticker(str):
    pass


class Share:
    def init(self, ticker: Ticker, price: float):
        self.ticker = ticker
        self.price = price


class Portfolio:
    def __init__(self, cash: float, shares: Dict[Ticker, (Share, int)]):
        self.shares = shares
        self.cash = cash

    def add_share(self, share: Share, quantity: int) -> None:
        if self.cash < share.price * quantity:
            raise Exception("У меня нет столько денег")
        if share.ticker in self.shares:
            self.shares[share.ticker][1] += quantity
        else:
            self.shares[share.ticker] = (share, quantity)

    def remove_share(self, share: Share, quantity: int) -> None:
        if share.ticker not in self.shares:
            raise Exception("у меня нет такой акции")

        current_share_quantity = self.shares[share.ticker][1]
        if quantity > current_share_quantity:
            raise Exception("у меня нет столько акций")
        self.shares[share.ticker][1] -= quantity


class Broker:
    portfolio: Portfolio

    market: Dict[Ticker, Share]

    def __init__(self, dateStart, startValue, db):
        self.date = dateStart
        self.portfolio = Portfolio(startValue, {})
        self.db = db
        self.update_market()

    def sell(self, ticker: Ticker, quantity: int) -> None:
        share = self.market[ticker]
        self.portfolio.remove_share(share, quantity)

    def buy(self, ticker: Ticker, quantity: int) -> None:
        share = self.market[ticker]
        self.portfolio.add_share(share, quantity)

    def update_market(self) -> None:
        data = self.db.getTicketsPrice(self.date)
        for ticker, share in data:
            self.market[ticker].price = share.price

    def get_all_shares(self) -> Dict[Ticker, Share]:
        return self.market

    def get_share(self, ticker: Ticker) -> Share:
        return self.market[ticker]

    def get_portfolio(self) -> Portfolio:
        return self.portfolio

    def next_day(self):
        self.date = self.date + relativedelta(days=1)
        while (self.date.weekday() > 5):
            self.date = self.date + relativedelta(days=1)
        self.update_market()


def slippingAverage(db, amount_of_days: int, tikers: [Ticker]):
    needed_month = amount_of_days // 31 + 1
    interesting_dates_over = db.getHistory(needed_month)
    interesting_dates_map = sorted(list(set(interesting_dates_over)))[-amount_of_days:]
    ans = {}
    for tiker in tikers:
        tiker_sum = 0
        for date in interesting_dates_map:
            if tiker in date:
                tiker_sum += date[tiker]
            else:
                pass
        ans[tiker] = tiker_sum / amount_of_days

    return ans


class MarketAlgorithm:
    def __init__(self, market: Broker, db: DbBrokerService):
        self.market = market
        self.db = db

    def run(self):
        tikers = ["LKOH", "SBER", "ROSN", "TATN"]
        averages = slippingAverage(self.db, 10, tikers)

        for tiker in tikers:
            tiker_current_cost = self.market.get_share(tiker)
            if averages[tiker] > tiker_current_cost:
                actions_cover_10_percent = 0.1 * self.market.get_portfolio().cash // tiker_current_cost
                try:
                    self.market.buy(tiker, actions_cover_10_percent)
                except:
                    print(f"При попытке купить {actions_cover_10_percent} "
                          f"{tiker} произошла ошибка: на балансе кошелька недостаточно средств")

            else:
                actions_cover_10_percent = round(self.market.get_portfolio().shares[tiker])
                self.market.sell(tiker, actions_cover_10_percent)
