from datetime import datetime
from enum import Enum
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class GenerationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerationSettings(BaseModel):
    width: int = 512
    height: int = 512
    model: str = "dall-e-3"
    style: Optional[str] = None


class Generation(Document):
    user_id: PydanticObjectId
    prompt: str
    image_url: str
    status: GenerationStatus = GenerationStatus.COMPLETED
    settings: GenerationSettings = GenerationSettings()
    created_at: datetime = datetime.now()

    class Settings:
        name = "generations"
        indexes = [
            "user_id",
        ]
