from huggingface_hub import InferenceClient
from io import BytesIO
from app.core.config import settings
from app.schemas.generation import GenerationCreate
from app.services.cloudinary_service import cloudinary_service


class HuggingFaceService:
    """Service for handling Hugging Face API interactions for image generation"""

    def __init__(self):
        self.client = InferenceClient(
            provider="nscale",
            api_key=settings.HUGGIN_API_KEY
        )
        self.model = "stabilityai/stable-diffusion-xl-base-1.0"


    async def generate_image(self, data: GenerationCreate) -> str:
        try:
            # Use InferenceClient to generate image from text prompt
            # This returns a PIL.Image object
            image = self.client.text_to_image(
            prompt=data.prompt,
            model=self.model,
            width=540,          # ✅ image width
            height=540,         # ✅ image height
            guidance_scale=7.5,  # optional (CFG scale)
            num_inference_steps=30,  # optional
            seed=42              # optional (for reproducibility)
            )


            print(image.show(), 'hugging face response')

            # Convert PIL Image to bytes for Cloudinary upload
            # Create a BytesIO buffer to hold the image data
            img_buffer = BytesIO()
            image.save(img_buffer, format='PNG')  # Save image as PNG to buffer
            img_buffer.seek(0)  # Reset buffer position to beginning

            # Upload the image directly to Cloudinary
            # This returns the secure HTTPS URL of the uploaded image
            cloudinary_url = cloudinary_service.upload_bytes_image(
                image_bytes=img_buffer.getvalue(),  # Get bytes from buffer
                folder="ai-generated",  # Store in ai-generated folder
                public_id=None  # Let Cloudinary auto-generate ID
            )

            # print(f"Image uploaded to Cloudinary: {cloudinary_url}")

            return cloudinary_url

        except Exception as e:
            # Catch any errors (API failures, network issues, authentication errors, etc.)
            # Re-raise with a descriptive error message
            raise Exception(f"Failed to generate image with Hugging Face: {str(e)}")


huggingface_service = HuggingFaceService()
