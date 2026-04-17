from datetime import datetime, UTC
from typing import Any

from pydantic import BaseModel, Field


class Event(BaseModel):
    type: str = "publish"
    topic: str
    event_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    payload: dict[str, Any]