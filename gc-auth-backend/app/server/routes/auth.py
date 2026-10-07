from fastapi import APIRouter
from server.models.auth import Auth, AuthAuth
import bcrypt
import datetime
import jwt
import logging
from server.config import JWT_SECRET
from fastapi.responses import JSONResponse

auth_router = APIRouter()

logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)

def create_response(success: bool, message: str, data=None, code=200):
    return JSONResponse(content={"success": success, "message": message, "data": data, "code": code}, status_code=code)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

async def encode_empid(empid: str) -> str:
    payload = {
        "empid": empid,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

@auth_router.post("/signup")
async def signup_user(auth: AuthAuth):
    try:
        existing_user = await Auth.find_one(Auth.empid == auth.empid)
        if existing_user:
            logger.warning(f"Signup attempt failed: User {auth.empid} already exists")
            return create_response(False, "User already exists", code=400)

        hashpwd = hash_password(auth.password)
        new_user = Auth(empid=auth.empid, password=hashpwd, token="")
        await new_user.insert()

        logger.info(f"User {auth.empid} created successfully")
        return create_response(True, "User created successfully", code=201)

    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        return create_response(False, "Internal server error", code=500)

@auth_router.post("/signin")
async def signin_user(auth: AuthAuth):
    try:
        user = await Auth.find_one(Auth.empid == auth.empid)
        if not user:
            logger.warning(f"Signin failed: User {auth.empid} does not exist")
            return create_response(False, "User does not exist", code=401)

        if not verify_password(auth.password, user.password):
            logger.warning(f"Signin failed: Invalid password for {auth.empid}")
            return create_response(False, "Invalid password", code=403)

        token = await encode_empid(auth.empid)
        user.token = token
        await user.save()

        logger.info(f"User {auth.empid} signed in successfully")
        
        return create_response(True, "Login successful", data={"token": token})

    except Exception as e:
        logger.error(f"Signin error: {str(e)}", exc_info=True)
        return create_response(False, "Internal server error", code=500)