from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.generation import GenerationStatus, GenerationSettings


class GenerationCreate(BaseModel):
    prompt: str
    settings: Optional[GenerationSettings] = None


class GenerationResponse(BaseModel):
    id: str
    user_id: str
    prompt: str
    image_url: str
    status: GenerationStatus
    settings: GenerationSettings
    created_at: datetime

    class Config:
        from_attributes = True
