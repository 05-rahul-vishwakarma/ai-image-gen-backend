from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Request
import bcrypt
from jose import jwt
from beanie import PydanticObjectId

from app.schemas.user import UserLogin, UserCreate, UserResponse
from app.schemas.auth import TokenResponse
from app.models.user import User
from app.models.session import Session
from app.core.config import settings


async def login(data: UserLogin, request: Optional[Request] = None) -> TokenResponse:
    """Login or register user"""
    # Check if user exists
    existing_user = await User.find_one(User.email == data.email)

    if existing_user:
        # User exists - verify password
        password_bytes = data.password.encode('utf-8')
        stored_password_bytes = existing_user.password.encode('utf-8')

        if not bcrypt.checkpw(password_bytes, stored_password_bytes):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user = existing_user
    else:
        # User doesn't exist - create new user (unified auth)
        password_bytes = data.password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        # Extract name from email (before @)
        name = data.email.split('@')[0]

        user = User(
            email=data.email,
            password=hashed_password.decode('utf-8'),
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        await user.insert()

    # Generate JWT token
    token_payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow()
    }

    access_token = jwt.encode(
        token_payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    # Extract client info from request
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

    # Create session in database
    session = Session(
        user_id=user.id,
        token=access_token,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        ip_address=ip_address,
        user_agent=user_agent,
        is_active=True,
        last_activity=datetime.now(),
        created_at=datetime.now()
    )
    await session.insert()

    # Create user response
    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        created_at=user.created_at
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


async def logout(user_id: str, token: Optional[str] = None) -> dict:
    """
    End user session.

    Invalidates the current session in the database.

    Args:
        user_id: ID of the user logging out
        token: JWT token to invalidate (optional)

    Returns:
        dict: Success message
    """
    # Invalidate session in database
    if token:
        # Find and deactivate the specific session
        session = await Session.find_one(
            Session.token == token,
            Session.user_id == PydanticObjectId(user_id)
        )
        if session:
            session.is_active = False
            await session.save()
    else:
        # Deactivate all sessions for this user
        sessions = await Session.find(
            Session.user_id == PydanticObjectId(user_id),
            Session.is_active == True
        ).to_list()

        for session in sessions:
            session.is_active = False
            await session.save()

    return {
        "message": "Successfully logged out",
        "detail": "Session has been invalidated"
    }


async def get_current_user(user_id: str) -> UserResponse:
    """
    Get current authenticated user by ID.

    Args:
        user_id: ID of the authenticated user

    Returns:
        UserResponse: User information

    Raises:
        HTTPException: 404 if user not found
    """
    user = await User.get(PydanticObjectId(user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        created_at=user.created_at
    )
