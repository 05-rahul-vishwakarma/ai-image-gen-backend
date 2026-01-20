from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = "AI Image Generator"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, production

    # MongoDB
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")

    # JWT
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # CORS
    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # OpenAI
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    HUGGIN_API_KEY: str = Field(...,env='HUGGIN_API_KEY')

    # Cloudinary (Optional)
    CLOUDINARY_CLOUD_NAME: str = Field(..., env="CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str = Field(..., env="CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = Field(...,env="CLOUDINARY_API_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
