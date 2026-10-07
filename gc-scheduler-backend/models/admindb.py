from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime

class EmployeeMoodDistribution(BaseModel):
    happy: int
    tendingToHappy: int
    neutral: int
    sad: int
    angry: int

class DailyChatParticipation(BaseModel):
    date: datetime
    numberOfParticipants: int

class BriefEscalatedUser(BaseModel):
    name: str
    empid: str
    dept: str
    lastActive: datetime
    currentMood: str
    isEscalated: bool
    briefMoodSummary: str
    avatarUrl: str

class Admindb(Document):
    totalNumberOfEmp: int
    noOfHappyEmp: int
    noOfEscalatedIssues: int
    totalChatInteractions: int
    employeeMoodDistribution: EmployeeMoodDistribution
    dailyChatParticipation: List[DailyChatParticipation]
    hikeFromPrevMonth: int
    briefEscalatedUsersList: List[BriefEscalatedUser]

    class Settings:
        collection = "admindb"
        indexes = [
            "totalNumberOfEmp",
            "noOfHappyEmp",
            "noOfEscalatedIssues",
            "totalChatInteractions",
            "hikeFromPrevMonth",
        ]