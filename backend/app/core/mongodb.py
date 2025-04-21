from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.mongodb import User, Channel, Post, ChannelMetrics

async def init_mongodb():
    """Initialize MongoDB connection and register models"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[
            User,
            Channel,
            Post,
            ChannelMetrics
        ]
    )

async def get_database():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    return client[settings.MONGODB_DB_NAME] 