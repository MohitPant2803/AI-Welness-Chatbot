from fastapi import FastAPI
from server.database import init_db
from server.routes.auth import auth_router
from server.routes.user import user_router
from server.routes.adminAuth import admin_auth_router
from server.routes.admindb import admindb_router
from server.middlewares.auth import AuthMiddleware
from server.middlewares.adminAuth import AdminAuthMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(AuthMiddleware)
app.add_middleware(AdminAuthMiddleware)

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

app.include_router(auth_router, prefix="/api/v1/emp/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/emp/details", tags=["User"])
app.include_router(admin_auth_router, prefix="/api/v1/admin/auth", tags=["AdminAuth"])
app.include_router(admindb_router, prefix="/api/v1/admin/details", tags=["AdminDB"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to your Beanie-powered app!"}
