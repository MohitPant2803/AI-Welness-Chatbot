from .celery import app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models.queue import Queue, QueueUser
from models.admindbemp import Admindbemp
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import MONGO_URI
import google.generativeai as genai
import asyncio
from proj.analyse import analyze_employee_moods
from proj.analyse_emps import main
import json
import datetime

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = ""
SENDER_PASSWORD = ""

genai.configure(api_key="")
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def sendMail(to_email: str, subject: str, empName: str):
    """
    Send an email with the given parameters.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    message = ""
    with open("doc.html", "r") as file:
        message = file.read().replace("{{username}}", empName)
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

async def ensureDbInitialized():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client.get_default_database()
        await init_beanie(database=db, document_models=[Queue, Admindbemp])
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization failed: {e}")

async def analyseEmpsAsync():
    await ensureDbInitialized()
    queue = await Queue.find_one({})
    if not queue:
        queue = Queue()
        await queue.insert()

    main()
    analyze_employee_moods()

    data = {}

    with open("employee_questions.json", "r") as f:
        data = json.load(f)

    for key, value in data.items():
        new_user = QueueUser(
            empid=key,
            emailID=value["email"],
            message=value["recommended_question"],
            empName=value["name"]
        )
        print(f"Adding user {key} to queue, user : ", new_user)

        queue.users.append(new_user)
        await queue.save()

async def sendMailFromQueueAsync():
    await ensureDbInitialized()
    queue = await Queue.find_one({})
    if not queue or not queue.users:
        return
    
    processed_users = []
    remaining_users = []
    
    for user in queue.users:
        try:
            EMP = await Admindbemp.find_one(Admindbemp.briefUserDetails.empid == user.empid)
            if not EMP:
                print(f"User {user.empid} not found in Admindbemp.")
                remaining_users.append(user)
                continue
            EMP.chatHistory.append({
                "message": user.message,
                "timestamp": datetime.datetime.now(),
                "sender": "ai"
            })
            await EMP.save()
            print(f"Sending email to {user.emailID} with message: {user.message}")
            if(user.emailID == None or user.emailID == ""):
                print(f"✅ Email sent successfully!")
            sendMail(to_email=user.emailID, subject=user.message, empName=user.empName)
            processed_users.append(user.empid)
        except Exception as e:
            print(f"Error processing user {user.empid}: {e}")
            remaining_users.append(user)
    
    if processed_users:
        queue.users = [user for user in queue.users if user.empid not in processed_users]
        await queue.save()

@app.task(bind=True, autoretry_for=(smtplib.SMTPException,), retry_backoff=True, max_retries=3)
def sendMailFromQueue(self):
    asyncio.run(sendMailFromQueueAsync())

@app.task(bind=True, autoretry_for=(smtplib.SMTPException,), retry_backoff=True, max_retries=3)
def analyseEmps(self):
    asyncio.run(analyseEmpsAsync())
