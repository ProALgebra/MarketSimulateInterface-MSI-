import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker


rabbitmq_broker = RabbitmqBroker(host="localhost")
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor()
def work(ticker: str, price: float):
    pass

if __name__ == "__main__":
    print("запускаю таск для консумера")
    work.send("test", 1.01)