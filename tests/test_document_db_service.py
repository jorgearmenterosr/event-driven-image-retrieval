import json
from unittest.mock import MagicMock

from app.schemas import Event
from app.constants import INFERENCE_COMPLETED, ANNOTATION_STORED
from app.services.document_db_service import DocumentDBService
from app.storage.document_store import DocumentStore


def test_handle_inference_completed_stores_document_and_publishes_event():
    broker = MagicMock()
    store = DocumentStore()
    service = DocumentDBService(broker, store)

    input_event = Event(
        topic=INFERENCE_COMPLETED,
        event_id="evt_img_001_inference",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "objects": [
                {"label": "car", "bbox": [12, 44, 188, 200], "conf": 0.93},
                {"label": "person", "bbox": [230, 51, 286, 210], "conf": 0.88},
            ],
            "model_version": "sim-v1",
        },
    )

    output_event = service.handle_inference_completed(input_event)

    assert output_event is not None
    assert output_event.topic == ANNOTATION_STORED
    assert output_event.payload["image_id"] == "img_001"
    assert output_event.payload["object_count"] == 2

    saved_doc = store.get_document("img_001")
    assert saved_doc is not None
    assert saved_doc["image_id"] == "img_001"
    assert len(saved_doc["objects"]) == 2
    assert saved_doc["review"]["status"] == "unreviewed"
    assert "stored" in saved_doc["history"]

    broker.publish.assert_called_once()

    topic_arg, message_arg = broker.publish.call_args[0]
    assert topic_arg == ANNOTATION_STORED

    message = json.loads(message_arg)
    assert message["topic"] == ANNOTATION_STORED
    assert message["payload"]["image_id"] == "img_001"


def test_handle_inference_completed_is_idempotent():
    broker = MagicMock()
    store = DocumentStore()
    service = DocumentDBService(broker, store)

    input_event = Event(
        topic=INFERENCE_COMPLETED,
        event_id="evt_img_001_inference",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "objects": [
                {"label": "car", "bbox": [12, 44, 188, 200], "conf": 0.93},
            ],
            "model_version": "sim-v1",
        },
    )

    first_result = service.handle_inference_completed(input_event)
    second_result = service.handle_inference_completed(input_event)

    assert first_result is not None
    assert second_result is None
    assert store.count() == 1
    broker.publish.assert_called_once()