from datetime import datetime

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from shared.dbs.postgres.ticker_repository import TickerHistoryRepository
from shared.dbs.postgres.postgresql import sync_session

rabbitmq_broker = RabbitmqBroker(host="localhost")
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor()
def work(ticker: str, price: float):
    repo = TickerHistoryRepository(sync_session)
    repo.insert_ticker(ticker, datetime.now(), price)

# чтобы запустить воркер нужно написать "dramatiq rabbitworkshop.consumer" в терминале
