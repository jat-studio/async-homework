import pika


HOST = "localhost"
USER = "admin"
PASSWORD = "admin"
PORT = 25672
VHOST = "%2F"

BUSINESS_EVENTS_EXCHANGE = "business-events"
CUD_EVENTS_EXCHANGE = "cud-events"


class RabbitMQGateway:

    def __init__(
        self,
        host: str = HOST,
        user: str = USER,
        password: str = PASSWORD,
        port: int = PORT,
        vhost: str = VHOST,
    ) -> None:
        self._url = pika.URLParameters(f"amqp://{user}:{password}@{host}:{port}/{vhost}")

    @property
    def conn(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(self._url)

    def produce_business_event(self, body: str) -> None:
        conn = self.conn
        conn.channel().basic_publish(exchange=BUSINESS_EVENTS_EXCHANGE, routing_key="", body=body)

        conn.close()

    def produce_cud_event(self, body: str) -> None:
        conn = self.conn
        conn.channel().basic_publish(exchange=CUD_EVENTS_EXCHANGE, routing_key="", body=body)

        conn.close()
