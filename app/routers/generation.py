from typing import List
from fastapi import APIRouter, Depends ,Request, Response

from app.schemas.generation import GenerationCreate, GenerationResponse
from app.handlers import generation as generation_handler
from app.middlewares.auth import get_current_user
from app.models.user import User
from app.schemas.response import ApiResponse

router = APIRouter()


@router.post("/", response_model=ApiResponse)
async def create_generation(
    data: GenerationCreate,
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
):
    """Create new image generation"""
    prompt_response = await generation_handler.create_generation(str(current_user.id), data)
    return {
        "success":True,
        "message":"succesfully getting",
        "data":prompt_response
    }


@router.get("/", response_model=ApiResponse)
async def get_generations(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """Get all generations for the current user"""
    return await generation_handler.get_generations(str(current_user.id))

@router.get("/{generation_id}", response_model=GenerationResponse)
async def get_generation(
    generation_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get single generation by ID"""
    return await generation_handler.get_generation(str(current_user.id), generation_id)


@router.delete("/{generation_id}")
async def delete_generation(
    generation_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a generation"""
    return await generation_handler.delete_generation(str(current_user.id), generation_id)


@router.delete("/")
async def clear_history(current_user: User = Depends(get_current_user)):
    """Clear all generations for current user"""
    return await generation_handler.clear_history(str(current_user.id))
