from app.schemas import Event
from app.constants import EMBEDDING_CREATED
from app.utils.fake_embedding import create_fake_embedding


class EmbeddingService:
    def __init__(self, broker):
        self.broker = broker
        self.processed_events = set()

    def handle_annotation_stored(self, event: Event) -> Event | None:
        if event.event_id in self.processed_events:
            return None

        self.processed_events.add(event.event_id)

        image_id = event.payload["image_id"]
        embedding = create_fake_embedding(image_id)

        embedding_event = Event(
            topic=EMBEDDING_CREATED,
            event_id=f"{event.event_id}_embedding",
            payload={
                "image_id": image_id,
                "path": event.payload["path"],
                "embedding": embedding,
                "dimension": len(embedding),
            },
        )

        self.broker.publish(EMBEDDING_CREATED, embedding_event.model_dump_json())
        return embedding_event