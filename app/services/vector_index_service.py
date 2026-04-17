from app.schemas import Event
from app.constants import QUERY_COMPLETED
from app.storage.vector_store import VectorStore
from app.utils.fake_embedding import create_fake_embedding


class VectorIndexService:
    def __init__(self, broker, vector_store: VectorStore):
        self.broker = broker
        self.vector_store = vector_store
        self.processed_events = set()

    def handle_embedding_created(self, event: Event) -> None:
        if event.event_id in self.processed_events:
            return None

        self.processed_events.add(event.event_id)

        image_id = event.payload["image_id"]
        embedding = event.payload["embedding"]

        self.vector_store.add_vector(image_id, embedding)
        return None

    def handle_query_submitted(self, event: Event) -> Event:
        query_id = event.payload["query_id"]
        query_text = event.payload["text"]
        top_k = event.payload.get("top_k", 3)

        query_vector = create_fake_embedding(query_text)
        results = self.vector_store.search(query_vector, top_k=top_k)

        completed_event = Event(
            topic=QUERY_COMPLETED,
            event_id=f"{event.event_id}_completed",
            payload={
                "query_id": query_id,
                "text": query_text,
                "top_k": top_k,
                "results": results,
            },
        )

        self.broker.publish(QUERY_COMPLETED, completed_event.model_dump_json())
        return completed_event