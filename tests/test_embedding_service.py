import json
from unittest.mock import MagicMock

from app.schemas import Event
from app.constants import ANNOTATION_STORED, EMBEDDING_CREATED
from app.services.embedding_service import EmbeddingService


def test_handle_annotation_stored_publishes_embedding_created():
    broker = MagicMock()
    service = EmbeddingService(broker)

    input_event = Event(
        topic=ANNOTATION_STORED,
        event_id="evt_img_001_inference_stored",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "object_count": 2,
        },
    )

    output_event = service.handle_annotation_stored(input_event)

    assert output_event is not None
    assert output_event.topic == EMBEDDING_CREATED
    assert output_event.payload["image_id"] == "img_001"
    assert len(output_event.payload["embedding"]) == 8
    assert output_event.payload["dimension"] == 8

    broker.publish.assert_called_once()

    topic_arg, message_arg = broker.publish.call_args[0]
    assert topic_arg == EMBEDDING_CREATED

    message = json.loads(message_arg)
    assert message["topic"] == EMBEDDING_CREATED
    assert message["payload"]["image_id"] == "img_001"


def test_handle_annotation_stored_is_idempotent():
    broker = MagicMock()
    service = EmbeddingService(broker)

    input_event = Event(
        topic=ANNOTATION_STORED,
        event_id="evt_img_001_inference_stored",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "object_count": 2,
        },
    )

    first_result = service.handle_annotation_stored(input_event)
    second_result = service.handle_annotation_stored(input_event)

    assert first_result is not None
    assert second_result is None
    broker.publish.assert_called_once()