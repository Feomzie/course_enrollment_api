import time

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(401, "Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(401, "User not found")

    if not user.is_active:
        raise HTTPException(401, "Inactive user")
    
    return user


def admin_required(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admin privileges required")
    return user


def student_required(user=Depends(get_current_user)):
    if user.role != "student":
        raise HTTPException(403, "Student privileges required")
    return user


def auth_rate_limit(request: Request):
    limit = 20
    window_seconds = 60
    client_ip = request.client.host if request.client else "unknown"
    key = f"{request.url.path}:{client_ip}"

    now = time.time()
    window_start = now - window_seconds

    if not hasattr(auth_rate_limit, "requests"):
        auth_rate_limit.requests = {}

    request_times = auth_rate_limit.requests.setdefault(key, [])
    request_times[:] = [timestamp for timestamp in request_times if timestamp >= window_start]

    if len(request_times) >= limit:
        raise HTTPException(429, "Too many authentication requests. Please try again later.")

    request_times.append(now)