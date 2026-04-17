import json
from unittest.mock import MagicMock

from app.constants import IMAGE_SUBMITTED
from app.services.image_service import ImageService


def test_handle_upload_publishes_image_submitted_event():
    broker = MagicMock()
    service = ImageService(broker)

    event = service.handle_upload("img_001", "images/test.jpg")

    assert event.topic == IMAGE_SUBMITTED
    assert event.payload["image_id"] == "img_001"
    assert event.payload["path"] == "images/test.jpg"

    broker.publish.assert_called_once()

    topic_arg, message_arg = broker.publish.call_args[0]
    assert topic_arg == IMAGE_SUBMITTED

    message = json.loads(message_arg)
    assert message["topic"] == IMAGE_SUBMITTED
    assert message["payload"]["image_id"] == "img_001"
    assert message["payload"]["path"] == "images/test.jpg"