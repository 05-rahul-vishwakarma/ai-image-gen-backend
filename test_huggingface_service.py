"""
Test script to verify Hugging Face Stable Diffusion integration
Run this to test if the HUGGIN_API_KEY is configured correctly
"""
import asyncio
from app.services.huggingface_service import huggingface_service
from app.schemas.generation import GenerationCreate


async def test_image_generation():
    """Test image generation with Hugging Face Stable Diffusion"""
    print("=" * 70)
    print("Testing Hugging Face Image Generation")
    print("=" * 70)
    print()

    # Create test data with a simple prompt
    test_data = GenerationCreate(
        prompt="A beautiful sunset over mountains with orange and pink sky"
    )

    try:
        print(f"Model: Stable Diffusion v1.5 (RunwayML)")
        print(f"Prompt: {test_data.prompt}")
        print()
        print("Generating image...")
        print("(This may take 10-30 seconds on first request as model loads)")
        print()

        # Generate image using Hugging Face
        image_data = await huggingface_service.generate_image(test_data)

        print("✅ Success! Image generated")
        print()
        print(f"Image data format: Base64 encoded PNG")
        print(f"Data length: {len(image_data)} characters")
        print(f"Preview: {image_data[:80]}...")
        print()
        print("💡 The image is base64 encoded and can be:")
        print("   1. Stored directly in the database")
        print("   2. Displayed in HTML: <img src='data:image/png;base64,...' />")
        print("   3. Decoded and saved as a file")
        print()

        # Test saving to file
        print("Testing file save...")
        file_path = "test_generated_image.png"
        await huggingface_service.generate_image_with_file(test_data, file_path)
        print(f"✅ Image also saved to: {file_path}")
        print()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("Make sure your HUGGIN_API_KEY is set correctly in the .env file")
        print("Get your API key from: https://huggingface.co/settings/tokens")


if __name__ == "__main__":
    asyncio.run(test_image_generation())
