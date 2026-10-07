from beanie import Document
from pydantic import BaseModel

class Chat(Document):
    empid: str
    password: str
    token: str

    class Settings:
        collection = "chat"

    class Config:
        json_schema_extra = {
            "example": {
                "empid": "EMP12345",
                "password": "securepassword",
                "token": "randomtoken123"
            }
        }

class ChatAuth(BaseModel):
    empid: str
    password: str