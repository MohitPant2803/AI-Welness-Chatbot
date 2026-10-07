from beanie import Document
from pydantic import BaseModel

class Auth(Document):
    empid: str
    password: str
    token: str

    class Settings:
        collection = "auth"
        indexes = [
            "empid"
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "empid": "EMP12345",
                "password": "securepassword",
                "token": "randomtoken123"
            }
        }

class AuthAuth(BaseModel):
    empid: str
    password: str