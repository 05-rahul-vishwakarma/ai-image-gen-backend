from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import List
from beanie import PydanticObjectId

from app.schemas.user import UserResponse, ProfileResponse
from app.schemas.session import SessionResponse
from app.handlers import user as user_handler
from app.middlewares.auth import get_current_user, get_token
from app.models.user import User
from app.models.session import Session
from app.schemas.response import ApiResponse

router = APIRouter()


@router.get("/profile", response_model=ApiResponse[ProfileResponse])
async def get_profile(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """Get user profile"""
    return await user_handler.get_profile(str(current_user.id), request, response)


@router.patch("/profile", response_model=ApiResponse[UserResponse])
async def update_profile(
    data: dict,
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
):
    """Update user profile"""
    return await user_handler.update_profile(str(current_user.id), data, request, response)


@router.get("/sessions", response_model=List[SessionResponse])
async def get_active_sessions(current_user: User = Depends(get_current_user)):
    """Get all active sessions for the current user"""
    sessions = await Session.find(
        Session.user_id == current_user.id,
        Session.is_active == True
    ).to_list()

    return [
        SessionResponse(
            id=str(session.id),
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            device_info=session.device_info,
            is_active=session.is_active,
            last_activity=session.last_activity,
            created_at=session.created_at
        )
        for session in sessions
    ]


@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Revoke a specific session"""
    session = await Session.find_one(
        Session.id == PydanticObjectId(session_id),
        Session.user_id == current_user.id
    )

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.is_active = False
    await session.save()

    return {"message": "Session revoked successfully"}


@router.delete("/sessions")
async def revoke_all_sessions(
    current_user: User = Depends(get_current_user),
    token: str = Depends(get_token)
):
    """Revoke all sessions except the current one"""
    sessions = await Session.find(
        Session.user_id == current_user.id,
        Session.is_active == True,
        Session.token != token
    ).to_list()

    for session in sessions:
        session.is_active = False
        await session.save()

    return {"message": f"Revoked {len(sessions)} sessions"}
