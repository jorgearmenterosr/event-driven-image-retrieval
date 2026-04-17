from unittest.mock import MagicMock

from app.constants import QUERY_SUBMITTED
from app.schemas import Event
from app.services.document_db_service import DocumentDBService
from app.services.embedding_service import EmbeddingService
from app.services.image_service import ImageService
from app.services.inference_service import InferenceService
from app.services.vector_index_service import VectorIndexService
from app.storage.document_store import DocumentStore
from app.storage.vector_store import VectorStore


def test_end_to_end_upload_pipeline():
    broker = MagicMock()

    document_store = DocumentStore()
    vector_store = VectorStore()

    image_service = ImageService(broker)
    inference_service = InferenceService(broker)
    document_service = DocumentDBService(broker, document_store)
    embedding_service = EmbeddingService(broker)
    vector_service = VectorIndexService(broker, vector_store)

    image_event = image_service.handle_upload("img_001", "images/test.jpg")
    assert image_event.payload["image_id"] == "img_001"

    inference_event = inference_service.handle_image_submitted(image_event)
    assert inference_event is not None
    assert inference_event.payload["image_id"] == "img_001"

    stored_event = document_service.handle_inference_completed(inference_event)
    assert stored_event is not None
    assert stored_event.payload["image_id"] == "img_001"

    embedding_event = embedding_service.handle_annotation_stored(stored_event)
    assert embedding_event is not None
    assert embedding_event.payload["image_id"] == "img_001"

    vector_service.handle_embedding_created(embedding_event)

    saved_doc = document_store.get_document("img_001")
    assert saved_doc is not None
    assert saved_doc["image_id"] == "img_001"

    assert vector_store.exists("img_001")
    assert vector_store.count() == 1


def test_end_to_end_query_pipeline():
    broker = MagicMock()

    document_store = DocumentStore()
    vector_store = VectorStore()

    image_service = ImageService(broker)
    inference_service = InferenceService(broker)
    document_service = DocumentDBService(broker, document_store)
    embedding_service = EmbeddingService(broker)
    vector_service = VectorIndexService(broker, vector_store)

    for image_id in ["img_001", "img_002"]:
        image_event = image_service.handle_upload(image_id, f"images/{image_id}.jpg")
        inference_event = inference_service.handle_image_submitted(image_event)
        stored_event = document_service.handle_inference_completed(inference_event)
        embedding_event = embedding_service.handle_annotation_stored(stored_event)
        vector_service.handle_embedding_created(embedding_event)

    query_event = Event(
        topic=QUERY_SUBMITTED,
        event_id="evt_query_001",
        payload={
            "query_id": "qry_001",
            "text": "car",
            "top_k": 2,
        },
    )

    query_result = vector_service.handle_query_submitted(query_event)

    assert query_result.payload["query_id"] == "qry_001"
    assert len(query_result.payload["results"]) == 2