# Import the OpenAI client library to interact with OpenAI's API
from openai import OpenAI

# Import the settings module to access environment variables (API keys, config)
from app.core.config import settings

# Import the GenerationCreate schema for type validation of incoming requests
from app.schemas.generation import GenerationCreate


class OpenAIService:
    """Service for handling OpenAI API interactions"""

    def __init__(self):
        """
        Initialize the OpenAI service
        Creates an OpenAI client instance with the API key from environment variables
        """
        # Create OpenAI client with API key loaded from .env file via settings
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_image(self, data: GenerationCreate) -> str:
        """
        Generate an image using OpenAI's DALL-E API

        Args:
            data: GenerationCreate schema with prompt and settings

        Returns:
            str: URL of the generated image

        Raises:
            Exception: If image generation fails
        """
        try:
            print(data,'data')
            # Get settings from request data, use empty dict if no settings provided
            settings_data = data.settings or {}

            # Extract the AI model to use (default: dall-e-3 if not specified)
            # getattr safely gets the 'model' attribute or returns the default value
            model = getattr(settings_data, 'model', 'dall-e-3')

            # Extract the style parameter (e.g., 'vivid' or 'natural')
            # Returns None if not specified
            style = getattr(settings_data, 'style', None)

            # DALL-E 3 only supports specific image sizes:
            # - 1024x1024 (square)
            # - 1024x1792 (portrait)
            # - 1792x1024 (landscape)
            # We use 1024x1024 as the default size for generated images
            size = "1024x1024"

            # Build the dictionary of parameters to send to OpenAI API
            request_params = {
                "model": model,              # Which DALL-E model to use (dall-e-3 or dall-e-2)
                "prompt": data.prompt,       # The text description of the image to generate
                "size": size,                # The size of the generated image
                "quality": "standard",       # Image quality: "standard" or "hd" (higher quality, more expensive)
                "n": 1,                      # Number of images to generate (always 1 for DALL-E 3)
            }

            # If style is provided and we're using dall-e-3, add it to request
            # Style can be "vivid" (dramatic, hyper-real) or "natural" (more realistic)
            # Note: style parameter only works with dall-e-3, not dall-e-2
            if style and model == "dall-e-3":
                request_params["style"] = style

            # Make the actual API call to OpenAI to generate the image
            # This sends the request and waits for OpenAI to create the image
            # The ** operator unpacks the request_params dictionary as keyword arguments
            response = self.client.images.generate(**request_params)

            # Check if the response contains generated images
            # response.data is a list of generated images
            # We check if it exists and has at least one image
            if response.data and len(response.data) > 0:
                # Extract the URL of the first (and only) generated image
                # OpenAI hosts the image temporarily and provides a URL to access it
                image_url = response.data[0].url

                # Return the image URL so it can be saved to the database
                return image_url
            else:
                # If no images were generated, raise an error
                raise Exception("No image generated in response")

        except Exception as e:
            # Catch any errors (API failures, network issues, invalid parameters, etc.)
            # Re-raise with a more descriptive error message
            raise Exception(f"Failed to generate image: {str(e)}")

    async def generate_image_variation(self, image_path: str, n: int = 1, size: str = "1024x1024") -> list[str]:
        """
        Create a variation of an existing image
        This is a bonus feature that creates similar versions of an uploaded image

        Args:
            image_path: Path to the original image file on the filesystem
            n: Number of variations to generate (default: 1)
            size: Size of the generated images (default: "1024x1024")

        Returns:
            list[str]: List of URLs of generated image variations

        Raises:
            Exception: If variation creation fails
        """
        try:
            # Open the image file in binary read mode ("rb")
            # Using 'with' ensures the file is properly closed after use
            with open(image_path, "rb") as image_file:
                # Call OpenAI API to create variations of the uploaded image
                # This generates new images that are similar to the original
                response = self.client.images.create_variation(
                    image=image_file,  # The original image file object
                    n=n,               # How many variations to create
                    size=size          # Size of each variation image
                )

            # Extract URLs from all generated variations
            # List comprehension loops through response.data and gets each image's URL
            # Returns a list of URLs (one for each generated variation)
            return [img.url for img in response.data]

        except Exception as e:
            # Catch any errors (file not found, API failures, invalid image format, etc.)
            # Re-raise with a descriptive error message
            raise Exception(f"Failed to create image variation: {str(e)}")


# Create a singleton instance of OpenAIService
# This creates one shared instance that can be imported and used throughout the app
# Using a singleton avoids creating multiple OpenAI client instances (more efficient)
openai_service = OpenAIService()
