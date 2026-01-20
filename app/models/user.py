from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import EmailStr


class User(Document):
    email: EmailStr
    password: str
    name: str
    avatar: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = "users"
        indexes = [
            "email",
            "name"
        ]
