from uuid import UUID

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from result_worker.settings import MQ_HOST

broker = RabbitmqBroker(host=MQ_HOST)

dramatiq.set_broker(broker)


@dramatiq.actor()
def send_tg_result(task_id: str):
    try:
        task_id = UUID(task_id)
    except ValueError:
        raise Exception("task_id должен быть валидным UUID")

    # достать таск

    # достать юзера

    # достать графики

    # преобразовать результат таска в осознанный текст

    # отправить текстовый результат и прикрепить графики
