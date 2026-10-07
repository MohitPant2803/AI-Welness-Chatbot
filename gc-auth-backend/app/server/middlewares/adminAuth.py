import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from server.config import JWT_SECRET

logger = logging.getLogger("admin_auth_middleware")
logger.setLevel(logging.INFO)

SECRET_KEY = JWT_SECRET
ALGORITHM = "HS256"

def create_response(success: bool, message: str, code=200):
    return JSONResponse(content={"success": success, "message": message, "code": code}, status_code=code)

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if not request.url.path.startswith("/api/v1/admin/details"):
                return await call_next(request)

            token = request.headers.get("Authorization")
            if not token:
                logger.warning("Missing Authorization token")
                return create_response(False, "Token is missing", code=401)

            token = token.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            adminid = payload.get("adminid")
            if not adminid:
                logger.warning("Invalid token: adminid not found")
                return create_response(False, "Token is invalid: adminid not found", code=401)

            request.state.adminid = adminid
            logger.info(f"Authenticated admin: {adminid}")

        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            return create_response(False, "Token is invalid: expired", code=401)

        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return create_response(False, "Token is invalid: invalid", code=401)

        except Exception as e:
            logger.exception("Unexpected error in authentication")
            return create_response(False, "Internal server error", code=500)

        return await call_next(request)