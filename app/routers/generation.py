from typing import Dict, Any
from fastapi import APIRouter, Depends, status

from app.schemas.generation import GenerationCreate
from app.handlers import generation as generation_handler
from app.middlewares.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_generation(
    data: GenerationCreate,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Create new image generation"""
    return await generation_handler.create_generation(str(current_user.id), data)


@router.get("/")
async def get_generations(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Get all generations for current user"""
    return await generation_handler.get_generations(str(current_user.id))


@router.get("/{generation_id}")
async def get_generation(
    generation_id: str,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get single generation by ID"""
    return await generation_handler.get_generation(str(current_user.id), generation_id)


@router.delete("/{generation_id}")
async def delete_generation(
    generation_id: str,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Delete a generation"""
    return await generation_handler.delete_generation(str(current_user.id), generation_id)


@router.delete("/")
async def clear_history(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Clear all generations for current user"""
    return await generation_handler.clear_history(str(current_user.id))
