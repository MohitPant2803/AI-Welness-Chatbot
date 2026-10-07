from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime

class QueueUser(BaseModel):
    empid: str
    emailID: str
    message: str
    empName: str

class Queue(Document):
    users: List[QueueUser] = []