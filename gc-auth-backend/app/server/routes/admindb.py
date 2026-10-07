import os
import logging
from fastapi import APIRouter
import redis.asyncio as redis
import json
from server.models.admindb import Admindb
from server.models.admindball import Admindball
from server.models.admindbemp import Admindbemp
from server.models.search import vector_search
from server.models.meet import Meet
from datetime import datetime
from bson import ObjectId
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


admindb_router = APIRouter()

redisClient = redis.Redis(host="localhost", port=6379, decode_responses=True)

def create_response(success: bool, message: str, data=None, code=200):
    return {"success": success, "message": message, "data": data, "code": code}

def custom_serializer(obj):
    """Handle MongoDB ObjectId, datetime, and custom class serialization"""
    if isinstance(obj, ObjectId):
        return {"$oid": str(obj)}
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "dict"):
        return obj.dict()
    elif hasattr(obj, "__dict__"):
        return {k: custom_serializer(v) for k, v in obj.__dict__.items()}
    return str(obj)

@admindb_router.get("/db")
async def get_admindb():
    try:
        cached_item = await redisClient.get("admindb")
        if cached_item:
            data = json.loads(cached_item)
            return create_response(True, "Data retrieved successfully", data)
        
        admindb_data = await Admindb.find_one({})
        if not admindb_data:
            logger.warning("AdminDB data not found")
            return create_response(False, "AdminDB data not found", code=404)

        processed_data = custom_serializer(admindb_data)
        
        if "_id" in processed_data:
            processed_data["_id"] = {"$oid": str(processed_data["_id"])}
        
        await redisClient.set(
            "admindb", 
            json.dumps(processed_data, default=custom_serializer),
            ex=3600
        )

        logger.info("AdminDB data retrieved successfully")
        return create_response(True, "Data retrieved successfully", processed_data)
    
    except Exception as e:
        logger.error(f"Error retrieving admin DB: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)

@admindb_router.get("/db/all")
async def get_admindb_all():
    try:
        cached_item = await redisClient.get("admindball")
        if cached_item:
            data = json.loads(cached_item)
            return create_response(True, "Data retrieved successfully", data)
        
        admindb_data = await Admindball.find_one({})
        if not admindb_data:
            logger.warning("AdminDB all data not found")
            return create_response(False, "AdminDB all data not found", code=404)
        
        processed_data = custom_serializer(admindb_data)
        
        if "_id" in processed_data:
            processed_data["_id"] = {"$oid": str(processed_data["_id"])}
        
        await redisClient.set(
            "admindball", 
            json.dumps(processed_data, default=custom_serializer),
            ex=3600
        )

        logger.info("AdminDB all data retrieved successfully")
        return create_response(True, "Data retrieved successfully", admindb_data)

    except Exception as e:
        logger.error(f"Error retrieving admin DB all: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)

@admindb_router.get("/db/emp/{empid}")
async def get_admindb_emp(empid: str):
    try:
        cached_item = await redisClient.get(f"admindbemp/{empid}")
        if cached_item:
            data = json.loads(cached_item)
            return create_response(True, "Data retrieved successfully", data)
        
        admindb_data = await Admindbemp.find_one(Admindbemp.briefUserDetails.empid == empid)
        if not admindb_data:
            logger.warning(f"AdminDB data not found for empid: {empid}")
            return create_response(False, "AdminDB data not found", code=404)
        
        processed_data = custom_serializer(admindb_data)
        
        if "_id" in processed_data:
            processed_data["_id"] = {"$oid": str(processed_data["_id"])}
        
        await redisClient.set(
            f"admindbemp/{empid}", 
            json.dumps(processed_data, default=custom_serializer),
            ex=3600
        )

        logger.info(f"AdminDB data retrieved successfully for empid: {empid}")
        return create_response(True, "Data retrieved successfully", admindb_data)

    except Exception as e:
        logger.error(f"Error retrieving admin DB for empid {empid}: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)
    
@admindb_router.get("/search/{query}")
async def search(query: str):
    try:
        cached_item = await redisClient.get(f"search/{query}")
        if cached_item:
            return json.loads(cached_item)
        
        res = await vector_search(query)
        if not res:
            return create_response(False, "No results found", code=404)
        
        resdict = {"results": res}

        if "_id" in resdict:
            resdict["_id"] = {"$oid": str(resdict["_id"])}

        await redisClient.set(
            f"search/{query}", 
            json.dumps(resdict, default=custom_serializer),
            ex=3600
        )

        logger.info(f"Search results retrieved successfully for query: {query}")
        return resdict
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        return create_response(False, "Internal server error", code=500)
    
emails = {
    "EMP0125":"harshxgupta931@gmail.com",
    "EMP0491":"flameable.powder@gmail.com"
}

names = {
    "EMP0125":"Harsh Gupta",
    "EMP0491":"Abhinav Kumar Singh"
}

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "dummy_sender@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "dummy_app_password")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendMail(to_email: str, subject: str, empName: str, link: str):
    """
    Send an email with the given parameters.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    message = ""
    with open("doc.html", "r") as file:
        message = file.read().replace("{{username}}", empName).replace("{{link}}", link)
    msg.attach(MIMEText(message, "html"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email} successfully!")
        return f"Email sent to {to_email}"
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return f"Failed: {e}"
    
@admindb_router.post("/meet/{empid}")
async def get_meet(empid: str):
    try:
        meet = await Meet.find_one({})
        if not meet:
            logger.warning("Meet data not found")
            return create_response(False, "Meet data not found", code=404)
        url = meet.meetUrl
        email = emails.get(empid)
        if not email:
            logger.warning(f"Email not found for empid: {empid}")
            return create_response(False, "Email not found", code=404)
        subject = "Meeting Link with HR"
        empName = names.get(empid)
        if not empName:
            logger.warning(f"Employee name not found for empid: {empid}")
            return create_response(False, "Employee name not found", code=404)
        sendMail(email, subject, empName, url)
        logger.info(f"Email sent successfully to {email}")
        if not url:
            logger.warning("Meet URL not found")
            return create_response(False, "Meet URL not found", code=404)
        logger.info("Meet URL retrieved successfully")
        return create_response(True, "Meet URL retrieved successfully", url)
    except Exception as e:
        logger.error(f"Error creating a meeting: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)