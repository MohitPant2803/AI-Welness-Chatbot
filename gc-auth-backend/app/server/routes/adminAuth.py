from fastapi import APIRouter
from server.models.adminAuth import Admin, AdminAuth
import bcrypt
import datetime
import jwt
import logging
from server.config import JWT_SECRET
import redis.asyncio as redis
import json

admin_auth_router = APIRouter()

logger = logging.getLogger("admin_auth")
logger.setLevel(logging.INFO)

redisClient = redis.Redis(host="localhost", port=6379, decode_responses=True)

def create_response(success: bool, message: str, data=None, code=200):
    return {"success": success, "message": message, "data": data, "code": code}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

async def encode_adminid(adminid: str) -> str:
    payload = {
        "adminid": adminid,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

@admin_auth_router.post("/signup")
async def signup_user(auth: AdminAuth):
    try:
        existing_user = await Admin.find_one(Admin.adminid == auth.adminid)
        if existing_user:
            logger.warning(f"Signup attempt failed: Admin {auth.adminid} already exists")
            return create_response(False, "Admin already exists", code=400)

        hashed_password = hash_password(auth.password)
        new_admin = Admin(adminid=auth.adminid, password=hashed_password, token="")
        await new_admin.insert()
        await redisClient.delete("allAdmin")
        logger.info(f"Admin {auth.adminid} created successfully")
        return create_response(True, "Admin created successfully", code=201)

    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        return create_response(False, "Internal server error", code=500)

@admin_auth_router.post("/signin")
async def signin_user(auth: AdminAuth):
    try:
        admin = await Admin.find_one(Admin.adminid == auth.adminid)
        if not admin:
            logger.warning(f"Signin failed: Admin {auth.adminid} does not exist")
            return create_response(False, "Admin does not exist", code=401)

        if not verify_password(auth.password, admin.password):
            logger.warning(f"Signin failed: Invalid password for {auth.adminid}")
            return create_response(False, "Invalid password", code=403)

        token = await encode_adminid(auth.adminid)
        admin.token = token
        await admin.save()
        await redisClient.delete("allAdmin")
        logger.info(f"Admin {auth.adminid} signed in successfully")
        return create_response(True, "Login successful", {"token": token})

    except Exception as e:
        logger.error(f"Signin error: {str(e)}", exc_info=True)
        return create_response(False, "Internal server error", code=500)

# @admin_auth_router.get("/users")
# async def get_users():
#     try:
#         cached_item = await redisClient.get("allAdmin")
#         if cached_item:
#             data = json.loads(cached_item)
#             return create_response(True, "Admins fetched successfully", {"admins": data})
#         users = await Admin.find_all().to_list()
#         users_serialized = [
#             {
#                 "id": str(user.id),
#                 "adminid": user.adminid,
#                 "password": user.password,
#                 "token": user.token
#             }
#             for user in users
#         ]
#         await redisClient.set("allAdmin", json.dumps(users_serialized), ex=3600)
#         return create_response(True, "Admins fetched successfully", {"admins": users_serialized})
#     except Exception as e:
#         logger.error(f"Get users error: {str(e)}", exc_info=True)
#         return create_response(False, "Internal server error", code=500)