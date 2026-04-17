import json

from app.schemas import Event
from app.constants import IMAGE_SUBMITTED


class ImageService:
    def __init__(self, broker):
        self.broker = broker

    def handle_upload(self, image_id: str, path: str, source: str = "cli") -> Event:
        event = Event(
            topic=IMAGE_SUBMITTED,
            event_id=f"evt_{image_id}",
            payload={
                "image_id": image_id,
                "path": path,
                "source": source,
            },
        )

        self.broker.publish(IMAGE_SUBMITTED, event.model_dump_json())
        return event