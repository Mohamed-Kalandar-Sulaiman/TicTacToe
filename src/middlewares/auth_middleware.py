# src/middleware/auth_middleware.py
from fastapi import Request, HTTPException
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

SECRET_KEY = "your_secret_key"  # Change this to a strong secret key
ALGORITHM = "HS256"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for docs and redoc
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(status_code=401,
                                detail="Not authenticated")

        # Extract token from "Bearer <token>"
        token = token.split(" ")[1] if " " in token else token

        try:
            # Decode the token to verify it
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload  # Store user info in the request state
        except JWTError:
            raise HTTPException(status_code=403, detail="Could not validate credentials")

        response = await call_next(request)
        return response
