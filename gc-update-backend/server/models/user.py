from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime

class Badge(BaseModel):
    name: str
    icon: str
    description: str
    slug: str

class Leave(BaseModel):
    leaveType: str
    numberOfDays: int
    startDate: datetime
    endDate: datetime

class Award(BaseModel):
    awardType: str
    awardDate: datetime
    rewardPoints: int

class VibeEntry(BaseModel):
    moodLevel: int  # Scale of 1-4
    timestamp: datetime

class Reward(BaseModel):
    icon: str
    name: str
    pointsRequired: int
    redeemedOn: datetime | None = None  # None if not redeemed

class CompanyAward(BaseModel):
    title: str
    dateReceived: datetime
    description: str

class TrendEntry(BaseModel):
    title: str  # e.g., "Improving Trend"
    description: str  # e.g., "Last 7 days"
    icon: str | None = None  # Optional icon (can be a URL or an emoji)

class TrendEntryArray(BaseModel):
    improvingTrend: TrendEntry
    consistentCheckIns: TrendEntry
    wellnessScore: TrendEntry

class wellnessPointEntry(BaseModel):
    points: int
    description: str

class wellnessPointEntryArray(BaseModel):
    chatCheckIn: wellnessPointEntry
    wellnessActivities: wellnessPointEntry
    streakBonus: wellnessPointEntry

class User(Document):
    empid: str
    name: str
    streakDays: int  # Tracks consistency
    wellnessScore: int  # Score out of 100
    numberOfteamMessages: int
    numberOfemailsSent: int
    dept: str
    role: str
    joinedOn: datetime
    level: int
    levelProgress: int
    moodCalendar: List[VibeEntry] 
    recentTrends: TrendEntryArray
    numberOfmeetingsAttended: int
    workHours: int
    currentVibe: str
    vibeHistory: List[VibeEntry]
    earnedBadges: List[Badge]
    badgesToUnlock: List[Badge]  # Future milestone badges
    wellnessPoints: int  # Renamed from `coins`
    changedThisWeek: int
    wellnessPointEntry:wellnessPointEntryArray 
    avaiableRewards: List[Reward]
    pastRewards: List[Reward]
    avatar: str
    leaves: List[Leave]
    awards: List[Award]
    companyAwards: List[CompanyAward]  # Professional recognition

    class Settings:
        collection = "user"
        indexes = [
            "empid",
            "streakDays",
            "numberOfteamMessages",
            "numberOfemailsSent",
            "numberOfmeetingsAttended",
            "workHours",
            "currentVibe",
            "wellnessPoints",
        ]

class User(Document):
    empid: str
    name: str
    streakDays: int  # Tracks consistency
    wellnessScore: int  # Score out of 100
    numberOfteamMessages: int
    numberOfemailsSent: int
    dept: str
    role: str
    joinedOn: datetime
    level: int
    levelProgress: int
    moodCalendar: List[VibeEntry] 
    recentTrends: TrendEntryArray
    numberOfmeetingsAttended: int
    workHours: int
    currentVibe: str
    vibeHistory: List[VibeEntry]
    earnedBadges: List[Badge]
    badgesToUnlock: List[Badge]  # Future milestone badges
    wellnessPoints: int  # Renamed from `coins`
    changedThisWeek: int
    wellnessPointEntry:wellnessPointEntryArray 
    avaiableRewards: List[Reward]
    pastRewards: List[Reward]
    avatar: str
    leaves: List[Leave]
    awards: List[Award]
    companyAwards: List[CompanyAward]  # Professional recognition