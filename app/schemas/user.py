from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.session import SessionResponse 

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    avatar: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ProfileResponse(BaseModel):
    user:UserResponse
    session:SessionResponse