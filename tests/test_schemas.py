from app.schemas import Event


def test_event_schema_creation():
    event = Event(
        topic="image.submitted",
        event_id="evt_001",
        payload={
            "image_id": "img_001",
            "path": "images/test.jpg"
        }
    )

    assert event.type == "publish"
    assert event.topic == "image.submitted"
    assert event.event_id == "evt_001"
    assert event.payload["image_id"] == "img_001"
    assert "timestamp" in event.model_dump()