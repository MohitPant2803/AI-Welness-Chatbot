from .celery import app
from models.user import User
from models.admindb import Admindb
from models.admindball import Admindball
from models.admindbemp import Admindbemp
from models.user import TrendEntry
from models.user import VibeEntry
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from server.config import MONGO_URI
import math

ctr = 0

async def ensure_db_initialized():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        global ctr
        ctr+=1
        print("="*40)
        print(f"INIT DB CALLED {ctr} times")
        print("="*40)
        db = client.get_default_database()
        await init_beanie(database=db, document_models=[User, Admindb, Admindball, Admindbemp])
    except Exception as e:
        print(f"Database initialization failed: {e}")

async def updatePerChatAsync(currentMood: str, isEscalated: bool, briefMoodSummary: str, currentMoodRate: str, userChat: str, botChat: str, empid: str, wellnessScore: int, moodAnalysis: str, recommendedAction: str, chatAIAnalysis: str):
    try:
        from datetime import datetime, timedelta
        await ensure_db_initialized()

        user = await User.find_one(User.empid == empid)
        adminDB = await Admindb.find_one({})
        adminDBAll = await Admindball.find_one({})
        AdminDBEmp = await Admindbemp.find_one(Admindbemp.briefUserDetails.empid == empid)

        if not user:
            print(f"No user found with empid: {empid}")
        if user:
            user.wellnessPointEntry.chatCheckIn.points += 10
            
            if user.moodCalendar and len(user.moodCalendar) > 0:
                yesterday = datetime.now().date() - timedelta(days=1)
                today = datetime.now().date()
    
                last_mood = user.moodCalendar[-1]
                if hasattr(last_mood, 'timestamp') and hasattr(last_mood, 'moodLevel'):
                    last_mood_date = last_mood.timestamp.date()
    
                    if not user.isStreakBonusUpdated:
                        if last_mood_date == yesterday:
                            user.streakDays += 1
                            user.wellnessPointEntry.streakBonus.points += 10*user.streakDays
                            user.isStreakBonusUpdated = True
                        elif last_mood_date != today:
                            user.streakDays = 1
                            user.isStreakBonusUpdated = True
            else:
                user.streakDays = 1
                user.isStreakBonusUpdated = True
    
            user.wellnessPoints = (
                user.wellnessPointEntry.chatCheckIn.points +
                user.wellnessPointEntry.streakBonus.points +
                user.wellnessPointEntry.wellnessActivities.points
            )
    
            try:
                await user.save()
            except Exception as e:
                print(f"Error saving user: {e}")
    
        else:
            print(f"No user found with empid: {empid}")
    
        if adminDB:
            today = datetime.now().date()
            
            today_entry = None
            for entry in adminDB.dailyChatParticipation:
                if entry.date.date() == today:
                    today_entry = entry
                    break
                
            if today_entry:
                today_entry.numberOfParticipants += 1
            else:
                from models.admindb import DailyChatParticipation
                adminDB.dailyChatParticipation.append(
                    DailyChatParticipation(
                        date=datetime.now(),
                        numberOfParticipants=1
                    )
                )
            
            await adminDB.save()
        else:
            print("No Admindb found")
        

        user.levelProgress += 5
        if user.levelProgress >= 100:
            user.levelProgress -= 100
            user.level += 1
        user.wellnessScore = wellnessScore
        formatted_time = datetime.now()
        
        if AdminDBEmp:
            AdminDBEmp.briefUserDetails.lastActive = formatted_time
            AdminDBEmp.briefUserDetails.currentMood = currentMood
            AdminDBEmp.briefUserDetails.isEscalated = isEscalated
            AdminDBEmp.briefUserDetails.briefMoodSummary = briefMoodSummary
            AdminDBEmp.currentMoodRate = currentMoodRate
            AdminDBEmp.chatHistory.append({"message": userChat, "timestamp": formatted_time, "sender": "user"})
            AdminDBEmp.chatHistory.append({"message": botChat, "timestamp": formatted_time, "sender": "ai"})
            AdminDBEmp.moodAnalysis = moodAnalysis
            AdminDBEmp.chatAIAnalysis = chatAIAnalysis
            AdminDBEmp.recommendedAction = recommendedAction


        if adminDBAll:
            for user_details in adminDBAll.briefTotalUsersList:
                if user_details.empid == empid:
                    user_details.currentMood = currentMood
                    user_details.lastActive = formatted_time
                    user_details.isEscalated = isEscalated
                    user_details.briefMoodSummary = briefMoodSummary
                    break

        if adminDB:
            adminDB.totalChatInteractions += 1

            flag = 0
            idx = -1
            for i, escalated_user in enumerate(adminDB.briefEscalatedUsersList):
                if escalated_user.empid == empid:
                    if not isEscalated:
                        flag = -1
                        idx = i
                    else:
                        flag = 1
                    break

            if flag == 0 and isEscalated:
                adminDB.briefEscalatedUsersList.append({
                    "name": user.name,
                    "empid": empid,
                    "dept": user.dept,
                    "lastActive": formatted_time,
                    "currentMood": currentMood,
                    "isEscalated": isEscalated,
                    "briefMoodSummary": briefMoodSummary,
                    "avatarUrl": user.avatar
                })
                adminDB.noOfEscalatedIssues += 1

            if flag == -1:
                adminDB.briefEscalatedUsersList.pop(idx)
                adminDB.noOfEscalatedIssues -= 1

        await user.save()
        if AdminDBEmp:
            await AdminDBEmp.save()
        if adminDB:
            await adminDB.save()
        if adminDBAll:
            await adminDBAll.save()

    except Exception as e:
        print("Some error occurred:", e)

