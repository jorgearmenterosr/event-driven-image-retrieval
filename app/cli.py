from app.broker.redis_broker import RedisBroker
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB
from app.constants import QUERY_SUBMITTED
from app.schemas import Event
from app.services.document_db_service import DocumentDBService
from app.services.embedding_service import EmbeddingService
from app.services.image_service import ImageService
from app.services.inference_service import InferenceService
from app.services.vector_index_service import VectorIndexService
from app.storage.document_store import DocumentStore
from app.storage.vector_store import VectorStore


def main():
    broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    document_store = DocumentStore()
    vector_store = VectorStore()

    image_service = ImageService(broker)
    inference_service = InferenceService(broker)
    document_service = DocumentDBService(broker, document_store)
    embedding_service = EmbeddingService(broker)
    vector_service = VectorIndexService(broker, vector_store)

    while True:
        print("\nEvent-Driven Image Retrieval System")
        print("1. Upload image")
        print("2. Search query")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            image_id = input("Enter image id: ").strip()
            path = input("Enter image path: ").strip()

            image_event = image_service.handle_upload(image_id=image_id, path=path)
            inference_event = inference_service.handle_image_submitted(image_event)
            stored_event = document_service.handle_inference_completed(inference_event)
            embedding_event = embedding_service.handle_annotation_stored(stored_event)
            vector_service.handle_embedding_created(embedding_event)

            print(f"\nImage '{image_id}' processed successfully.")

        elif choice == "2":
            query_text = input("Enter query text: ").strip()
            top_k = int(input("Enter top k results: ").strip())

            query_event = Event(
                topic=QUERY_SUBMITTED,
                event_id=f"evt_query_{query_text.replace(' ', '_')}",
                payload={
                    "query_id": f"qry_{query_text.replace(' ', '_')}",
                    "text": query_text,
                    "top_k": top_k,
                },
            )

            result_event = vector_service.handle_query_submitted(query_event)

            print("\nQuery results:")
            for result in result_event.payload["results"]:
                print(f"- {result['image_id']} (score={result['score']})")

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()