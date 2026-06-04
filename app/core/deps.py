from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
    
    return user


def admin_required(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admin privileges required")
    return user


def student_required(user=Depends(get_current_user)):
    if user.role != "student":
        raise HTTPException(403, "Student privileges required")
    return user