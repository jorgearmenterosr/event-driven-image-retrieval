from app.schemas import Event
from app.constants import INFERENCE_COMPLETED
from app.utils.fake_inference import run_fake_inference


class InferenceService:
    def __init__(self, broker):
        self.broker = broker
        self.processed_events = set()

    def handle_image_submitted(self, event: Event) -> Event | None:
        if event.event_id in self.processed_events:
            return None

        self.processed_events.add(event.event_id)

        image_id = event.payload["image_id"]
        objects = run_fake_inference(image_id)

        inference_event = Event(
            topic=INFERENCE_COMPLETED,
            event_id=f"{event.event_id}_inference",
            payload={
                "image_id": image_id,
                "path": event.payload["path"],
                "objects": objects,
                "model_version": "sim-v1",
            },
        )

        self.broker.publish(INFERENCE_COMPLETED, inference_event.model_dump_json())
        return inference_event