import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from fastapi.responses import JSONResponse
from server.config import JWT_SECRET

logger = logging.getLogger("auth_middleware")
logger.setLevel(logging.INFO)

SECRET_KEY = JWT_SECRET
ALGORITHM = "HS256"

def create_response(success: bool, message: str, code=200):
    return JSONResponse(content={"success": success, "message": message, "code": code}, status_code=code)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if not request.url.path.startswith("/api/v1/emp/details"):
                return await call_next(request)

            token = request.headers.get("Authorization")
            if not token:
                logger.warning("Missing Authorization token")
                return create_response(False, "Token is missing", code=401)

            token = token.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            empid = payload.get("empid")
            if not empid:
                logger.warning("Invalid token: empid not found")
                return create_response(False, "Token is invalid: empid not found", code=401)

            request.state.empid = empid
            logger.info(f"Authenticated user: {empid}")

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
