import redis

from app.broker.broker_interface import BrokerInterface


class RedisBroker(BrokerInterface):

    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.pubsub = self.client.pubsub()

    def publish(self, topic: str, message: str) -> None:
        self.client.publish(topic, message)

    def subscribe(self, topic: str):
        self.pubsub.subscribe(topic)
        return self.pubsub