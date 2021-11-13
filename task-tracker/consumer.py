#!/usr/bin/env python
import os
import sys

from rabbitmq_gateway import (
    BUSINESS_EVENTS_EXCHANGE,
    CUD_EVENTS_EXCHANGE,
    RabbitMQGateway,
)

CUD_QUEUE = "cud-task-tracker"
BUSINESS_QUEUE = "business-task-tracker"


def main() -> None:
    conn = RabbitMQGateway().conn
    channel = conn.channel()

    channel.queue_declare(queue=CUD_QUEUE)
    channel.queue_bind(queue=CUD_QUEUE, exchange=CUD_EVENTS_EXCHANGE)

    channel.queue_declare(queue=BUSINESS_QUEUE)
    channel.queue_bind(queue=BUSINESS_QUEUE, exchange=BUSINESS_EVENTS_EXCHANGE)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=CUD_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=BUSINESS_QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