@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=3)
def updatePerChat(self, currentMood: str, isEscalated: bool, briefMoodSummary: str, currentMoodRate: str, userChat: str, botChat: str, empid: str, wellnessScore: int, moodAnalysis: str, recommendedAction: str, chatAIAnalysis: str):
    asyncio.run(updatePerChatAsync(
        currentMood=currentMood, isEscalated=isEscalated, briefMoodSummary=briefMoodSummary,
        currentMoodRate=currentMoodRate, userChat=userChat, botChat=botChat, empid=empid,
        wellnessScore=wellnessScore, moodAnalysis=moodAnalysis, recommendedAction=recommendedAction, chatAIAnalysis=chatAIAnalysis
    ))

async def EODTaskAsync():
    await ensure_db_initialized()
    consistencyChampionBadge = {
        "name":"Consistency Champion",
        "description":"Checked in for 30 days",
        "slug":"consistency-champion",
        "icon":""
    }
    wellnessWarriorBadge = {
        "name":"Wellness Warrior",
        "description":"Maintain balance for a month",
        "slug":"wellness-warrior",
        "icon":""
    }
    growthGuruBadge = {
        "name":"Growth Guru",
        "description":"Showed a positive trend for 3 weeks",
        "slug":"growth-guru",
        "icon":""
    }

    try:
        users = await User.find({}).to_list(length=None)
        adminDB = await Admindb.find_one({})
        totalAngry = 0
        totalSad = 0
        totalNeutral = 0
        totalTendingToHappy = 0
        totalHappy = 0
        if(users):
            for user in users:
                empid = user.empid
                AdminDBEmp = await Admindbemp.find_one(Admindbemp.briefUserDetails.empid == empid)
                user.moodCalendar.append(
                    VibeEntry(
                        moodLevel=math.ceil(user.wellnessScore / 20),
                        timestamp=datetime.now()
                    )
                )

                exists = any(item.slug == "consistency-champion" for item in user.earnedBadges)
                if not exists:
                    if user.streakDays >= 30:
                        user.earnedBadges.append(consistencyChampionBadge)
                        AdminDBEmp.earnedBadges.append(consistencyChampionBadge)
                        user.badgesToUnlock = [item for item in user.badgesToUnlock if item.slug != "consistency-champion"]
                
                exists = any(item.slug == "wellness-warrior" for item in user.earnedBadges)
                if not exists:
                    result = False
                    if len(user.moodCalendar) < 30:
                        result = False
                    else:
                        result = all(item.moodLevel >= 3 for item in user.moodCalendar[-30:])
                    if result:
                        user.earnedBadges.append(wellnessWarriorBadge)
                        AdminDBEmp.earnedBadges.append(wellnessWarriorBadge)
                        user.badgesToUnlock = [item for item in user.badgesToUnlock if item.slug != "wellness-warrior"]
                
                exists = any(item.slug == "growth-guru" for item in user.earnedBadges)
                if not exists:
                    result = False
                    if len(user.moodCalendar) < 21:
                        result = False
                    else:
                        result = all(item["moodLevel"] >= 4 for item in user.moodCalendar[-21:])
                    if result:
                        user.earnedBadges.append(growthGuruBadge)
                        AdminDBEmp.earnedBadges.append(growthGuruBadge)
                        user.badgesToUnlock = [item for item in user.badgesToUnlock if item.slug != "growth-guru"]
                
                count = 0
                for item in reversed(user.moodCalendar):
                    if item.moodLevel >= 4:
                        count += 1
                    else:
                        break

                user.recentTrends.improvingTrend = TrendEntry(
                    title="Improving Trend",
                    description="Last 1 Day" if count == 1 else f"Last {count} Days",
                    icon=None
                )

                user.recentTrends.consistentCheckIns = TrendEntry(
                    title="Consistent Check-Ins",
                    description="1 Day Streak" if user.streakDays == 1 else f"{user.streakDays} Day Streak",
                    icon=None
                )

                remark = ["angry", "sad", "neutral", "tending to happy", "happy"][(user.wellnessScore - 1) // 20]
                user.recentTrends.wellnessScore = TrendEntry(
                    title="Wellness Score",
                    description=f"{user.wellnessScore}/100 ({remark})",
                    icon=None
                )

                user.currentVibe = remark
                AdminDBEmp.pastFiveMoodTrends.pop(0)
                AdminDBEmp.pastFiveMoodTrends.append({
                    "date":datetime.now(),
                    "mood":remark.capitalize()
                })

                if remark == "angry":
                    totalAngry+=1
                elif remark == "sad":
                    totalSad+=1
                elif remark == "neutral":
                    totalNeutral+=1
                elif remark == "tending to happy":
                    totalTendingToHappy+=1
                elif remark == "happy":
                    totalHappy+=1

                user.isStreakBonusUpdated = False
                await user.save()
                await AdminDBEmp.save()
            
            adminDB.employeeMoodDistribution = {
                "angry":totalAngry,
                "sad":totalSad,
                "neutral":totalNeutral,
                "tendingToHappy":totalTendingToHappy,
                "happy":totalHappy
            }
            await adminDB.save()

    except Exception as e:
        print("Some error occured : ", e)

@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=3)
def EODTask(self):
    asyncio.run(EODTaskAsync())

