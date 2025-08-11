from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    print("MongoDB connected")

async def close_mongo_connection():
    db.client.close()
    print("MongoDB connection closed")
