from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models import User, Generation, Session

client = None


async def init_db():
    """Initialize database connection and Beanie ODM"""
    global client
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000  # 5 second timeout
        )
        # Test connection
        await client.admin.command('ping')

        await init_beanie(
            database=client[settings.DATABASE_NAME],
            document_models=[User, Generation, Session],
        )
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"⚠️  MongoDB not connected: {e}")
        print("⚠️  Running without database (some features won't work)")


async def close_db():
    """Close database connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")