async def updateAtSODAsync(empid: str):
    from datetime import datetime, timedelta
    await ensure_db_initialized()
    user = await User.find_one(User.empid == empid)
    if user:
        user.wellnessPointEntry.chatCheckIn.points += 10
        
        if user.moodCalendar and len(user.moodCalendar) > 0:
            yesterday = datetime.now().date() - timedelta(days=1)
            today = datetime.now().date()

            last_mood = user.moodCalendar[-1]
            if hasattr(last_mood, 'timestamp') and hasattr(last_mood, 'moodLevel'):
                last_mood_date = last_mood.timestamp.date()

                if not user.isStreakBonusUpdated:
                    if last_mood_date == yesterday:
                        user.streakDays += 1
                        user.wellnessPointEntry.streakBonus.points += 10*user.streakDays
                        user.isStreakBonusUpdated = True
                    elif last_mood_date != today:
                        user.streakDays = 1
                        user.isStreakBonusUpdated = True
        else:
            user.streakDays = 1
            user.isStreakBonusUpdated = True

        user.wellnessPoints = (
            user.wellnessPointEntry.chatCheckIn.points +
            user.wellnessPointEntry.streakBonus.points +
            user.wellnessPointEntry.wellnessActivities.points
        )

        try:
            await user.save()
        except Exception as e:
            print(f"Error saving user: {e}")

        else:
            print(f"No user found with empid: {empid}")

        admin_db = await Admindb.find_one({})
    if admin_db:
        today = datetime.now().date()
        
        today_entry = None
        for entry in admin_db.dailyChatParticipation:
            if entry.date.date() == today:
                today_entry = entry
                break
        
        if today_entry:
            today_entry.numberOfParticipants += 1
        else:
            from models.admindb import DailyChatParticipation
            admin_db.dailyChatParticipation.append(
                DailyChatParticipation(
                    date=datetime.now(),
                    numberOfParticipants=1
                )
            )
        
        await admin_db.save()
    else:
        print("No Admindb found")

@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=3)
def updateAtSOD(self, empid: str):
    asyncio.run(updateAtSODAsync(
        empid=empid
    ))

async def updateTeamMessagesAsync(empid:str, numberOfteamMessages:int):
    await ensure_db_initialized()
    user = await User.find_one(User.empid == empid)
    if user:
        user.numberOfteamMessages += numberOfteamMessages
        
        try:
            await user.save()
        except Exception as e:
            print(f"Error saving user: {e}")
    else:
        print(f"No user found with empid: {empid}")

@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=3)
def updateTeamMessages(self, empid: str, numberOfteamMessages:int):
    asyncio.run(updateTeamMessagesAsync(
        empid=empid,
        numberOfteamMessages=numberOfteamMessages
    ))
async def updateEmailsSendAsync(empid:str, numberOfemailsSent:int):
    await ensure_db_initialized()
    user = await User.find_one(User.empid == empid)
    if user:
        user.numberOfemailsSent += numberOfemailsSent
        
        try:
            await user.save()
        except Exception as e:
            print(f"Error saving user: {e}")
    else:
        print(f"No user found with empid: {empid}")

@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=3)
def updateEmailsSend(self, empid: str, numberOfemailsSent:int):
    asyncio.run(updateEmailsSendAsync(
        empid=empid,
        numberOfemailsSent=numberOfemailsSent
    ))



async def updateMeetingAsync(empid:str, numberOfmeetingsAttended:int):
    await ensure_db_initialized()
    user = await User.find_one(User.empid == empid)
    if user:
        user.numberOfmeetingsAttended += numberOfmeetingsAttended
        
        try:
            await user.save()
        except Exception as e:
            print(f"Error saving user: {e}")
    else:
        print(f"No user found with empid: {empid}")

@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=3)
def updateMeeting(self, empid: str, numberOfmeetingsAttended:int):
    asyncio.run(updateMeetingAsync(
        empid=empid,
        numberOfmeetingsAttended=numberOfmeetingsAttended
    ))

async def updateWorkHoursAsync(empid:str, workHours:int):
    await ensure_db_initialized()
    user = await User.find_one(User.empid == empid)
    if user:
        user.workHours = workHours
        
        try:
            await user.save()
        except Exception as e:
            print(f"Error saving user: {e}")
    else:
        print(f"No user found with empid: {empid}")

@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=3)
def updateWorkHours(self, empid: str, workHours:int):
    asyncio.run(updateWorkHoursAsync(
        empid=empid,
        workHours=workHours
    ))