from typing import List
from beanie import PydanticObjectId
from fastapi import HTTPException

from app.schemas.generation import GenerationCreate, GenerationResponse
from app.models.generation import Generation, GenerationStatus, GenerationSettings
from app.services.huggingface_service import huggingface_service


async def create_generation(user_id: str, data: GenerationCreate) -> GenerationResponse:
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
            print(data)
            image_data = await huggingface_service.generate_image(data)
            print(image_data[:100], 'image data preview')  # Print first 100 chars

            # Update generation with image data and COMPLETED status
            generation.image_url = image_data  # Store base64 image data
            generation.status = GenerationStatus.COMPLETED
            await generation.save()

        except Exception as e:
            # Update generation with FAILED status
            generation.status = GenerationStatus.FAILED
            await generation.save()
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

        # Return response
        return GenerationResponse(
            id=str(generation.id),
            user_id=str(generation.user_id),
            prompt=generation.prompt,
            image_url=generation.image_url,
            status=generation.status,
            settings=generation.settings,
            created_at=generation.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create generation: {str(e)}")


async def get_generations(user_id: str) -> List[GenerationResponse]:
    """Get all generations for user"""
    try:
        generations = await Generation.find(
            Generation.user_id == PydanticObjectId(user_id)
        ).sort(-Generation.created_at).to_list()

        return [
            GenerationResponse(
                id=str(gen.id),
                user_id=str(gen.user_id),
                prompt=gen.prompt,
                image_url=gen.image_url,
                status=gen.status,
                settings=gen.settings,
                created_at=gen.created_at
            )
            for gen in generations
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch generations: {str(e)}")


async def get_generation(user_id: str, generation_id: str) -> GenerationResponse:
    """Get single generation by ID"""
    try:
        generation = await Generation.get(PydanticObjectId(generation_id))

        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        # Verify ownership
        if str(generation.user_id) != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        return GenerationResponse(
            id=str(generation.id),
            user_id=str(generation.user_id),
            prompt=generation.prompt,
            image_url=generation.image_url,
            status=generation.status,
            settings=generation.settings,
            created_at=generation.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch generation: {str(e)}")


async def delete_generation(user_id: str, generation_id: str) -> dict:
    """Delete a generation"""
    try:
        generation = await Generation.get(PydanticObjectId(generation_id))

        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        # Verify ownership
        if str(generation.user_id) != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        await generation.delete()

        return {"message": "Generation deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete generation: {str(e)}")


async def clear_history(user_id: str) -> dict:
    """Clear all generations for user"""
    try:
        result = await Generation.find(
            Generation.user_id == PydanticObjectId(user_id)
        ).delete()

        return {
            "message": "Generation history cleared successfully",
            "deleted_count": result.deleted_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")
