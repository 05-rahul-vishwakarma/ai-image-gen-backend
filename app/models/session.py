from datetime import datetime
from typing import Optional
from beanie import Document, PydanticObjectId


class Session(Document):
    user_id: PydanticObjectId
    token: str
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[str] = None
    is_active: bool = True
    last_activity: datetime = datetime.now()
    created_at: datetime = datetime.now()

    class Settings:
        name = "sessions"
        indexes = [
            "token",
            "user_id",
            "expires_at",
            "is_active",
        ]
