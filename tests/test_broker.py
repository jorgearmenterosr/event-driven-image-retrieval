from unittest.mock import MagicMock

from app.broker.redis_broker import RedisBroker


def test_publish_calls_redis_client():
    broker = RedisBroker()
    broker.client = MagicMock()

    broker.publish("image.submitted", '{"test": "value"}')

    broker.client.publish.assert_called_once_with(
        "image.submitted",
        '{"test": "value"}'
    )