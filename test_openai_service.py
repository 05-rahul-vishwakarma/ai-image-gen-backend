"""
Simple test script to verify OpenAI service integration
Run this to test if the OpenAI API key is configured correctly
"""
import asyncio
from app.services.openai_service import openai_service
from app.schemas.generation import GenerationCreate, GenerationSettings


async def test_image_generation():
    """Test image generation with a simple prompt"""
    print("Testing OpenAI image generation...")
    print("-" * 50)

    # Create test data
    test_data = GenerationCreate(
        prompt="A beautiful sunset over mountains",
        settings=GenerationSettings(
            model="dall-e-3",
            style="vivid"
        )
    )

    try:
        print(f"Prompt: {test_data.prompt}")
        print(f"Model: {test_data.settings.model}")
        print(f"Style: {test_data.settings.style}")
        print("\nGenerating image...")

        # Generate image
        image_url = await openai_service.generate_image(test_data)

        print(f"\nSuccess! Image generated:")
        print(f"URL: {image_url}")
        print("\nCopy the URL above and paste it in your browser to view the image")

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure your OPENAI_API_KEY is set correctly in the .env file")


if __name__ == "__main__":
    asyncio.run(test_image_generation())
