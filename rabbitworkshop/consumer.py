import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker


rabbitmq_broker = RabbitmqBroker(host="localhost")
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor()
def work(filename, content):
    with open(filename, "w") as file:
        file.write(content)
    print("Ya vse")


# чтобы запустить воркер нужно написать "dramatiq rabbitworkshop.consumer" в терминале