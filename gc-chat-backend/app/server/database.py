from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from server.models.user import Chat

from server.config import MONGO_URI

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Chat])
