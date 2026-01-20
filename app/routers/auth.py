from fastapi import APIRouter, Depends, Response, Request, status

from app.schemas.user import UserLogin, UserResponse
from app.schemas.auth import TokenResponse
from app.schemas.response import ApiResponse
from app.handlers import auth as auth_handler
from app.middlewares.auth import get_current_user, get_token
from app.models.user import User
from app.core.config import settings

router = APIRouter()


@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login(data: UserLogin, response: Response, request: Request):
    """
    Login or register user (unified auth).

    Sets the JWT token in an HttpOnly cookie for security.
    Also returns the token in the response body for flexibility.
    """
    token_response = await auth_handler.login(data, request)

    # Set token in HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,  # Prevents JavaScript access (XSS protection)
        secure=settings.ENVIRONMENT == "production",  # Only HTTPS in production
        samesite="lax", # CSRF protection (use "strict" for more security)
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Cookie expiry in seconds
        path="/",       # Cookie available for all routes
    )

    response.status_code = status.HTTP_200_OK

    return {
        "success": True,
        "message": "Logged in successfully",
        "data": token_response
    }


@router.post("/logout")
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user),
    token: str = Depends(get_token)
):
    """
    End user session.

    Clears the HttpOnly cookie and invalidates the session in the database.
    """
    # Clear the cookie
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax"
    )

    return await auth_handler.logout(str(current_user.id), token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    return await auth_handler.get_current_user(str(current_user.id))
