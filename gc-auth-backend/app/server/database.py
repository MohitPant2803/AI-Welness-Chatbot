from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from server.models.auth import Auth
from server.models.user import User
from server.models.adminAuth import Admin
from server.models.admindb import Admindb
from server.models.admindball import Admindball
from server.models.admindbemp import Admindbemp
from server.models.sound import Sounds
from server.models.meet import Meet

from server.config import MONGO_URI

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Auth, User, Admin, Admindb, Admindball, Admindbemp, Sounds, Meet])