from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SessionResponse(BaseModel):
    id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[str] = None
    is_active: bool
    last_activity: datetime
    created_at: datetime

    class Config:
        from_attributes = True
