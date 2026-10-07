from fastapi import FastAPI
from server.routes.chat import chat_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(chat_router, prefix="/ws", tags=["Auth"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to your Beanie-powered ws app!"}