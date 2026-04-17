from app.schemas import Event
from app.constants import ANNOTATION_STORED
from app.storage.document_store import DocumentStore


class DocumentDBService:
    def __init__(self, broker, document_store: DocumentStore):
        self.broker = broker
        self.document_store = document_store
        self.processed_events = set()

    def handle_inference_completed(self, event: Event) -> Event | None:
        if event.event_id in self.processed_events:
            return None

        self.processed_events.add(event.event_id)

        image_id = event.payload["image_id"]

        document = {
            "image_id": image_id,
            "path": event.payload["path"],
            "objects": event.payload["objects"],
            "model_version": event.payload["model_version"],
            "review": {
                "status": "unreviewed",
                "notes": [],
            },
            "history": ["submitted", "inferred", "stored"],
        }

        self.document_store.insert_document(document)

        stored_event = Event(
            topic=ANNOTATION_STORED,
            event_id=f"{event.event_id}_stored",
            payload={
                "image_id": image_id,
                "path": event.payload["path"],
                "object_count": len(event.payload["objects"]),
            },
        )

        self.broker.publish(ANNOTATION_STORED, stored_event.model_dump_json())
        return stored_event