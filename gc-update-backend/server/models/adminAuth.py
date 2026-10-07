from beanie import Document
from pydantic import BaseModel

class Admin(Document):
    adminid: str
    password: str
    token: str

    class Settings:
        collection = "admin"

    class Config:
        json_schema_extra = {
            "example": {
                "adminid": "ADM1234",
                "password": "securepassword",
                "token": "randomtoken123"
            }
        }

class AdminAuth(BaseModel):
    adminid: str
    password: str