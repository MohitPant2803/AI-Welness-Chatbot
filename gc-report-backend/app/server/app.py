from fastapi import FastAPI
from server.database import init_db
from server.routes.reportAll import admindball_router
from server.routes.reportEmp import admindbemp_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        await init_db()
        print("Connected to DB")
    except Exception as e:
        print("error occurred:", e)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admindball_router, prefix="/api/v1/get/report/all", tags=["AdminDB"])
app.include_router(admindbemp_router, prefix="/api/v1/get/report", tags=["AdminDB"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to your Beanie-powered app!"}
