from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from server.routes.app import chat
import jwt

chat_router = APIRouter()

EMPID: str = ""
SECRET_KEY = "harshlovesrandomhotgirl"
ALGORITHM = "HS256"

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_text(message)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)

manager = ConnectionManager()

@chat_router.websocket("/wsconnect/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await manager.connect(websocket)
    if not token:
        print("no token found")
        await websocket.close()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        empid = payload.get("empid")
        if not empid:
            print("no empid found")
            await websocket.close()
            return
    except jwt.ExpiredSignatureError:
        print("Token expired")
        await websocket.close()
        return
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    empid = payload.get("empid")
    if not empid:
        print("no empid found")
        await websocket.close()
        return
    try:
        while True:
            data = await websocket.receive_text()
            AIres = await chat(data, empid)
            await manager.send_personal_message(f"{AIres}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)