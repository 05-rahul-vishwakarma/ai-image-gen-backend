from typing import List, Dict, Any
from beanie import PydanticObjectId
from fastapi import HTTPException

from app.schemas.generation import GenerationCreate, GenerationResponse
from app.schemas.response import success_response, error_response
from app.models.generation import Generation, GenerationStatus, GenerationSettings
from app.services.huggingface_service import huggingface_service


async def create_generation(user_id: str, data: GenerationCreate) -> Dict[str, Any]:
    """Create new image generation"""
    try:
        # Create initial generation record with PROCESSING status
        generation = Generation(
            user_id=PydanticObjectId(user_id),
            prompt=data.prompt,
            image_url="",  # Will be updated after generation
            status=GenerationStatus.PROCESSING,
            settings=data.settings or GenerationSettings()
        )
        await generation.insert()

        try:
            # Generate image using Hugging Face Stable Diffusion
            # Returns base64 encoded image data
            image_data = await huggingface_service.generate_image(data)

            # Update generation with image data and COMPLETED status
            generation.image_url = image_data  # Store cloudnary imge url
            generation.status = GenerationStatus.COMPLETED
            await generation.save()

        except Exception as e:
            # Update generation with FAILED status
            generation.status = GenerationStatus.FAILED
            await generation.save()
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

        # Return response
        response_data = GenerationResponse(
            id=str(generation.id),
            user_id=str(generation.user_id),
            prompt=generation.prompt,
            image_url=generation.image_url,
            status=generation.status,
            settings=generation.settings,
            created_at=generation.created_at
        )

        return success_response("Generation created successfully", response_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create generation: {str(e)}")



async def get_generations(user_id: str) -> Dict[str, Any]:
    """Get all generations for a user"""
    try:
        all_generations = await (
            Generation.find(Generation.user_id == PydanticObjectId(user_id))
            .sort(-Generation.created_at)  # newest first
            .to_list()
        )

        # Convert Beanie documents to Pydantic response objects
        generations_data = [
            GenerationResponse(
                id=str(gen.id),
                user_id=str(gen.user_id),
                prompt=gen.prompt,
                image_url=gen.image_url,
                status=gen.status,
                settings=gen.settings,
                created_at=gen.created_at
            )
            for gen in all_generations
        ]

        return success_response("Generations fetched successfully", generations_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch generations: {str(e)}")


async def get_generation(user_id: str, generation_id: str) -> Dict[str, Any]:
    """Get single generation by ID"""
    try:
        generation = await Generation.get(PydanticObjectId(generation_id))

        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        # Verify ownership
        if str(generation.user_id) != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        response_data = GenerationResponse(
            id=str(generation.id),
            user_id=str(generation.user_id),
            prompt=generation.prompt,
            image_url=generation.image_url,
            status=generation.status,
            settings=generation.settings,
            created_at=generation.created_at
        )

        return success_response("Generation fetched successfully", response_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch generation: {str(e)}")


async def delete_generation(user_id: str, generation_id: str) -> Dict[str, Any]:
    """Delete a generation"""
    try:
        generation = await Generation.get(PydanticObjectId(generation_id))

        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        # Verify ownership
        if str(generation.user_id) != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        await generation.delete()

        return success_response("Generation deleted successfully", None)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete generation: {str(e)}")


async def clear_history(user_id: str) -> Dict[str, Any]:
    """Clear all generations for user"""
    try:
        result = await Generation.find(
            Generation.user_id == PydanticObjectId(user_id)
        ).delete()

        return success_response(
            "Generation history cleared successfully",
            {"deleted_count": result.deleted_count}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")
