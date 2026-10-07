from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime

class BriefUserDetails(BaseModel):
    name: str
    empid: str
    dept: str
    lastActive: datetime
    currentMood: str
    isEscalated: bool
    briefMoodSummary: str
    avatarUrl: str
    teamMessages: int
    emailsSent: int
    meetings: int
    workHours: int

class PastMoodTrend(BaseModel):
    date: datetime
    mood: str

class Badge(BaseModel):
    name: str
    icon: str
    description: str
    slug: str

class CompanyAward(BaseModel):
    awardType: str
    awardDate: datetime
    rewardPoints: int

class LeaveHistory(BaseModel):
    leaveType: str
    numberOfDays: int
    startDate: datetime
    endDate: datetime

class ChatHistory(BaseModel):
    message: str
    timestamp: datetime
    sender: str

class Admindbemp(Document):
    briefUserDetails: BriefUserDetails
    pastFiveMoodTrends: List[PastMoodTrend]
    currentMoodRate: str
    moodAnalysis: str
    recommendedAction: str
    earnedBadges: List[Badge]
    companyAwards: List[CompanyAward]
    leaveHistory: List[LeaveHistory]
    chatHistory: List[ChatHistory]
    chatAIAnalysis: str

    class Settings:
        collection = "admindbemp"