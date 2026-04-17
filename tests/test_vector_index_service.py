import json
from unittest.mock import MagicMock

from app.schemas import Event
from app.constants import EMBEDDING_CREATED, QUERY_SUBMITTED, QUERY_COMPLETED
from app.services.vector_index_service import VectorIndexService
from app.storage.vector_store import VectorStore


def test_handle_embedding_created_adds_vector_to_store():
    broker = MagicMock()
    store = VectorStore()
    service = VectorIndexService(broker, store)

    input_event = Event(
        topic=EMBEDDING_CREATED,
        event_id="evt_img_001_embedding",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "embedding": [0.1, 0.2, 0.3, 0.4],
            "dimension": 4,
        },
    )

    service.handle_embedding_created(input_event)

    assert store.exists("img_001")
    assert store.count() == 1
    broker.publish.assert_not_called()


def test_handle_embedding_created_is_idempotent():
    broker = MagicMock()
    store = VectorStore()
    service = VectorIndexService(broker, store)

    input_event = Event(
        topic=EMBEDDING_CREATED,
        event_id="evt_img_001_embedding",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg",
            "embedding": [0.1, 0.2, 0.3, 0.4],
            "dimension": 4,
        },
    )

    service.handle_embedding_created(input_event)
    service.handle_embedding_created(input_event)

    assert store.count() == 1


def test_handle_query_submitted_publishes_query_completed():
    broker = MagicMock()
    store = VectorStore()
    service = VectorIndexService(broker, store)

    store.add_vector("img_001", [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    store.add_vector("img_002", [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])

    query_event = Event(
        topic=QUERY_SUBMITTED,
        event_id="evt_query_001",
        payload={
            "query_id": "qry_001",
            "text": "car",
            "top_k": 2,
        },
    )

    output_event = service.handle_query_submitted(query_event)

    assert output_event.topic == QUERY_COMPLETED
    assert output_event.payload["query_id"] == "qry_001"
    assert len(output_event.payload["results"]) == 2

    broker.publish.assert_called_once()

    topic_arg, message_arg = broker.publish.call_args[0]
    assert topic_arg == QUERY_COMPLETED

    message = json.loads(message_arg)
    assert message["topic"] == QUERY_COMPLETED
    assert message["payload"]["query_id"] == "qry_001"