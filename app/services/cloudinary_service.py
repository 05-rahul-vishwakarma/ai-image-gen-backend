# Import Cloudinary SDK for image upload and management
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import base64 for decoding base64 images
import base64

# Import BytesIO for handling image data in memory
from io import BytesIO

# Import settings to access Cloudinary credentials from environment variables
from app.core.config import settings


class CloudinaryService:
    """Service for handling Cloudinary image storage and URL generation"""

    def __init__(self):
        # Configure Cloudinary with credentials from settings
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True  # Use HTTPS URLs
        )

    def upload_base64_image(self, base64_image: str, folder: str = "ai-generated") -> str:
        """
        Upload a base64 encoded image to Cloudinary and return the URL

        Args:
            base64_image: Base64 encoded image string (with or without data URI prefix)
            folder: Cloudinary folder to store the image in (default: "ai-generated")

        Returns:
            str: Public URL of the uploaded image

        Raises:
            Exception: If upload fails or image format is invalid
        """
        try:
            # Remove data URI prefix if present (e.g., "data:image/png;base64,")
            if "base64," in base64_image:
                base64_image = base64_image.split("base64,")[1]

            # Upload the base64 image to Cloudinary
            # Cloudinary automatically detects image format and optimizes
            upload_result = cloudinary.uploader.upload(
                f"data:image/png;base64,{base64_image}",
                folder=folder,  # Organize images in folders
                resource_type="image",  # Specify resource type
                overwrite=True,  # Allow overwriting existing files
                invalidate=True  # Invalidate CDN cache for updated images
            )

            # Return the secure URL (HTTPS) of the uploaded image
            return upload_result["secure_url"]

        except Exception as e:
            raise Exception(f"Failed to upload image to Cloudinary: {str(e)}")

    def upload_file_image(self, file_path: str, folder: str = "ai-generated") -> str:
        """
        Upload an image file to Cloudinary and return the URL

        Args:
            file_path: Path to the image file to upload
            folder: Cloudinary folder to store the image in (default: "ai-generated")

        Returns:
            str: Public URL of the uploaded image

        Raises:
            Exception: If upload fails or file not found
        """
        try:
            # Upload the file to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file_path,
                folder=folder,
                resource_type="image",
                overwrite=True,
                invalidate=True
            )

            # Return the secure URL of the uploaded image
            return upload_result["secure_url"]

        except Exception as e:
            raise Exception(f"Failed to upload file to Cloudinary: {str(e)}")

    def upload_bytes_image(self, image_bytes: bytes, folder: str = "ai-generated", public_id: str = None) -> str:
        """
        Upload image bytes to Cloudinary and return the URL

        Args:
            image_bytes: Raw image bytes
            folder: Cloudinary folder to store the image in (default: "ai-generated")
            public_id: Optional custom public ID for the image

        Returns:
            str: Public URL of the uploaded image

        Raises:
            Exception: If upload fails
        """
        try:
            # Create BytesIO object from bytes
            image_buffer = BytesIO(image_bytes)

            # Upload the image bytes to Cloudinary
            upload_result = cloudinary.uploader.upload(
                image_buffer,
                folder=folder,
                resource_type="image",
                public_id=public_id,
                overwrite=True,
                invalidate=True
            )

            # Return the secure URL of the uploaded image
            return upload_result["secure_url"]

        except Exception as e:
            raise Exception(f"Failed to upload bytes to Cloudinary: {str(e)}")

    def delete_image(self, public_id: str) -> bool:
        """
        Delete an image from Cloudinary by public ID

        Args:
            public_id: The public ID of the image to delete

        Returns:
            bool: True if deletion was successful

        Raises:
            Exception: If deletion fails
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
        except Exception as e:
            raise Exception(f"Failed to delete image from Cloudinary: {str(e)}")


# Create a singleton instance of CloudinaryService
# This creates one shared instance that can be imported and used throughout the app
cloudinary_service = CloudinaryService()
