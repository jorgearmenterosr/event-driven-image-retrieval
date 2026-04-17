import json
from unittest.mock import MagicMock

from app.schemas import Event
from app.constants import IMAGE_SUBMITTED, INFERENCE_COMPLETED
from app.services.inference_service import InferenceService


def test_handle_image_submitted_publishes_inference_completed():
    broker = MagicMock()
    service = InferenceService(broker)

    input_event = Event(
        topic=IMAGE_SUBMITTED,
        event_id="evt_img_001",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "source": "cli",
        },
    )

    output_event = service.handle_image_submitted(input_event)

    assert output_event is not None
    assert output_event.topic == INFERENCE_COMPLETED
    assert output_event.payload["image_id"] == "img_001"
    assert len(output_event.payload["objects"]) == 2
    assert output_event.payload["model_version"] == "sim-v1"

    broker.publish.assert_called_once()

    topic_arg, message_arg = broker.publish.call_args[0]
    assert topic_arg == INFERENCE_COMPLETED

    message = json.loads(message_arg)
    assert message["topic"] == INFERENCE_COMPLETED
    assert message["payload"]["image_id"] == "img_001"


def test_handle_image_submitted_is_idempotent():
    broker = MagicMock()
    service = InferenceService(broker)

    input_event = Event(
        topic=IMAGE_SUBMITTED,
        event_id="evt_img_001",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "source": "cli",
        },
    )

    first_result = service.handle_image_submitted(input_event)
    second_result = service.handle_image_submitted(input_event)

    assert first_result is not None
    assert second_result is None
    broker.publish.assert_called_once()