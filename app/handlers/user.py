from fastapi import Request, Response, status, HTTPException
from beanie import PydanticObjectId
from app.schemas.user import UserResponse, ProfileResponse
from app.schemas.session import SessionResponse
from app.schemas.response import ApiResponse
from app.models.user import User
from app.models.session import Session

async def get_profile(
    user_id: str,
    request: Request,
    response: Response
) -> ApiResponse[ProfileResponse]:

    # Fetch user from database
    user = await User.get(PydanticObjectId(user_id))
    session = await Session.find_one(
    Session.user_id == PydanticObjectId(user_id)
)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response.status_code = status.HTTP_200_OK

    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        created_at=user.created_at
    )

    session_response = SessionResponse(
        id=str(session.id),
        ip_address=session.ip_address,
        user_agent=session.user_agent,
        device_info=session.device_info,
        is_active=session.is_active,
        last_activity=session.last_activity,
        created_at=session.created_at
    )

    profile = ProfileResponse(
        user=user_response,
        session=session_response
    )

    return {
        "success": True,
        "message": "Successfully fetched profile",
        "data": profile,
    }
    
    
async def update_profile(
    user_id: str,
    data: dict,
    request: Request,
    response: Response
) -> ApiResponse[UserResponse]:
    """Update user profile"""
    # Fetch user from database
    user = await User.get(PydanticObjectId(user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update allowed fields
    if "name" in data:
        user.name = data["name"]
    if "avatar" in data:
        user.avatar = data["avatar"]

    # Save updated user
    await user.save()

    response.status_code = status.HTTP_200_OK

    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        created_at=user.created_at
    )

    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": user_response
    }
