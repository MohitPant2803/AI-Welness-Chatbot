import logging
import json
from fastapi import APIRouter, Request
from server.models.user import User
from server.models.sound import Sounds
from server.models.admindbemp import Admindbemp
import redis.asyncio as redis
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

user_router = APIRouter()

redisClient = redis.Redis(host="localhost", port=6379, decode_responses=True)

def create_response(success: bool, message: str, data=None, code=200):
    return {"success": success, "message": message, "data": data, "code": code}

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@user_router.get("/user")
async def get_user(request: Request):
    try:
        employeeID = getattr(request.state, "empid", None)
        if not employeeID:
            logger.warning("Unauthorized access attempt - empid not found in request")
            return create_response(False, "Token is invalid: empid not found", code=401)

        cached_item = await redisClient.get(f"user/details/{employeeID}")
        if cached_item:
            data = json.loads(cached_item)
            return create_response(True, "User details fetched successfully", {"userDetails": data})

        user_data = await User.find_one(User.empid == employeeID)
        if not user_data:
            logger.warning(f"User not found for empid: {employeeID}")
            return create_response(False, "User not found", code=404)
        
        user_dict = user_data.model_dump()
        user_dict["id"] = str(user_dict.pop("_id", ""))

        await redisClient.set(
            f"user/details/{employeeID}", 
            json.dumps(user_dict, default=serialize_datetime), 
            ex=3600
        )

        logger.info(f"User data retrieved successfully for empid: {employeeID}")
        return create_response(True, "User data retrieved successfully", {"userDetails": user_dict})

    except Exception as e:
        logger.error(f"Error retrieving user for empid {employeeID}: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)
    
@user_router.get("/user/chats")
async def get_user_chats(request: Request):
    try:
        employeeID = getattr(request.state, "empid", None)
        if not employeeID:
            logger.warning("Unauthorized access attempt - empid not found in request")
            return create_response(False, "Token is invalid: empid not found", code=401)

        cached_item = await redisClient.get(f"user/chats/{employeeID}")
        if cached_item:
            data = json.loads(cached_item)
            return create_response(True, "User chats fetched successfully", {"userChats": data})

        user_data = await User.find_one(User.empid == employeeID)
        if not user_data:
            logger.warning(f"User not found for empid: {employeeID}")
            return create_response(False, "User not found", code=404)
        emp_data = await Admindbemp.find_one(Admindbemp.briefUserDetails.empid == employeeID)
        if not emp_data:
            logger.warning(f"Employee data not found for empid: {employeeID}")
            return create_response(False, "Employee data not found", code=404)
        
        new_user_data = {
            "empid": emp_data.briefUserDetails.empid,
            "name": emp_data.briefUserDetails.name,
            "chats": [
                {
                    "message": chat.message,
                    "timestamp": chat.timestamp,
                    "sender": chat.sender
                }
                for chat in emp_data.chatHistory
            ],
            "lastActive": emp_data.briefUserDetails.lastActive,
            "levelProgress": user_data.levelProgress,
            "level": user_data.level,
            "streakDays": user_data.streakDays,
            "wellnessPoints": user_data.wellnessPoints
        }

        await redisClient.set(
            f"user/chats/{employeeID}", 
            json.dumps(new_user_data, default=serialize_datetime), 
            ex=3600
        )

        logger.info(f"User chats retrieved successfully for empid: {employeeID}")
        return create_response(True, "User chats retrieved successfully", {"userChats": new_user_data})

    except Exception as e:
        logger.error(f"Error retrieving user chats for empid {employeeID}: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)

@user_router.get("/sounds")
async def get_all_sounds(request: Request):
    try:
        # Check for cached sounds
        cached_sounds = await redisClient.get("sounds/all")
        if cached_sounds:
            sounds_data = json.loads(cached_sounds)
            return create_response(True, "Sounds fetched successfully from cache", {"sounds": sounds_data})
        
        # Fetch raw documents from MongoDB directly
        sounds_collection = Sounds.get_motor_collection()
        sounds_cursor = sounds_collection.find({})
        sounds_list = await sounds_cursor.to_list(length=None)
        
        if not sounds_list:
            logger.info("No sounds found in database")
            return create_response(True, "No sounds found", {"sounds": []})
        
        # Process the MongoDB documents
        for sound in sounds_list:
            # Convert ObjectId to string
            sound["_id"] = str(sound["_id"])
        
        # Cache the results for 1 hour
        await redisClient.set(
            "sounds/all", 
            json.dumps(sounds_list, default=serialize_datetime),
            ex=3600
        )
        
        logger.info(f"Successfully retrieved {len(sounds_list)} sounds")
        return create_response(True, "Sounds fetched successfully", {"sounds": sounds_list})
    
    except Exception as e:
        logger.error(f"Error retrieving sounds: {str(e)}", exc_info=True)
        return create_response(False, f"Internal Server Error: {str(e)}", code=500)