from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime

class BriefTotalUser(BaseModel):
    name: str
    empid: str
    dept: str
    lastActive: datetime
    currentMood: str
    isEscalated: bool
    briefMoodSummary: str
    avatarUrl: str

class Admindball(Document):
    briefTotalUsersList: List[BriefTotalUser]

    class Settings:
        collection = "admindball"