from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, Any

class Sounds(Document):
    # Remove the _id field definition to let Beanie handle it automatically
    id: int  # This is your custom id field, not the MongoDB _id
    name: str
    description: str
    shortDescription: str
    isPopular: bool
    genre: str
    url: str
    thumbnailUrl: str
    length: str

    class Settings:
        collection = "sounds"
        indexes = [
            "id",
            "name",
            "genre"
        ]

class SoundsCreate(BaseModel):
    id: int
    name: str
    description: str
    shortDescription: str
    isPopular: bool
    genre: str
    url: str
    thumbnailUrl: str
    length: str